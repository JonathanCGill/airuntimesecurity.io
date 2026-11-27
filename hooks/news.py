"""MkDocs hook: surface the news page across the site.

docs/news.md is the only part of the site that changes every fortnight. Each
entry carries a MASO verdict block:

    !!! success "MASO verdict: Prevented"
        **MASO would have prevented this.** One or two sentences.

        | Failure point | MASO control | Effect |
        |---|---|---|
        | ... | [IA-2.7 Vaulted per-flow credential brokering](maso/controls/identity-and-access.md) | ... |

        **Not covered**: what MASO would not have caught.

This hook parses those entries once per build and uses them to:

- replace `<!-- NEWS_LATEST -->` on the home page with the newest entries,
- replace `<!-- NEWS_SCOREBOARD -->` on the news page with verdict counts,
- replace `<!-- NEWS_BY_CONTROL -->` on validated-against.md with a control index,
- append a "Seen in the wild" section to each MASO control page,
- write an Atom feed (`feed.xml`) with one entry per news item.

Nothing here edits files in docs/; everything is applied to the page markdown
at build time, so news.md stays the single source.
"""

from __future__ import annotations

import html
import logging
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from markdown.extensions.toc import slugify

log = logging.getLogger("mkdocs.hooks.news")

NEWS_SRC = "news.md"
CONTROLS_DIR = "maso/controls/"

HEADING_RE = re.compile(r"^### (\d{4}-\d{2}-\d{2}): (.+?)\s*$")
TAGS_RE = re.compile(r"^\*\*Tags\*\*:\s*(.+)$")
VERDICT_RE = re.compile(r'^!!! (success|warning|danger) "MASO (verdict|coverage): ([^"]+)"\s*$')
CONTROL_ID_RE = re.compile(r"\b((?:EC|SC|IA|OB|PG|AT|MC|DP|PA|OI|EI)-\d+\.\d+[a-z]?)\b")
CONTROL_DEF_RE = re.compile(r"^\| \*\*([A-Z]{2}-\d+\.\d+[a-z]?)\*\* ([^|]+?)\s*\|", re.M)

# Verdict type -> CSS modifier. The admonition type carries the meaning, the
# label is shown as written so the wording stays the author's.
VERDICT_CLASS = {"success": "good", "warning": "partial", "danger": "none"}

SECTION_TITLE = "Seen in the wild"


@dataclass
class NewsItem:
    date: date
    title: str
    anchor: str
    tags: list[str] = field(default_factory=list)
    kind: str = ""          # "verdict" (incident) or "coverage" (research, guidance, launch)
    vtype: str = ""         # success | warning | danger
    label: str = ""         # Prevented, Contained, Not prevented, Covered, ...
    bottom_line: str = ""   # first paragraph of the verdict block, plain text
    summary: str = ""       # first paragraph after the tags, plain text
    controls: list[str] = field(default_factory=list)
    owned_by: str = ""      # who owns what MASO does not cover, plain text


_items: list[NewsItem] = []
_control_pages: dict[str, str] = {}   # control id -> src_uri of the page defining it
_control_names: dict[str, str] = {}


# ── parsing ────────────────────────────────────────────────────────────────

def _plain(md: str) -> str:
    """Strip the inline markdown used in news entries down to plain text."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", md)
    text = re.sub(r"[*`]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def heading_anchor(heading_text: str) -> str:
    """The id MkDocs' toc extension gives an h3 with this text."""
    return slugify(_plain(heading_text), "-")


def _finish_verdict(item: NewsItem, block: list[str]) -> None:
    """Pull the bottom line and control IDs out of a verdict block's lines."""
    para: list[str] = []
    for line in block:
        if line.startswith("**Owned by**:"):
            item.owned_by = _plain(line.split(":", 1)[1])
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2:
                for cid in CONTROL_ID_RE.findall(cells[1]):
                    if cid not in item.controls:
                        item.controls.append(cid)
        elif not item.bottom_line:
            if line.strip():
                para.append(line.strip())
            elif para:
                item.bottom_line = _plain(" ".join(para))
    if para and not item.bottom_line:
        item.bottom_line = _plain(" ".join(para))


def parse_news(text: str) -> list[NewsItem]:
    start = text.find("<!-- NEWS_START -->")
    end = text.find("<!-- NEWS_END -->")
    if start == -1 or end == -1:
        return []

    items: list[NewsItem] = []
    item: NewsItem | None = None
    block: list[str] | None = None   # lines of the current verdict block, dedented
    para: list[str] = []
    seen_tags = False

    def end_para():
        nonlocal para
        if item is not None and seen_tags and para and not item.summary:
            item.summary = _plain(" ".join(para))
        para = []

    def end_block():
        nonlocal block
        if item is not None and block is not None:
            _finish_verdict(item, block)
        block = None

    for line in text[start:end].splitlines():
        if block is not None:
            if line.startswith("    ") or not line.strip():
                block.append(line[4:])
                continue
            end_block()

        m = HEADING_RE.match(line)
        if m:
            end_para()
            item = NewsItem(
                date=date.fromisoformat(m.group(1)),
                title=m.group(2),
                anchor=heading_anchor(f"{m.group(1)}: {m.group(2)}"),
            )
            items.append(item)
            seen_tags = False
            continue
        if item is None:
            continue

        t = TAGS_RE.match(line)
        if t:
            item.tags = [s.strip() for s in t.group(1).split(",") if s.strip()]
            seen_tags = True
            continue

        v = VERDICT_RE.match(line)
        if v:
            end_para()
            item.vtype, item.kind, item.label = v.group(1), v.group(2), v.group(3).strip()
            block = []
            continue

        if line.strip():
            para.append(line.strip())
        else:
            end_para()
    end_block()
    end_para()
    return items


def index_controls(docs_dir: Path) -> tuple[dict[str, str], dict[str, str]]:
    pages, names = {}, {}
    for path in sorted((docs_dir / CONTROLS_DIR).glob("*.md")):
        src = f"{CONTROLS_DIR}{path.name}"
        for cid, name in CONTROL_DEF_RE.findall(path.read_text(encoding="utf-8")):
            pages.setdefault(cid, src)
            names.setdefault(cid, name.strip())
    return pages, names


def validate(items: list[NewsItem], control_pages: dict[str, str]) -> list[str]:
    problems = []
    for it in items:
        where = f"news item {it.date} '{it.title[:50]}'"
        if not it.label:
            problems.append(f"{where}: no MASO verdict or coverage block")
            continue
        if not it.bottom_line:
            problems.append(f"{where}: verdict block has no bottom line")
        if not it.owned_by:
            problems.append(f"{where}: verdict block has no 'Owned by' line")
        if not it.controls:
            problems.append(f"{where}: verdict table names no MASO control")
        for cid in it.controls:
            if cid not in control_pages:
                problems.append(f"{where}: unknown control {cid}")
    return problems


# ── rendering ──────────────────────────────────────────────────────────────

def _fmt_date(d: date) -> str:
    return f"{d.day} {d.strftime('%b %Y')}"


def _rel(from_src: str, to_src: str) -> str:
    """Relative markdown link from one docs page to another."""
    depth = from_src.count("/")
    return "../" * depth + to_src


def render_latest(items: list[NewsItem], count: int = 3) -> str:
    cards = []
    for it in items[:count]:
        controls = " &middot; ".join(html.escape(c) for c in it.controls[:4])
        cards.append(
            f'<a class="airs-rd-news__item" href="/news/#{it.anchor}">'
            f'<span class="airs-rd-verdict airs-rd-verdict--{VERDICT_CLASS[it.vtype]}">'
            f'{"MASO" if it.kind == "verdict" else "Coverage"}: {html.escape(it.label)}</span>'
            f'<span class="airs-rd-news__date">{_fmt_date(it.date)}</span>'
            f'<span class="airs-rd-news__title">{html.escape(it.title)}</span>'
            f'<span class="airs-rd-news__bottom">{html.escape(it.bottom_line)}</span>'
            f'<span class="airs-rd-news__controls">{controls}</span>'
            "</a>"
        )
    return (
        '<div class="airs-rd-news__grid">' + "".join(cards) + "</div>\n"
        + f'<p class="airs-rd-news__score">{html.escape(scoreline(items))}</p>'
    )


def scoreline(items: list[NewsItem]) -> str:
    v = [i for i in items if i.kind == "verdict"]
    counts = {k: sum(1 for i in v if i.vtype == k) for k in VERDICT_CLASS}
    return (
        f"Across the {len(v)} incidents on the news page: MASO would have prevented "
        f"{counts['success']}, contained {counts['warning']}, and not prevented {counts['danger']}."
    )


def render_scoreboard(items: list[NewsItem]) -> str:
    v = [i for i in items if i.kind == "verdict"]
    c = [i for i in items if i.kind == "coverage"]
    lines = [
        "| Verdict | Incidents |",
        "|---|---|",
    ]
    for vtype, label in (("success", "Prevented"), ("warning", "Contained"), ("danger", "Not prevented")):
        hits = [i for i in v if i.vtype == vtype]
        links = ", ".join(f"[{_fmt_date(i.date)}](#{i.anchor})" for i in hits) or "None"
        lines.append(f"| **{label}** ({len(hits)}) | {links} |")
    out = "\n".join(lines)
    if c:
        out += (
            f"\n\nA further {len(c)} entries are research, guidance, or product launches rather than "
            "incidents. Those carry a **coverage** rating instead: whether MASO already specifies what "
            "the item calls for."
        )
    return out


def render_control_section(page_src: str, page_controls: set[str], items: list[NewsItem]) -> str:
    rows = []
    for cid in sorted(page_controls, key=_control_sort_key):
        for it in items:
            if cid in it.controls:
                link = f"{_rel(page_src, NEWS_SRC)}#{it.anchor}"
                rows.append(
                    f"| **{cid}** | [{_fmt_date(it.date)}: {_md_escape(it.title)}]({link}) | {it.label} |"
                )
    if not rows:
        return ""
    return (
        f"## {SECTION_TITLE}\n\n"
        "Recent incidents and research from the [news page]"
        f"({_rel(page_src, NEWS_SRC)}) that cite a control on this page, with the verdict given there. "
        "This list is generated from the news page at build time.\n\n"
        "| Control | News item | Verdict |\n|---|---|---|\n" + "\n".join(rows) + "\n"
    )


def render_by_control(page_src: str, items: list[NewsItem]) -> str:
    by: dict[str, list[NewsItem]] = {}
    for it in items:
        for cid in it.controls:
            by.setdefault(cid, []).append(it)
    rows = []
    for cid in sorted(by, key=_control_sort_key):
        page = _control_pages.get(cid)
        name = _control_names.get(cid, "")
        ctrl = f"[{cid} {name}]({_rel(page_src, page)})" if page else cid
        refs = "<br>".join(
            f"[{_fmt_date(i.date)}]({_rel(page_src, NEWS_SRC)}#{i.anchor}): {i.label}" for i in by[cid]
        )
        rows.append(f"| {ctrl} | {len(by[cid])} | {refs} |")
    return "| Control | Items | News items and verdicts |\n|---|---|---|\n" + "\n".join(rows) + "\n"


def _control_sort_key(cid: str):
    prefix, num = cid.split("-")
    major, minor = num.split(".")
    minor_digits = re.match(r"\d+", minor).group(0)
    return (prefix, int(major), int(minor_digits), minor)


def _md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")


def render_feed(items: list[NewsItem], site_url: str) -> str:
    base = site_url.rstrip("/") + "/"
    updated = items[0].date if items else date.today()
    entries = []
    for it in items:
        url = f"{base}news/#{it.anchor}"
        when = datetime(it.date.year, it.date.month, it.date.day, tzinfo=timezone.utc).isoformat()
        prefix = "MASO verdict" if it.kind == "verdict" else "MASO coverage"
        content = f"{prefix}: {it.label}. {it.bottom_line}\n\n{it.summary}"
        entries.append(
            "  <entry>\n"
            f"    <title>{xml_escape(it.title)}</title>\n"
            f'    <link href="{xml_escape(url)}"/>\n'
            f"    <id>{xml_escape(url)}</id>\n"
            f"    <updated>{when}</updated>\n"
            + "".join(f'    <category term="{xml_escape(t)}"/>\n' for t in it.tags)
            + f"    <summary>{xml_escape(content)}</summary>\n"
            "  </entry>\n"
        )
    feed_updated = datetime(updated.year, updated.month, updated.day, tzinfo=timezone.utc).isoformat()
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">\n'
        "  <title>AI Runtime Security News</title>\n"
        "  <subtitle>Agentic AI incidents and research, each checked against the MASO controls.</subtitle>\n"
        f'  <link href="{base}news/"/>\n'
        f'  <link rel="self" href="{base}feed.xml"/>\n'
        f"  <id>{base}news/</id>\n"
        f"  <updated>{feed_updated}</updated>\n"
        + "".join(entries)
        + "</feed>\n"
    )


# ── mkdocs events ──────────────────────────────────────────────────────────

def on_config(config, **kwargs):
    global _items, _control_pages, _control_names
    docs_dir = Path(config["docs_dir"])
    news_path = docs_dir / NEWS_SRC
    _control_pages, _control_names = index_controls(docs_dir)
    _items = parse_news(news_path.read_text(encoding="utf-8")) if news_path.exists() else []
    for problem in validate(_items, _control_pages):
        log.warning(problem)
    return config


def on_page_markdown(markdown, page, config, files, **kwargs):
    if not _items:
        return markdown
    src = page.file.src_uri

    if src == "README.md" and "<!-- NEWS_LATEST -->" in markdown:
        return markdown.replace("<!-- NEWS_LATEST -->", render_latest(_items))

    if src == NEWS_SRC and "<!-- NEWS_SCOREBOARD -->" in markdown:
        return markdown.replace("<!-- NEWS_SCOREBOARD -->", render_scoreboard(_items))

    if src == "validated-against.md" and "<!-- NEWS_BY_CONTROL -->" in markdown:
        return markdown.replace("<!-- NEWS_BY_CONTROL -->", render_by_control(src, _items))

    if src.startswith(CONTROLS_DIR):
        defined = {cid for cid, page_src in _control_pages.items() if page_src == src}
        section = render_control_section(src, defined, _items)
        if not section:
            return markdown
        marker = '\n!!! info "References"'
        pos = markdown.rfind(marker)
        if pos == -1:
            return markdown.rstrip() + "\n\n" + section
        return markdown[:pos].rstrip() + "\n\n" + section + "\n" + markdown[pos:]

    return markdown


def on_post_build(config, **kwargs):
    if not _items:
        return
    site_url = config.get("site_url") or "https://airuntimesecurity.io/"
    out = Path(config["site_dir"]) / "feed.xml"
    out.write_text(render_feed(_items, site_url), encoding="utf-8")

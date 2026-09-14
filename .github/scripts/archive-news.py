#!/usr/bin/env python3
"""Move news items older than three months from news.md to the news archive.

The archive lives outside the MkDocs source tree and is read on GitHub, so
relative links inside archived items are rewritten to point back into `docs/`.
"""

import posixpath
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
NEWS_FILE = DOCS / "news.md"
ARCHIVE_FILE = ROOT / "archive" / "2026-03-31" / "news-archive.md"

ITEM_PATTERN = re.compile(r"^### (\d{4}-\d{2}-\d{2}): ")
CUTOFF = date.today() - timedelta(days=90)

LINK_PATTERN = re.compile(r"\]\(([^)\s]+)\)")
# Absolute, external, and anchor-only targets are already location-independent.
SKIP_PREFIXES = ("http://", "https://", "#", "mailto:", "/")

# Every relative target in a news item is written relative to docs/news.md, so
# it is resolved against `docs/` and re-expressed relative to the archive file.
# This includes parent-relative targets such as `../README.md`, which resolve to
# the repository root from docs/news.md and would silently point at
# archive/2026-03-31/README.md if they were copied across unchanged.
NEWS_DIR = "docs"
ARCHIVE_DIR = "archive/2026-03-31"


def rewrite_links(text: str) -> str:
    """Rewrite links written relative to docs/news.md so they resolve from the archive."""

    def repl(match: re.Match[str]) -> str:
        target = match.group(1)
        if target.startswith(SKIP_PREFIXES):
            return match.group(0)

        path, sep, anchor = target.partition("#")
        if not path:
            return match.group(0)

        # Resolve against docs/, then re-express relative to the archive directory.
        resolved = posixpath.normpath(posixpath.join(NEWS_DIR, path))
        rebased = posixpath.relpath(resolved, ARCHIVE_DIR)
        return f"]({rebased}{sep}{anchor})"

    return LINK_PATTERN.sub(repl, text)


def parse_items(text: str) -> list[tuple[date | None, str]]:
    """Split the NEWS_START/NEWS_END block into individual items."""
    items: list[tuple[date | None, str]] = []
    current_lines: list[str] = []
    current_date: date | None = None

    for line in text.splitlines(keepends=True):
        m = ITEM_PATTERN.match(line)
        if m:
            if current_lines:
                items.append((current_date, "".join(current_lines)))
            current_date = date.fromisoformat(m.group(1))
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        items.append((current_date, "".join(current_lines)))

    return items


def run() -> None:
    news_text = NEWS_FILE.read_text()
    archive_text = ARCHIVE_FILE.read_text()

    start_marker = "<!-- NEWS_START -->"
    end_marker = "<!-- NEWS_END -->"
    archive_start = "<!-- ARCHIVE_START -->"
    archive_end = "<!-- ARCHIVE_END -->"

    news_start = news_text.index(start_marker) + len(start_marker)
    news_end = news_text.index(end_marker)
    block = news_text[news_start:news_end]

    items = parse_items(block)

    keep: list[str] = []
    archive: list[str] = []

    for item_date, content in items:
        if item_date is not None and item_date < CUTOFF:
            archive.append(rewrite_links(content))
        else:
            keep.append(content)

    if not archive:
        print("No items to archive.")
        sys.exit(0)

    # Rebuild news.md
    if keep:
        keep_block = "\n" + "".join(keep)
    else:
        keep_block = "\n\n*No recent items. Check the [news archive](https://github.com/JonathanCGill/airuntimesecurity.io/blob/main/archive/2026-03-31/news-archive.md).*\n\n"
    new_news = news_text[:news_start] + keep_block + news_text[news_end:]
    NEWS_FILE.write_text(new_news)

    # Append to archive
    arch_start = archive_text.index(archive_start) + len(archive_start)
    arch_end = archive_text.index(archive_end)
    existing = archive_text[arch_start:arch_end].strip()

    # Remove placeholder text
    if existing == "*No archived items yet.*":
        existing = ""

    archived_block = "".join(archive).strip()
    if existing:
        new_archive_content = f"\n\n{archived_block}\n\n{existing}\n\n"
    else:
        new_archive_content = f"\n\n{archived_block}\n\n"

    new_archive = archive_text[:arch_start] + new_archive_content + archive_text[arch_end:]
    ARCHIVE_FILE.write_text(new_archive)

    print(f"Archived {len(archive)} item(s).")


if __name__ == "__main__":
    run()

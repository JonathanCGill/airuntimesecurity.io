#!/usr/bin/env python3
"""Keep the README and headline MASO figures in step with the source files.

Every number this script manages is derived from the files that define it
(control tables, the risk register, the red-team playbook, the test suite),
never typed by hand.

Usage:
    python .github/scripts/readme_facts.py --check   # exit 1 if anything is stale
    python .github/scripts/readme_facts.py --write   # rewrite stale figures in place

--check also fails on README links to local files that do not exist.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTROLS = ROOT / "docs/maso/controls"

# (display name, ID prefix, file stem) for the eleven MASO control domains.
DOMAINS = [
    ("Identity & Access", "IA", "identity-and-access"),
    ("Data Protection", "DP", "data-protection"),
    ("Extraction Integrity", "EI", "extraction-integrity"),
    ("Execution Control", "EC", "execution-control"),
    ("Observability", "OB", "observability"),
    ("Prompt, Goal & Epistemic Integrity", "PG", "prompt-goal-and-epistemic-integrity"),
    ("Supply Chain", "SC", "supply-chain"),
    ("Objective Intent", "OI", "objective-intent"),
    ("Privileged Agent Governance", "PA", "privileged-agent-governance"),
    ("Model Cognition Assurance", "MC", "model-cognition-assurance"),
    ("Agentic Task Mandate", "AT", "agentic-task-mandate"),
]


def maso_controls() -> dict[str, list[tuple[str, str, int]]]:
    """Return {prefix: [(id, title, tier), ...]} from each domain's control tables.

    Only IDs carrying the domain's own prefix count, so cross-referenced
    controls quoted in another domain's file are not double counted.
    """
    out = {}
    for _, prefix, stem in DOMAINS:
        text = (CONTROLS / f"{stem}.md").read_text(encoding="utf-8")
        seen: dict[str, tuple[str, int]] = {}
        pattern = rf"^\| \*\*({prefix}-(\d)\.(\d+))\*\* ([^|]+?) \|"
        for m in re.finditer(pattern, text, re.M):
            seen.setdefault(m.group(1), (m.group(4).strip(), int(m.group(2))))
        ids = sorted(seen, key=lambda i: [int(n) for n in i.split("-")[1].split(".")])
        out[prefix] = [(i, *seen[i]) for i in ids]
    return out


def facts() -> dict[str, int]:
    controls = maso_controls()
    flat = [c for cs in controls.values() for c in cs]

    register = (CONTROLS / "risk-register.md").read_text(encoding="utf-8")
    table = register.split("## Risk Table", 1)[1].split("## Consolidated", 1)[0]

    playbook = (ROOT / "docs/maso/red-team/red-team-playbook.md").read_text(encoding="utf-8")

    tests = sum(
        len(re.findall(r"^\s*(?:async\s+)?def test_", p.read_text(encoding="utf-8"), re.M))
        for p in (ROOT / "tests").glob("test_*.py")
    )

    audit = (ROOT / "MASO-CONTROL-AUDIT.md").read_text(encoding="utf-8")
    env = len(re.findall(r"^- \[ \] \*\*ENV-\d+\*\*", audit, re.M))

    return {
        "controls": len(flat),
        "with_env": len(flat) + env,
        "domains": len(DOMAINS),
        "tier1": sum(1 for c in flat if c[2] == 1),
        "tier2": sum(1 for c in flat if c[2] == 2),
        "tier3": sum(1 for c in flat if c[2] == 3),
        "risks": len(re.findall(r"^\| [A-Z]{2,3}-\d+ \|", table, re.M)),
        "risk_categories": len(re.findall(r"^### ", table, re.M)),
        "scenarios": len(re.findall(r"^### RT-\d+", playbook, re.M)),
        "tests": tests,
    }


# (file, regex with one group per fact, fact keys in group order).
# Each regex must match exactly once; the groups are the numbers to keep current.
RULES = [
    ("README.md", r"Red%20Team-(\d+)%20scenarios", ["scenarios"]),
    ("README.md", r"\[!\[Red Team: (\d+) scenarios\]", ["scenarios"]),
    ("README.md", r"\*\*\[MASO Framework\]\(docs/maso/\)\*\*, (\d+) control domains", ["domains"]),
    ("README.md", r"risk-register\.md\), (\d+) risks across (\d+) categories", ["risks", "risk_categories"]),
    ("README.md", r"multi-agent orchestration: (\d+) controls across (\d+) domains", ["controls", "domains"]),
    ("README.md", r"plus (\d+) emergent risks", ["risks"]),
    ("README.md", r"# (\d+) domain specifications \+ risk register", ["domains"]),
    ("README.md", r"Adversarial test playbook \((\d+) scenarios\)", ["scenarios"]),
    ("README.md", r"tests/ +# (\d+) tests", ["tests"]),
    ("docs/maso/reference.md", r"Together they define up to (\d+) controls", ["controls"]),
    ("docs/maso/reference.md", r"a Tier 1 deployment uses roughly (\d+), not all (\d+)\.", ["tier1", "controls"]),
    ("docs/maso/maso-2.0-anticipated-changes.md", r"MASO's (\d+) controls", ["controls"]),
    ("MASO-CONTROL-AUDIT.md", r"\| \*\*Core total \(11 domains\)\*\* \| \| \*\*(\d+)\*\* \|", ["controls"]),
    ("MASO-CONTROL-AUDIT.md", r"\| \*\*With ENV\*\* \| \| \*\*(\d+)\*\* \|", ["with_env"]),
    ("MASO-CONTROL-AUDIT.md", r"\| Tier 1 \(Supervised\) \| (\d+) \| (\d+) \|", ["tier1", "tier1"]),
    ("MASO-CONTROL-AUDIT.md", r"\| Tier 3 \(Autonomous\) \| (\d+) \| (\d+) \|", ["tier3", "controls"]),
    ("MASO-CONTROL-AUDIT.md", r"A Tier 1 deployment applies (\d+) controls, not (\d+)\.", ["tier1", "controls"]),
]


def apply_rules(f: dict[str, int], write: bool) -> list[str]:
    problems = []
    texts: dict[str, str] = {}
    for rel, pattern, keys in RULES:
        text = texts.setdefault(rel, (ROOT / rel).read_text(encoding="utf-8"))
        matches = list(re.finditer(pattern, text))
        if len(matches) != 1:
            problems.append(f"{rel}: pattern matched {len(matches)} times, expected 1: {pattern}")
            continue
        m = matches[0]
        new = text
        for g in range(len(keys), 0, -1):  # right to left keeps offsets valid
            want = str(f[keys[g - 1]])
            if m.group(g) != want:
                problems.append(f"{rel}: '{m.group(0)}' should say {want} ({keys[g - 1]})")
                new = new[: m.start(g)] + want + new[m.end(g) :]
        texts[rel] = new
    if write:
        for rel, text in texts.items():
            path = ROOT / rel
            if path.read_text(encoding="utf-8") != text:
                path.write_text(text, encoding="utf-8")
    return problems


def tier2_cumulative(f: dict[str, int], write: bool) -> list[str]:
    """The Tier 2 row of the audit table carries a derived cumulative figure."""
    rel = "MASO-CONTROL-AUDIT.md"
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    want = f"| Tier 2 (Managed) | {f['tier2']} | {f['tier1'] + f['tier2']} |"
    new = re.sub(r"\| Tier 2 \(Managed\) \| \d+ \| \d+ \|", want, text)
    if new == text:
        return []
    if write:
        path.write_text(new, encoding="utf-8")
    return [f"{rel}: Tier 2 row should read '{want}'"]


def audit_domains(write: bool) -> list[str]:
    """Regenerate the per-domain checklists and count table in the audit file."""
    rel = "MASO-CONTROL-AUDIT.md"
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    new = text
    controls = maso_controls()
    for name, prefix, _ in DOMAINS:
        items = controls[prefix]
        body = "\n".join(f"- [ ] **{i}** {t}" for i, t, _ in items)
        section = re.compile(rf"## {re.escape(name)} \({prefix}\) — \d+\n\n.*?(?=\n\n## )", re.S)
        new = section.sub(lambda _m: f"## {name} ({prefix}) — {len(items)}\n\n{body}", new)
        new = re.sub(
            rf"(\| {re.escape(name)} \| {prefix} \| )\d+( \|)",
            lambda m: f"{m.group(1)}{len(items)}{m.group(2)}",
            new,
        )
    if new == text:
        return []
    if write:
        path.write_text(new, encoding="utf-8")
    return [f"{rel}: domain checklists or counts are out of date"]


def broken_readme_links() -> list[str]:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    out = []
    for target in re.findall(r"\]\((?!https?://|mailto:|#)([^)#\s]+)", text):
        if not (ROOT / target).exists():
            out.append(f"README.md: link target does not exist: {target}")
    return sorted(set(out))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = ap.parse_args()

    f = facts()
    problems = audit_domains(args.write) + apply_rules(f, args.write) + tier2_cumulative(f, args.write)
    links = broken_readme_links()

    print("Derived figures: " + ", ".join(f"{k}={v}" for k, v in f.items()))
    if args.write:
        for p in problems:
            print(f"fixed: {p}")
        for p in links:
            print(f"needs a manual fix: {p}")
        return 1 if links else 0
    for p in problems + links:
        print(p)
    if problems:
        print("\nRun: python .github/scripts/readme_facts.py --write")
    return 1 if problems or links else 0


if __name__ == "__main__":
    sys.exit(main())

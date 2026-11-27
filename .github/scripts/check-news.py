#!/usr/bin/env python3
"""Fail if any news item is missing its MASO verdict block or cites an unknown control.

Uses the same parser as the MkDocs hook (hooks/news.py), so what passes here is
what the home page, control pages, and feed will render.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "hooks"))

import news  # noqa: E402


def main() -> int:
    docs = ROOT / "docs"
    items = news.parse_news((docs / "news.md").read_text(encoding="utf-8"))
    pages, _ = news.index_controls(docs)
    problems = news.validate(items, pages)
    for problem in problems:
        print(f"ERROR: {problem}")
    if not problems:
        print(f"OK: {len(items)} news items, all with verdicts. {news.scoreline(items)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

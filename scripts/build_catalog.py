#!/usr/bin/env python3
"""Regenerate the machine-readable control catalog.

controls.yaml holds the catalog data. This script recomputes the derived
fields (per-domain control_count, total_controls, the count in the
description) and writes controls.yaml and controls.json in the exact
published format, so both stay identical and byte-stable.

Usage:
  python3 scripts/build_catalog.py           # rewrite both files
  python3 scripts/build_catalog.py --check   # exit 1 if either is stale

After regenerating, copy both files to aisecuredbydesign.io at
docs/infrastructure/catalog/ so the two sites stay byte-identical.
"""
import json
import pathlib
import re
import sys

import yaml

CATALOG = pathlib.Path(__file__).resolve().parent.parent / "docs/infrastructure/catalog"
YAML_PATH = CATALOG / "controls.yaml"
JSON_PATH = CATALOG / "controls.json"


def build() -> tuple[str, str]:
    raw = YAML_PATH.read_text(encoding="utf-8")
    header = "".join(line for line in raw.splitlines(True) if line.startswith("#"))
    data = yaml.safe_load(raw)

    total = 0
    for domain in data["domains"]:
        domain["control_count"] = len(domain["controls"])
        total += domain["control_count"]
    data["total_controls"] = total
    data["description"] = re.sub(
        r"catalog of the \d+ infrastructure controls",
        f"catalog of the {total} infrastructure controls",
        data["description"],
    )

    ids = [c["id"] for d in data["domains"] for c in d["controls"]]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        sys.exit(f"duplicate control IDs: {sorted(dupes)}")

    out_yaml = header + yaml.dump(data, sort_keys=False, width=100, allow_unicode=True)
    out_json = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    return out_yaml, out_json


def main() -> int:
    out_yaml, out_json = build()
    if "--check" in sys.argv:
        stale = [
            p.name
            for p, text in ((YAML_PATH, out_yaml), (JSON_PATH, out_json))
            if p.read_text(encoding="utf-8") != text
        ]
        if stale:
            print(f"Catalog out of date: {', '.join(stale)}. Run scripts/build_catalog.py.")
            return 1
        print("Catalog up to date.")
        return 0
    YAML_PATH.write_text(out_yaml, encoding="utf-8")
    JSON_PATH.write_text(out_json, encoding="utf-8")
    print("Catalog regenerated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

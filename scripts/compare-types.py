#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import xml.etree.ElementTree as ET
from pathlib import Path


FIELDS = ("nominal", "min", "lifetime", "restock")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare DayZ types.xml entries by classname."
    )
    parser.add_argument("--legacy", type=Path, required=True)
    parser.add_argument("--vanilla", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/generated/types-comparison.csv"),
    )
    return parser.parse_args()


def load_types(path: Path) -> dict[str, dict[str, str]]:
    root = ET.parse(path).getroot()
    result: dict[str, dict[str, str]] = {}

    for type_node in root.findall("type"):
        name = type_node.get("name")

        if not name:
            continue

        result[name] = {
            field: (type_node.findtext(field) or "")
            for field in FIELDS
        }

    return result


def main() -> int:
    args = parse_args()

    legacy = load_types(args.legacy)
    vanilla = load_types(args.vanilla)

    args.output.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []

    for classname in sorted(set(legacy) | set(vanilla)):
        legacy_values = legacy.get(classname)
        vanilla_values = vanilla.get(classname)

        if legacy_values and vanilla_values:
            status = (
                "different"
                if legacy_values != vanilla_values
                else "identical"
            )
        elif legacy_values:
            status = "legacy_only"
        else:
            status = "vanilla_only"

        row = {
            "classname": classname,
            "status": status,
        }

        for field in FIELDS:
            row[f"legacy_{field}"] = (
                legacy_values[field] if legacy_values else ""
            )
            row[f"vanilla_{field}"] = (
                vanilla_values[field] if vanilla_values else ""
            )

        rows.append(row)

    fieldnames = [
        "classname",
        "status",
        *[
            column
            for field in FIELDS
            for column in (f"legacy_{field}", f"vanilla_{field}")
        ],
    ]

    with args.output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    counts = {
        status: sum(row["status"] == status for row in rows)
        for status in ("different", "identical", "legacy_only", "vanilla_only")
    }

    print(f"Entries checked: {len(rows)}")
    print(f"Different: {counts['different']}")
    print(f"Identical: {counts['identical']}")
    print(f"Legacy only: {counts['legacy_only']}")
    print(f"Vanilla only: {counts['vanilla_only']}")
    print(f"Report: {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

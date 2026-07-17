#!/usr/bin/env python3

from __future__ import annotations

import argparse
import difflib
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare legacy DayZ configuration files with a vanilla snapshot."
    )
    parser.add_argument(
        "--legacy",
        type=Path,
        default=Path("legacy"),
        help="Directory containing recovered legacy files.",
    )
    parser.add_argument(
        "--vanilla",
        type=Path,
        required=True,
        help="Root directory of the vanilla mission snapshot.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/generated/legacy-vs-vanilla"),
        help="Directory where comparison reports will be written.",
    )
    return parser.parse_args()


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8-sig").splitlines(keepends=True)


def find_vanilla_matches(vanilla_root: Path, filename: str) -> list[Path]:
    return sorted(
        path
        for path in vanilla_root.rglob(filename)
        if path.is_file()
    )


def main() -> int:
    args = parse_args()

    if not args.legacy.is_dir():
        raise SystemExit(f"Legacy directory not found: {args.legacy}")

    if not args.vanilla.is_dir():
        raise SystemExit(f"Vanilla directory not found: {args.vanilla}")

    args.output.mkdir(parents=True, exist_ok=True)

    comparable_extensions = {".xml", ".json"}
    legacy_files = sorted(
        path
        for path in args.legacy.iterdir()
        if path.is_file() and path.suffix.lower() in comparable_extensions
    )

    identical: list[tuple[Path, Path]] = []
    different: list[tuple[Path, Path, int]] = []
    missing: list[Path] = []
    ambiguous: list[tuple[Path, list[Path]]] = []

    for legacy_file in legacy_files:
        matches = find_vanilla_matches(args.vanilla, legacy_file.name)

        if not matches:
            missing.append(legacy_file)
            continue

        if len(matches) > 1:
            ambiguous.append((legacy_file, matches))
            continue

        vanilla_file = matches[0]
        legacy_lines = read_lines(legacy_file)
        vanilla_lines = read_lines(vanilla_file)

        if legacy_lines == vanilla_lines:
            identical.append((legacy_file, vanilla_file))
            continue

        diff = list(
            difflib.unified_diff(
                vanilla_lines,
                legacy_lines,
                fromfile=str(vanilla_file),
                tofile=str(legacy_file),
            )
        )

        diff_path = args.output / f"{legacy_file.name}.diff"
        diff_path.write_text("".join(diff), encoding="utf-8")

        changed_lines = sum(
            1
            for line in diff
            if (line.startswith("+") or line.startswith("-"))
            and not line.startswith("+++")
            and not line.startswith("---")
        )

        different.append((legacy_file, vanilla_file, changed_lines))

    summary_path = args.output / "summary.md"

    summary_lines = [
        "# Legacy vs vanilla comparison\n\n",
        f"- Legacy directory: `{args.legacy}`\n",
        f"- Vanilla directory: `{args.vanilla}`\n",
        f"- Files checked: **{len(legacy_files)}**\n",
        f"- Different: **{len(different)}**\n",
        f"- Identical: **{len(identical)}**\n",
        f"- Missing vanilla equivalent: **{len(missing)}**\n",
        f"- Ambiguous matches: **{len(ambiguous)}**\n\n",
        "## Different files\n\n",
    ]

    if different:
        for legacy_file, vanilla_file, changed_lines in different:
            summary_lines.append(
                f"- `{legacy_file.name}` → `{vanilla_file.relative_to(args.vanilla)}` "
                f"({changed_lines} added/removed lines)\n"
            )
    else:
        summary_lines.append("- None\n")

    summary_lines.append("\n## Identical files\n\n")

    if identical:
        for legacy_file, vanilla_file in identical:
            summary_lines.append(
                f"- `{legacy_file.name}` → `{vanilla_file.relative_to(args.vanilla)}`\n"
            )
    else:
        summary_lines.append("- None\n")

    summary_lines.append("\n## Missing vanilla equivalents\n\n")

    if missing:
        for legacy_file in missing:
            summary_lines.append(f"- `{legacy_file.name}`\n")
    else:
        summary_lines.append("- None\n")

    summary_lines.append("\n## Ambiguous matches\n\n")

    if ambiguous:
        for legacy_file, matches in ambiguous:
            summary_lines.append(f"- `{legacy_file.name}`:\n")
            for match in matches:
                summary_lines.append(
                    f"  - `{match.relative_to(args.vanilla)}`\n"
                )
    else:
        summary_lines.append("- None\n")

    summary_path.write_text("".join(summary_lines), encoding="utf-8")

    print(f"Comparison complete: {len(legacy_files)} files checked.")
    print(f"Different: {len(different)}")
    print(f"Identical: {len(identical)}")
    print(f"Missing vanilla equivalent: {len(missing)}")
    print(f"Ambiguous matches: {len(ambiguous)}")
    print(f"Summary: {summary_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

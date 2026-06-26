"""Instructor aggregator — merges student JSON exports into CSV or Excel."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

_COLUMNS = [
    "alias",
    "exported_at",
    "app_version",
    "completed_count",
    "arcade_points",
    "sp_points",
    "streak_days",
    "last_active_date",
    "quiz_accuracy_pct",
    "badges",
    "mod1_done",
    "mod2_done",
    "mod3_done",
    "mod4_done",
    "mod5_done",
    "mod6_done",
]


def _parse_file(path: Path) -> dict | None:
    """Return a row dict from a student export JSON, or None on error."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"WARNING: skipping {path.name} — {exc}", file=sys.stderr)
        return None

    try:
        mod = data.get("module_completion", {})
        row = {
            "alias": data.get("alias", ""),
            "exported_at": data.get("exported_at", ""),
            "app_version": data.get("app_version", ""),
            "completed_count": data.get("completed_count", ""),
            "arcade_points": data.get("arcade_points", ""),
            "sp_points": data.get("sp_points", ""),
            "streak_days": data.get("streak_days", ""),
            "last_active_date": data.get("last_active_date", ""),
            "quiz_accuracy_pct": data.get("quiz_accuracy_pct", ""),
            "badges": ",".join(data.get("badges", [])),
            "mod1_done": mod.get("1", {}).get("done", ""),
            "mod2_done": mod.get("2", {}).get("done", ""),
            "mod3_done": mod.get("3", {}).get("done", ""),
            "mod4_done": mod.get("4", {}).get("done", ""),
            "mod5_done": mod.get("5", {}).get("done", ""),
            "mod6_done": mod.get("6", {}).get("done", ""),
        }
    except Exception as exc:
        print(f"WARNING: skipping {path.name} — malformed structure: {exc}", file=sys.stderr)
        return None

    return row


def _write_csv(rows: list[dict], output: Path) -> None:
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _write_xlsx(rows: list[dict], output: Path) -> None:
    try:
        import openpyxl
    except ImportError:
        print(
            "WARNING: openpyxl not installed — falling back to CSV output.",
            file=sys.stderr,
        )
        output = output.with_suffix(".csv")
        _write_csv(rows, output)
        print(f"Saved CSV to {output}")
        return

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(_COLUMNS)
    for row in rows:
        ws.append([row.get(col, "") for col in _COLUMNS])
    wb.save(output)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Aggregate student progress JSON exports into CSV/Excel."
    )
    parser.add_argument("directory", type=Path, help="Directory containing *.json exports")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output file path")
    args = parser.parse_args(argv)

    exports_dir: Path = args.directory
    if not exports_dir.is_dir():
        print(f"ERROR: {exports_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    json_files = sorted(exports_dir.glob("*.json"))
    if not json_files:
        print(f"No *.json files found in {exports_dir}", file=sys.stderr)
        sys.exit(0)

    rows = []
    for path in json_files:
        row = _parse_file(path)
        if row is not None:
            rows.append(row)

    if not rows:
        print("No valid export files found.", file=sys.stderr)
        sys.exit(1)

    output: Path = args.output or exports_dir / "class_summary.csv"
    if output.suffix.lower() == ".xlsx":
        _write_xlsx(rows, output)
    else:
        _write_csv(rows, output)
        print(f"Saved {len(rows)} rows to {output}")


if __name__ == "__main__":
    main()

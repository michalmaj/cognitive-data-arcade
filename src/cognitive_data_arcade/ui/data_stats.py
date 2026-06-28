# src/cognitive_data_arcade/ui/data_stats.py
from __future__ import annotations

import csv
from pathlib import Path


def compute_data_stats(generated_dir: Path) -> dict[str, int]:
    """Return session, data_point, and active_day counts from CSV files."""
    if not generated_dir.exists():
        return {"sessions": 0, "data_points": 0, "active_days": 0}

    csv_files = list(generated_dir.rglob("*.csv"))
    sessions = len(csv_files)

    data_points = 0
    dates: set[str] = set()
    for f in csv_files:
        # Count unique days from filename prefix YYYYMMDD_HHMMSS
        name = f.stem
        if len(name) >= 8 and name[:8].isdigit():
            dates.add(name[:8])
        try:
            with f.open(newline="", encoding="utf-8") as fh:
                rows = sum(1 for _ in csv.reader(fh)) - 1
                data_points += max(0, rows)
        except (OSError, csv.Error):
            pass

    return {"sessions": sessions, "data_points": data_points, "active_days": len(dates)}


def compute_quiz_accuracy(quiz_results: dict[str, bool]) -> int | None:
    """Return quiz accuracy as 0-100 int, or None if no results."""
    total = len(quiz_results)
    if total == 0:
        return None
    correct = sum(1 for v in quiz_results.values() if v)
    return round(100 * correct / total)

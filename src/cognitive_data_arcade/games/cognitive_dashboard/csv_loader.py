from __future__ import annotations

import csv
from pathlib import Path

from cognitive_data_arcade.games.cognitive_dashboard.session import DashboardSession, TaskResult

_MAX_TRIALS = 500


def _load_task(
    data_root: Path, folder: str, rt_col: str, correct_col: str, condition_col: str
) -> TaskResult | None:
    """Read all CSVs from a task folder, combine into one TaskResult."""
    task_dir = data_root / folder
    if not task_dir.exists():
        return None

    rt_ms: list[float] = []
    correct: list[bool] = []
    condition: list[str] = []

    for csv_path in sorted(task_dir.glob("*.csv")):
        try:
            with csv_path.open(newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    try:
                        rt = float(row[rt_col])
                        ok = row[correct_col].strip().lower() in ("true", "1", "yes")
                        cond = row.get(condition_col, "unknown").strip()
                        rt_ms.append(rt)
                        correct.append(ok)
                        condition.append(cond)
                    except (KeyError, ValueError):
                        continue
        except OSError:
            continue

    if not rt_ms:
        return None

    # Keep most recent trials if data is very large
    if len(rt_ms) > _MAX_TRIALS:
        rt_ms = rt_ms[-_MAX_TRIALS:]
        correct = correct[-_MAX_TRIALS:]
        condition = condition[-_MAX_TRIALS:]

    return TaskResult(rt_ms=rt_ms, correct=correct, condition=condition)


def load_session_from_csv(data_root: Path) -> DashboardSession:
    """Build a DashboardSession from all saved CSV files on disk."""
    rt = _load_task(data_root, "reaction_time", "reaction_time_ms", "correct", "condition")
    stroop = _load_task(data_root, "stroop", "reaction_time_ms", "correct", "condition")
    flanker = _load_task(data_root, "flanker", "reaction_time_ms", "correct", "condition")
    gonogo = _load_task(data_root, "gono", "reaction_time_ms", "correct", "trial_type")
    return DashboardSession(rt=rt, stroop=stroop, flanker=flanker, gonogo=gonogo, synthetic=False)


def has_any_csv_data(data_root: Path) -> bool:
    """Return True if at least one game has saved CSV data."""
    for folder in ("reaction_time", "stroop", "flanker", "gono"):
        d = data_root / folder
        if d.exists() and any(d.glob("*.csv")):
            return True
    return False

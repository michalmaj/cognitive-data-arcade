from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class TrialResult:
    """Canonical trial record matching the minimal CSV schema from CLAUDE.md.

    Individual games may use richer game-specific dataclasses and pass them
    directly to write_trial(); this class is kept for reference and for code
    that wants the minimal common schema.
    """

    participant_id: str
    session_id: str
    trial_id: int
    task_name: str
    condition: str
    stimulus: str
    expected_response: str
    actual_response: str
    correct: bool
    reaction_time_ms: float
    timestamp: str


def write_trial(path: Path, trial: object) -> None:
    """Append one trial dataclass record to path.

    Creates the parent directory and writes the CSV header automatically on
    the first call.  Works with any frozen or non-frozen dataclass; the column
    order matches the field declaration order of the dataclass.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        row = asdict(trial)  # type: ignore[call-overload]
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if write_header:
            writer.writeheader()
        writer.writerow(row)


class CSVLogger:
    """Auto-pathing logger that derives file path from task_name + session_id."""

    def __init__(self, base_dir: Path) -> None:
        self._base_dir = base_dir

    def log_trial(self, trial: TrialResult) -> None:
        path = self._session_path(trial.task_name, trial.session_id)
        write_trial(path, trial)

    def _session_path(self, task_name: str, session_id: str) -> Path:
        return self._base_dir / task_name / f"{session_id}.csv"

import csv
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class TrialResult:
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


class CSVLogger:
    def __init__(self, base_dir: Path) -> None:
        self._base_dir = base_dir

    def log_trial(self, trial: TrialResult) -> None:
        path = self._session_path(trial.task_name, trial.session_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        write_header = not path.exists()
        with path.open("a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(asdict(trial).keys()))
            if write_header:
                writer.writeheader()
            writer.writerow(asdict(trial))

    def _session_path(self, task_name: str, session_id: str) -> Path:
        return self._base_dir / task_name / f"{session_id}.csv"

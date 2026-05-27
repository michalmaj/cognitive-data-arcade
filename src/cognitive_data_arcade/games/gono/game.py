from __future__ import annotations

import csv
import enum
import random
from dataclasses import asdict, dataclass
from pathlib import Path

from cognitive_data_arcade.games.gono.config import GoNoGoConfig


class _Phase(enum.Enum):
    ITI = "iti"
    FIXATION = "fixation"
    STIMULUS = "stimulus"
    FEEDBACK = "feedback"
    BETWEEN_BLOCKS = "between_blocks"
    DONE = "done"


@dataclass(frozen=True)
class _TrialRecord:
    participant_id: str
    session_id: str
    trial_id: int
    task_name: str
    trial_type: str  # "go" / "nogo"
    response: str  # "hit" / "miss" / "false_alarm" / "correct_rejection"
    correct: bool
    reaction_time_ms: float  # 0.0 if no response
    timestamp: str  # ISO 8601


def _generate_trials(config: GoNoGoConfig) -> list[dict[str, str]]:
    num_blocks = config.num_trials // config.trials_per_block
    go_per_block = round(config.go_ratio * config.trials_per_block)
    nogo_per_block = config.trials_per_block - go_per_block
    trials: list[dict[str, str]] = []
    for _ in range(num_blocks):
        block: list[dict[str, str]] = [{"trial_type": "go"}] * go_per_block + [
            {"trial_type": "nogo"}
        ] * nogo_per_block
        random.shuffle(block)
        trials.extend(block)
    return trials


def _write_trial(csv_path: Path, record: _TrialRecord) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(record).keys()))
        if write_header:
            writer.writeheader()
        writer.writerow(asdict(record))

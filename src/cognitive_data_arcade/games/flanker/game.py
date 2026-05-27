# src/cognitive_data_arcade/games/flanker/game.py
from __future__ import annotations

import csv
import datetime  # noqa: F401
import enum  # noqa: F401
import random
from dataclasses import asdict, dataclass
from pathlib import Path

import pygame  # noqa: F401

from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult  # noqa: F401
from cognitive_data_arcade.engine.i18n import Strings  # noqa: F401
from cognitive_data_arcade.engine.scene import Scene  # noqa: F401
from cognitive_data_arcade.games.flanker.config import FlankerConfig
from cognitive_data_arcade.profile.manager import ProfileManager  # noqa: F401

_BG = (10, 10, 20)
_WHITE = (240, 240, 240)
_DIM = (70, 70, 112)
_ORANGE = (243, 156, 18)
_RED = (231, 76, 60)
_GREEN = (39, 174, 96)
_W, _H = 1024, 768


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
    condition: str
    target_direction: str
    correct: bool
    reaction_time_ms: float
    timestamp: str


def _generate_trials(config: FlankerConfig) -> list[dict]:
    per_combo = config.num_trials // 4
    trials: list[dict] = []
    for condition in ("congruent", "incongruent"):
        for direction in ("left", "right"):
            for _ in range(per_combo):
                trials.append({"condition": condition, "target_direction": direction})
    random.shuffle(trials)
    return trials


def _write_trial(path: Path, record: _TrialRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(record).keys()))
        if write_header:
            writer.writeheader()
        writer.writerow(asdict(record))

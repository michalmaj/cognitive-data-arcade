from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

HintsMode = Literal["always", "toggle", "none"]


@dataclass(frozen=True)
class DifficultyConfig:
    rows: int
    errors_min: int
    errors_max: int
    hints_mode: HintsMode


EASY = DifficultyConfig(rows=15, errors_min=3, errors_max=6, hints_mode="always")
MEDIUM = DifficultyConfig(rows=50, errors_min=15, errors_max=20, hints_mode="toggle")
HARD = DifficultyConfig(rows=100, errors_min=25, errors_max=40, hints_mode="none")

ALL_DIFFICULTIES: list[DifficultyConfig] = [EASY, MEDIUM, HARD]

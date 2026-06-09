# src/cognitive_data_arcade/games/visual_search/config.py
from __future__ import annotations

from dataclasses import dataclass, field

FIXATION_MS: int = 500
FEEDBACK_MS: int = 400
ITI_MS: int = 300
TIMEOUT_MS: int = 5000
BLOCK_BREAK_MS: int = 2000

SET_SIZES: dict[str, int] = {"easy": 8, "medium": 16, "hard": 24}
TRIALS_PER_BLOCK: dict[str, int] = {"easy": 16, "medium": 24, "hard": 36}


@dataclass(frozen=True)
class VSConfig:
    mode: str         # "letters" | "shapes"
    difficulty: str   # "easy" | "medium" | "hard"
    set_size: int = field(init=False)
    trials_per_block: int = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "set_size", SET_SIZES[self.difficulty])
        object.__setattr__(self, "trials_per_block", TRIALS_PER_BLOCK[self.difficulty])

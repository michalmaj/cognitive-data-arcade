from __future__ import annotations

from dataclasses import dataclass

import pygame

COLORS: list[tuple[str, str, tuple[int, int, int], int]] = [
    ("CZERWONY", "red", (231, 76, 60), pygame.K_r),
    ("ZIELONY", "green", (39, 174, 96), pygame.K_g),
    ("NIEBIESKI", "blue", (41, 128, 185), pygame.K_b),
    ("ŻÓŁTY", "yellow", (243, 156, 18), pygame.K_y),
]


@dataclass(frozen=True)
class StroopConfig:
    num_trials: int = 36
    trials_per_block: int = 36
    num_colors: int = 3
    iti_min_ms: int = 800
    iti_max_ms: int = 1500
    feedback_duration_ms: int = 600
    timeout_ms: int = 3000
    ap_per_correct: int = 2


EASY = StroopConfig(num_colors=2, num_trials=36, trials_per_block=36)
MEDIUM = StroopConfig(num_colors=3, num_trials=36, trials_per_block=36)
HARD = StroopConfig(num_colors=4, num_trials=36, trials_per_block=36)
STANDARD = MEDIUM  # alias — menu.py unchanged

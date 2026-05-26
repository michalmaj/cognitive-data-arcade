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
    num_trials: int = 60
    trials_per_block: int = 30
    iti_min_ms: int = 800
    iti_max_ms: int = 1500
    feedback_duration_ms: int = 600
    timeout_ms: int = 3000
    ap_per_correct: int = 2


QUICK = StroopConfig(num_trials=36, trials_per_block=18)
STANDARD = StroopConfig(num_trials=60, trials_per_block=30)
FULL = StroopConfig(num_trials=96, trials_per_block=32)

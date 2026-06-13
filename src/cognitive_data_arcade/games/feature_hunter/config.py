from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class DifficultyConfig:
    name_pl: str
    card_count: int
    timer_s: float | None       # None = no timer
    hints: str                  # "full" | "scatter_only" | "none"
    time_bonus_per_5s: int
    min_signal_correlation: float   # abs(r) threshold for signal features
    max_noise_correlation: float    # abs(r) threshold for noise features


EASY = DifficultyConfig(
    name_pl="Latwy",
    card_count=4,
    timer_s=None,
    hints="full",
    time_bonus_per_5s=0,
    min_signal_correlation=0.60,
    max_noise_correlation=0.10,
)

MEDIUM = DifficultyConfig(
    name_pl="Sredni",
    card_count=6,
    timer_s=45.0,
    hints="scatter_only",
    time_bonus_per_5s=1,
    min_signal_correlation=0.30,
    max_noise_correlation=0.15,
)

HARD = DifficultyConfig(
    name_pl="Trudny",
    card_count=8,
    timer_s=20.0,
    hints="none",
    time_bonus_per_5s=2,
    min_signal_correlation=0.20,
    max_noise_correlation=0.20,
)

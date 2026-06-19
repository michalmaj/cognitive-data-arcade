from __future__ import annotations

import random
from dataclasses import dataclass, field

CATEGORIES: list[str] = ["SPORT", "POLITYKA", "NAUKA", "MUZYKA", "MODA"]

ENGAGEMENT: dict[str, int] = {
    "SPORT":    120,
    "POLITYKA":  40,
    "NAUKA":     25,
    "MUZYKA":    20,
    "MODA":      15,
}

CAT_COLORS: dict[str, tuple[int, int, int]] = {
    "SPORT":    (231, 76, 60),
    "POLITYKA": (52, 152, 219),
    "NAUKA":    (46, 204, 113),
    "MUZYKA":   (243, 156, 18),
    "MODA":     (233, 30, 140),
}

BubbleProfile = dict[str, float]


def uniform_profile() -> BubbleProfile:
    return {cat: 1.0 / len(CATEGORIES) for cat in CATEGORIES}


def diversity(profile: BubbleProfile) -> float:
    """1 - max(weights). 0 = monopoly, ~0.8 = equal split."""
    return 1.0 - max(profile.values())


def profile_from_clicks(clicks: dict[str, int]) -> BubbleProfile:
    total = sum(clicks.values())
    if total == 0:
        return uniform_profile()
    return {cat: clicks.get(cat, 0) / total for cat in CATEGORIES}


def curated_profile(slots: list[str]) -> BubbleProfile:
    counts = {cat: slots.count(cat) for cat in CATEGORIES}
    total = len(slots)
    return {cat: counts[cat] / total for cat in CATEGORIES}


def generate_slots(
    profile: BubbleProfile, n: int = 6, seed: int | None = None
) -> list[str]:
    rng = random.Random(seed)
    return rng.choices(list(profile.keys()), weights=list(profile.values()), k=n)


@dataclass
class GameState:
    bubble: BubbleProfile = field(default_factory=uniform_profile)
    score_curator: int = 0
    score_algo: int = 0
    diversity_act1: float = 0.0
    diversity_act2: float = 0.0
    diversity_act3: float = 0.0
    algo_clicked_cats: list[str] = field(default_factory=list)
    curator_slots: list[str] = field(default_factory=list)

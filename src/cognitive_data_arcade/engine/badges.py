from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from cognitive_data_arcade.profile.manager import Profile


@dataclass(frozen=True)
class SessionResult:
    task_name: str
    participant_id: str
    session_id: str
    total_trials: int
    correct_trials: int
    avg_reaction_time_ms: float
    min_reaction_time_ms: float
    max_reaction_time_ms: float
    arcade_points_earned: int
    science_points_earned: int

    @property
    def accuracy(self) -> float:
        if self.total_trials == 0:
            return 0.0
        return self.correct_trials / self.total_trials


@dataclass(frozen=True)
class Badge:
    badge_id: str
    icon: str
    name_en: str
    name_pl: str
    check: Callable[[SessionResult, Profile], bool]


def _check_quick_reflex(session: SessionResult, profile: Profile) -> bool:
    return session.avg_reaction_time_ms < 250.0 and session.accuracy >= 0.8


def _check_sharpshooter(session: SessionResult, profile: Profile) -> bool:
    return session.accuracy == 1.0 and session.total_trials >= 10


def _check_three_in_a_row(session: SessionResult, profile: Profile) -> bool:
    return session.correct_trials >= 3 and session.accuracy >= 0.9


def _check_clean_data(session: SessionResult, profile: Profile) -> bool:
    return session.science_points_earned > 0


def _check_first_game(session: SessionResult, profile: Profile) -> bool:
    return profile.arcade_points == 0


BADGE_REGISTRY: list[Badge] = [
    Badge("quick_reflex", "⚡", "Quick Reflex", "Błyskawiczny", _check_quick_reflex),
    Badge("sharpshooter", "🎯", "Sharpshooter", "Snajper", _check_sharpshooter),
    Badge(
        "three_in_a_row", "🔁", "Three in a Row", "Trzy z Rzędu", _check_three_in_a_row
    ),
    Badge("clean_data", "🧹", "Clean Data", "Czyste Dane", _check_clean_data),
    Badge("first_game", "🎮", "First Game", "Pierwsza Gra", _check_first_game),
]


class BadgeEngine:
    def __init__(self, registry: list[Badge] | None = None) -> None:
        self._registry = registry if registry is not None else BADGE_REGISTRY

    def evaluate(self, session: SessionResult, profile: Profile) -> list[str]:
        """Return badge_ids newly earned this session (not already in profile.badges)."""
        return [
            badge.badge_id
            for badge in self._registry
            if badge.badge_id not in profile.badges and badge.check(session, profile)
        ]

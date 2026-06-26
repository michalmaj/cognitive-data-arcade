from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pygame

from cognitive_data_arcade.profile.manager import Profile


# ── Session achievement badges (in-game scoring) ─────────────────────────────


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

    def __post_init__(self) -> None:
        if self.correct_trials > self.total_trials:
            raise ValueError(
                f"correct_trials ({self.correct_trials}) > total_trials ({self.total_trials})"
            )

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


def _check_high_accuracy(session: SessionResult, profile: Profile) -> bool:
    return session.correct_trials >= 3 and session.accuracy >= 0.9


def _check_clean_data(session: SessionResult, profile: Profile) -> bool:
    return session.science_points_earned > 0


def _check_first_game(session: SessionResult, profile: Profile) -> bool:
    return profile.arcade_points == 0


BADGE_REGISTRY: list[Badge] = [
    Badge("quick_reflex", "⚡", "Quick Reflex", "Błyskawiczny", _check_quick_reflex),
    Badge("sharpshooter", "🎯", "Sharpshooter", "Snajper", _check_sharpshooter),
    Badge("high_accuracy", "🎯", "High Accuracy", "Wysoka Celność", _check_high_accuracy),
    Badge("clean_data", "🧹", "Clean Data", "Czyste Dane", _check_clean_data),
    Badge("first_game", "🎮", "First Game", "Pierwsza Gra", _check_first_game),
]


BADGE_ICONS: dict[str, str] = {
    "quick_reflex": "badge_quick_reflex.png",
    "sharpshooter": "badge_sharpshooter.png",
    "high_accuracy": "badge_high_accuracy.png",
    "clean_data": "badge_clean_data.png",
    "first_game": "badge_first_game.png",
}


class BadgeEngine:
    def __init__(self, registry: list[Badge] | None = None) -> None:
        self._registry: tuple[Badge, ...] = tuple(
            registry if registry is not None else BADGE_REGISTRY
        )

    def evaluate(self, session: SessionResult, profile: Profile) -> list[str]:
        """Return badge_ids newly earned this session (not already in profile.badges).

        Must be called with the profile state BEFORE adding session points.
        The first_game badge checks profile.arcade_points == 0; calling this
        after ProfileManager.add_ap() will cause first_game to never trigger.
        """
        return [
            badge.badge_id
            for badge in self._registry
            if badge.badge_id not in profile.badges and badge.check(session, profile)
        ]


# ── Module completion badges (PNG icons, lesson-progress based) ───────────────

_ASSET_DIR = Path("assets") / "badges"

_MODULE_LESSONS: list[list[int]] = [
    [1, 2, 3, 4, 6],  # Module 1 -- Data & Cognition Basics
    [7, 8, 9, 10, 11, 12],  # Module 2 -- Cognitive Experiments
    [13, 14, 15, 16],  # Module 3 -- Statistics
    [17, 18, 19, 20],  # Module 4 -- Machine Learning
    [21, 22, 23, 24, 25, 26],  # Module 5 -- Language & NLP
    [27, 28, 29, 30, 31, 32],  # Module 6 -- Networks, Ethics & Finale
]
_ALL_LESSONS: list[int] = [n for group in _MODULE_LESSONS for n in group]


@dataclass(frozen=True)
class ModuleBadge:
    id: str
    icon_file: str
    name_pl: str
    name_en: str
    module_idx: int | None


_MODULE_BADGES: list[ModuleBadge] = [
    ModuleBadge("mod_1", "module_1_data_cognition.png", "Podstawy Danych", "Data Basics", 0),
    ModuleBadge(
        "mod_2", "module_2_cognitive_science.png", "Eksperymenty Kogn.", "Cognitive Science", 1
    ),
    ModuleBadge("mod_3", "module_3_statistics.png", "Statystyka", "Statistics", 2),
    ModuleBadge(
        "mod_4", "module_4_machine_learning.png", "Machine Learning", "Machine Learning", 3
    ),
    ModuleBadge("mod_5", "module_5_nlp.png", "Jezyk i NLP", "Language & NLP", 4),
    ModuleBadge("mod_6", "module_6_networks_ethics.png", "Sieci i Etyka", "Networks & Ethics", 5),
]
_SPECIAL_BADGES: list[ModuleBadge] = [
    ModuleBadge("first", "badge_first_lesson.png", "Pierwsze kroki", "First Steps", None),
    ModuleBadge("all_done", "badge_all_done.png", "Kompletny", "Complete", None),
]
_STREAK_BADGES: list[ModuleBadge] = [
    ModuleBadge("streak_3", "badge_streak_3.png", "3 dni z rzędu", "3-day streak", None),
    ModuleBadge("streak_7", "badge_streak_7.png", "Tygodniowy", "Weekly ritual", None),
    ModuleBadge("streak_30", "badge_streak_30.png", "Miesięczny", "Monthly habit", None),
]
ALL_MODULE_BADGES: list[ModuleBadge] = _MODULE_BADGES + _SPECIAL_BADGES + _STREAK_BADGES


def earned_badges(completed: set[int]) -> list[ModuleBadge]:
    result: list[ModuleBadge] = []
    for badge in _MODULE_BADGES:
        required = _MODULE_LESSONS[badge.module_idx]  # type: ignore[index]
        if all(n in completed for n in required):
            result.append(badge)
    if completed:
        result.append(_SPECIAL_BADGES[0])  # first lesson
    if all(n in completed for n in _ALL_LESSONS):
        result.append(_SPECIAL_BADGES[1])  # all done
    return result


def module_complete(module_idx: int, completed: set[int]) -> bool:
    return all(n in completed for n in _MODULE_LESSONS[module_idx])


_icon_cache: dict[str, pygame.Surface] = {}


def load_icon(icon_file: str, size: int = 32) -> pygame.Surface | None:
    """Load any PNG from assets/badges/ by filename, with LRU-style cache."""
    if not icon_file:
        return None
    key = f"{icon_file}:{size}"
    if key in _icon_cache:
        return _icon_cache[key]
    path = _ASSET_DIR / icon_file
    if not path.exists():
        return None
    try:
        raw = pygame.image.load(str(path)).convert_alpha()
        scaled = pygame.transform.smoothscale(raw, (size, size))
        _icon_cache[key] = scaled
        return scaled
    except pygame.error:
        return None


def load_badge_icon(badge: ModuleBadge, size: int = 32) -> pygame.Surface | None:
    return load_icon(badge.icon_file, size)


def tint_surface(surf: pygame.Surface, color: tuple[int, int, int]) -> pygame.Surface:
    tinted = surf.copy()
    tinted.fill((*color, 255), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted

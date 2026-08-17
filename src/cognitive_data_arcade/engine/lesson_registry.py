"""Canonical lesson registry for Cognitive Data Arcade.

This module is the single source of truth for lesson metadata:
lesson numbers, slugs, display titles, and lesson kinds.

Game construction is handled separately in ui/game_launcher.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LessonKind(Enum):
    """Classification of a lesson by its interactive component.

    PLAYABLE: the lesson has a runnable game or interactive scene.
    THEORY:   the lesson has educational content but no playable component.
    HIDDEN:   the lesson exists internally but is not shown in the UI
              (e.g. its content is subsumed by another lesson).
    """

    PLAYABLE = "playable"
    THEORY = "theory"
    HIDDEN = "hidden"


@dataclass(frozen=True)
class LessonSpec:
    """Immutable description of one lesson.

    Attributes:
        number:   Lesson number (1-based, matches course README numbering).
        slug:     Machine-readable identifier, matches the task_name used in
                  CSV logs and SessionResult (e.g. "reaction_time", "stroop").
        title_en: English display title shown in the menu.
        kind:     Whether the lesson is playable, theory-only, or hidden.
    """

    number: int
    slug: str
    title_en: str
    kind: LessonKind


_AVAILABLE = frozenset(range(1, 33))  # lesson_01 … lesson_32 all ship with v0.9.0


def lesson_available(lesson_num: int) -> bool:
    """Check if a lesson number is available.

    Args:
        lesson_num: The lesson number to check (1-32 are available in v0.9.0).

    Returns:
        True if the lesson is available, False otherwise.
    """
    return lesson_num in _AVAILABLE

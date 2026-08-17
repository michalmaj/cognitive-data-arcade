"""Regression guard: every PLAYABLE lesson in LESSON_REGISTRY must have
a corresponding game factory in game_launcher.game_factory_for().

This test will fail in PR #3 if a lesson is marked PLAYABLE but its
factory branch is accidentally removed. Keep it alive through the
launcher consolidation.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from cognitive_data_arcade.engine.lesson_registry import LESSON_REGISTRY, LessonKind
from cognitive_data_arcade.ui.game_launcher import game_factory_for

_PLAYABLE = [ls for ls in LESSON_REGISTRY if ls.kind == LessonKind.PLAYABLE]


@pytest.mark.parametrize("spec", _PLAYABLE, ids=lambda s: f"L{s.number:02d}_{s.slug}")
def test_playable_lesson_has_game_factory(spec):
    pm = MagicMock()
    strings = MagicMock()
    factory = game_factory_for(spec.number, pm, strings)
    assert factory is not None, (
        f"Lesson {spec.number} ({spec.slug}) is PLAYABLE in LESSON_REGISTRY "
        f"but game_factory_for({spec.number}, ...) returned None"
    )
    assert callable(factory), (
        f"game_factory_for({spec.number}, ...) must return a callable, got {type(factory)}"
    )

from __future__ import annotations

import pytest

from cognitive_data_arcade.engine.lesson_registry import lesson_available


# ── lesson_available (current contract before registry refactor) ──────────────


def test_known_lesson_available():
    assert lesson_available(1) is True
    assert lesson_available(32) is True


def test_unknown_lesson_not_available():
    assert lesson_available(0) is False
    assert lesson_available(33) is False


def test_lesson_5_available():
    # L05 exists (theory content in lesson_05.py) even though absent from the menu
    assert lesson_available(5) is True


@pytest.mark.parametrize("num", range(1, 33))
def test_all_lessons_1_to_32_available(num: int):
    assert lesson_available(num) is True

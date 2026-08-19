from __future__ import annotations

import pytest

from cognitive_data_arcade.engine.lesson_registry import (
    LESSON_REGISTRY,
    LessonKind,
    LessonSpec,
    get_lesson,
    lesson_available,
)

# ── lesson_available ──────────────────────────────────────────────────────────


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


# ── LESSON_REGISTRY integrity ─────────────────────────────────────────────────


def test_registry_has_32_entries():
    assert len(LESSON_REGISTRY) == 32


def test_registry_numbers_are_unique():
    nums = [ls.number for ls in LESSON_REGISTRY]
    assert len(nums) == len(set(nums)), "Duplicate lesson numbers found"


def test_registry_slugs_are_unique():
    slugs = [ls.slug for ls in LESSON_REGISTRY]
    assert len(slugs) == len(set(slugs)), "Duplicate slugs found"


def test_registry_covers_exactly_1_to_32():
    nums = {ls.number for ls in LESSON_REGISTRY}
    assert nums == set(range(1, 33))


def test_registry_ordered_by_number():
    nums = [ls.number for ls in LESSON_REGISTRY]
    assert nums == sorted(nums), "LESSON_REGISTRY must be ordered by lesson number"


def test_lesson_5_is_hidden():
    spec = get_lesson(5)
    assert spec is not None
    assert spec.kind == LessonKind.HIDDEN
    assert spec.slug == "missing_values"


def test_get_lesson_known():
    spec = get_lesson(1)
    assert isinstance(spec, LessonSpec)
    assert spec.number == 1
    assert spec.slug == "big_data_map"
    assert spec.kind == LessonKind.PLAYABLE


def test_get_lesson_unknown_returns_none():
    assert get_lesson(0) is None
    assert get_lesson(33) is None


def test_all_specs_have_non_empty_fields():
    for ls in LESSON_REGISTRY:
        assert ls.slug, f"Empty slug for lesson {ls.number}"
        assert ls.title_en, f"Empty title_en for lesson {ls.number}"


def test_playable_lessons_are_majority():
    playable = [ls for ls in LESSON_REGISTRY if ls.kind == LessonKind.PLAYABLE]
    assert len(playable) == 31  # L05 is the only non-playable


def test_hidden_lessons_count():
    hidden = [ls for ls in LESSON_REGISTRY if ls.kind == LessonKind.HIDDEN]
    assert len(hidden) == 1
    assert hidden[0].number == 5

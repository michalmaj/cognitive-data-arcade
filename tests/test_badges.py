from __future__ import annotations

import pytest
from cognitive_data_arcade.engine.badges import (
    ALL_MODULE_BADGES,
    Badge,
    BadgeEngine,
    BADGE_REGISTRY,
    SessionResult,
    _ALL_LESSONS,
    _MODULE_LESSONS,
    earned_badges,
    module_complete,
)
from cognitive_data_arcade.profile.manager import Profile


# ── Session achievement badge tests ──────────────────────────────────────────


def _make_session(**kwargs) -> SessionResult:
    defaults = dict(
        task_name="reaction_time",
        participant_id="p1",
        session_id="s1",
        total_trials=20,
        correct_trials=18,
        avg_reaction_time_ms=280.0,
        min_reaction_time_ms=210.0,
        max_reaction_time_ms=380.0,
        arcade_points_earned=70,
        science_points_earned=0,
    )
    defaults.update(kwargs)
    return SessionResult(**defaults)


def _make_profile(**kwargs) -> Profile:
    defaults = dict(
        alias="tester",
        device_uuid="test-uuid",
        arcade_points=0,
        science_points=0,
        badges=[],
        completed_lessons=[],
    )
    defaults.update(kwargs)
    return Profile(**defaults)


def test_session_result_accuracy_full() -> None:
    s = _make_session(total_trials=10, correct_trials=10)
    assert s.accuracy == 1.0


def test_session_result_accuracy_partial() -> None:
    s = _make_session(total_trials=20, correct_trials=15)
    assert s.accuracy == 0.75


def test_session_result_accuracy_zero_trials() -> None:
    s = _make_session(total_trials=0, correct_trials=0)
    assert s.accuracy == 0.0


def test_badge_engine_returns_new_ids() -> None:
    session = _make_session(avg_reaction_time_ms=200.0, total_trials=20, correct_trials=20)
    profile = _make_profile(arcade_points=0)
    engine = BadgeEngine()
    new_ids = engine.evaluate(session, profile)
    assert "quick_reflex" in new_ids
    assert "sharpshooter" in new_ids
    assert "first_game" in new_ids


def test_badge_engine_skips_already_earned() -> None:
    session = _make_session(avg_reaction_time_ms=200.0, total_trials=20, correct_trials=20)
    profile = _make_profile(arcade_points=0, badges=["quick_reflex"])
    engine = BadgeEngine()
    new_ids = engine.evaluate(session, profile)
    assert "quick_reflex" not in new_ids


def test_badge_engine_no_badges_for_slow_session() -> None:
    session = _make_session(
        avg_reaction_time_ms=500.0,
        total_trials=10,
        correct_trials=5,
        arcade_points_earned=10,
    )
    profile = _make_profile(arcade_points=50, badges=["first_game"])
    engine = BadgeEngine()
    new_ids = engine.evaluate(session, profile)
    assert new_ids == []


def test_badge_engine_custom_registry() -> None:
    always_true = Badge(
        badge_id="test_badge",
        icon="T",
        name_en="Test",
        name_pl="Test",
        check=lambda s, p: True,
    )
    engine = BadgeEngine(registry=[always_true])
    profile = _make_profile()
    new_ids = engine.evaluate(_make_session(), profile)
    assert new_ids == ["test_badge"]


def test_badge_registry_has_five_entries() -> None:
    ids = {b.badge_id for b in BADGE_REGISTRY}
    assert ids == {"quick_reflex", "sharpshooter", "high_accuracy", "clean_data", "first_game"}


def test_first_game_badge_requires_zero_ap_before() -> None:
    session = _make_session()
    profile_new = _make_profile(arcade_points=0)
    profile_old = _make_profile(arcade_points=100)
    engine = BadgeEngine()
    assert "first_game" in engine.evaluate(session, profile_new)
    assert "first_game" not in engine.evaluate(session, profile_old)


def test_clean_data_badge_requires_sp() -> None:
    session_with_sp = _make_session(science_points_earned=50)
    session_no_sp = _make_session(science_points_earned=0)
    profile = _make_profile(arcade_points=100)
    engine = BadgeEngine()
    assert "clean_data" in engine.evaluate(session_with_sp, profile)
    assert "clean_data" not in engine.evaluate(session_no_sp, profile)


def test_high_accuracy_badge_condition() -> None:
    good = _make_session(total_trials=20, correct_trials=18)
    bad = _make_session(total_trials=20, correct_trials=10)
    profile = _make_profile(arcade_points=100)
    engine = BadgeEngine()
    assert "high_accuracy" in engine.evaluate(good, profile)
    assert "high_accuracy" not in engine.evaluate(bad, profile)


def test_session_result_rejects_more_correct_than_total() -> None:
    with pytest.raises(ValueError, match="correct_trials"):
        _make_session(total_trials=10, correct_trials=11)


# ── Module completion badge tests ─────────────────────────────────────────────


def test_all_badges_count():
    assert len(ALL_MODULE_BADGES) == 11  # 6 module + 2 special + 3 streak


def test_module_lessons_cover_all_31():
    assert len(_ALL_LESSONS) == 31


def test_earned_badges_empty_when_no_progress():
    badges = earned_badges(set())
    assert badges == []


def test_first_lesson_badge_any_completion():
    badges = earned_badges({1})
    ids = [b.id for b in badges]
    assert "first" in ids


def test_module_badge_earned_when_all_lessons_done():
    completed = set(_MODULE_LESSONS[0])
    badges = earned_badges(completed)
    ids = [b.id for b in badges]
    assert "mod_1" in ids


def test_module_badge_not_earned_when_partial():
    completed = set(_MODULE_LESSONS[0][:-1])  # all but last
    badges = earned_badges(completed)
    ids = [b.id for b in badges]
    assert "mod_1" not in ids


def test_all_done_badge_requires_all_lessons():
    badges = earned_badges(set(_ALL_LESSONS))
    ids = [b.id for b in badges]
    assert "all_done" in ids
    assert "first" in ids
    # all 6 module badges earned
    assert sum(1 for b in badges if b.id.startswith("mod_")) == 6


def test_all_done_badge_not_earned_when_partial():
    badges = earned_badges(set(_ALL_LESSONS[:-1]))
    ids = [b.id for b in badges]
    assert "all_done" not in ids


def test_module_complete_true():
    assert module_complete(0, set(_MODULE_LESSONS[0]))


def test_module_complete_false():
    partial = set(_MODULE_LESSONS[0][:-1])
    assert not module_complete(0, partial)


def test_badge_fields_non_empty():
    for b in ALL_MODULE_BADGES:
        assert b.id
        assert b.icon_file.endswith(".png")
        assert b.name_pl
        assert b.name_en

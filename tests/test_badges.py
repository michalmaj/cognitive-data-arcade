import pytest

from cognitive_data_arcade.engine.badges import (
    Badge,
    BadgeEngine,
    BADGE_REGISTRY,
    SessionResult,
)
from cognitive_data_arcade.profile.manager import Profile


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
    session = _make_session(
        avg_reaction_time_ms=200.0,
        total_trials=20,
        correct_trials=20,
    )
    profile = _make_profile(arcade_points=0)
    engine = BadgeEngine()
    new_ids = engine.evaluate(session, profile)
    assert "quick_reflex" in new_ids
    assert "sharpshooter" in new_ids
    assert "first_game" in new_ids


def test_badge_engine_skips_already_earned() -> None:
    session = _make_session(
        avg_reaction_time_ms=200.0, total_trials=20, correct_trials=20
    )
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
        icon="🧪",
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
    assert ids == {
        "quick_reflex",
        "sharpshooter",
        "high_accuracy",
        "clean_data",
        "first_game",
    }


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
    good = _make_session(total_trials=20, correct_trials=18)  # 90% accuracy, 18 >= 3
    bad = _make_session(total_trials=20, correct_trials=10)  # 50% accuracy
    profile = _make_profile(arcade_points=100)
    engine = BadgeEngine()
    assert "high_accuracy" in engine.evaluate(good, profile)
    assert "high_accuracy" not in engine.evaluate(bad, profile)


def test_session_result_rejects_more_correct_than_total() -> None:
    with pytest.raises(ValueError, match="correct_trials"):
        _make_session(total_trials=10, correct_trials=11)

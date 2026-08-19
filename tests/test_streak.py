import json
from datetime import date

import pytest

from cognitive_data_arcade.profile.manager import ProfileManager


@pytest.fixture
def pm(tmp_path):
    return ProfileManager(tmp_path / "profile.json")


def test_first_touch_sets_streak_to_1(pm):
    p = pm.touch_streak(date(2026, 6, 26))
    assert p.streak_days == 1
    assert p.last_active_date == "2026-06-26"


def test_same_day_touch_is_noop(pm):
    pm.touch_streak(date(2026, 6, 26))
    p = pm.touch_streak(date(2026, 6, 26))
    assert p.streak_days == 1


def test_consecutive_day_increments(pm):
    pm.touch_streak(date(2026, 6, 25))
    p = pm.touch_streak(date(2026, 6, 26))
    assert p.streak_days == 2


def test_gap_resets_streak(pm):
    pm.touch_streak(date(2026, 6, 20))
    p = pm.touch_streak(date(2026, 6, 26))
    assert p.streak_days == 1


def test_streak_badge_awarded_at_3(pm):
    pm.touch_streak(date(2026, 6, 24))
    pm.touch_streak(date(2026, 6, 25))
    p = pm.touch_streak(date(2026, 6, 26))
    assert p.streak_days == 3
    assert "streak_3" in p.badges


def test_streak_badge_not_duplicate(pm):
    for i in range(5):
        pm.touch_streak(date(2026, 6, 22 + i))
    p = pm.load()
    assert p.badges.count("streak_3") == 1


def test_streak_fields_persisted(pm):
    pm.touch_streak(date(2026, 6, 26))
    raw = json.loads((pm._path).read_text())
    assert raw["streak_days"] == 1
    assert raw["last_active_date"] == "2026-06-26"


def test_reset_all_clears_streak(pm):
    pm.touch_streak(date(2026, 6, 26))
    p = pm.reset_all()
    assert p.streak_days == 0
    assert p.last_active_date == ""

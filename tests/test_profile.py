from pathlib import Path

from cognitive_data_arcade.profile.manager import Profile, ProfileManager, level_title


def test_level_title_boundaries() -> None:
    assert level_title(0) == "🌱 Data Seedling"
    assert level_title(499) == "🌱 Data Seedling"
    assert level_title(500) == "🔍 Data Explorer"
    assert level_title(1500) == "📊 Data Analyst"
    assert level_title(3000) == "🧠 Cognitive Scientist"
    assert level_title(5000) == "⚡ Mind Hacker"
    assert level_title(9999) == "⚡ Mind Hacker"


def test_load_creates_default_profile_when_missing(tmp_path: Path) -> None:
    manager = ProfileManager(tmp_path / "profile.json")
    profile = manager.load()
    assert profile.alias == "anonymous"
    assert profile.arcade_points == 0
    assert profile.science_points == 0
    assert profile.badges == []
    assert profile.completed_lessons == []
    assert len(profile.device_uuid) == 36  # UUID4 format


def test_load_persists_new_profile_to_disk(tmp_path: Path) -> None:
    path = tmp_path / "profile.json"
    ProfileManager(path).load()
    assert path.exists()


def test_add_ap_accumulates_across_calls(tmp_path: Path) -> None:
    manager = ProfileManager(tmp_path / "profile.json")
    manager.add_ap(100)
    manager.add_ap(200)
    assert manager.load().arcade_points == 300


def test_add_sp_accumulates_across_calls(tmp_path: Path) -> None:
    manager = ProfileManager(tmp_path / "profile.json")
    manager.add_sp(50)
    manager.add_sp(75)
    assert manager.load().science_points == 125


def test_award_badge_stores_badge(tmp_path: Path) -> None:
    manager = ProfileManager(tmp_path / "profile.json")
    manager.award_badge("speed_runner")
    assert "speed_runner" in manager.load().badges


def test_award_badge_ignores_duplicates(tmp_path: Path) -> None:
    manager = ProfileManager(tmp_path / "profile.json")
    manager.award_badge("speed_runner")
    manager.award_badge("speed_runner")
    assert manager.load().badges.count("speed_runner") == 1


def test_complete_lesson_stores_number(tmp_path: Path) -> None:
    manager = ProfileManager(tmp_path / "profile.json")
    manager.complete_lesson(2)
    assert 2 in manager.load().completed_lessons


def test_complete_lesson_ignores_duplicates(tmp_path: Path) -> None:
    manager = ProfileManager(tmp_path / "profile.json")
    manager.complete_lesson(2)
    manager.complete_lesson(2)
    assert manager.load().completed_lessons.count(2) == 1


def test_device_uuid_stable_across_loads(tmp_path: Path) -> None:
    manager = ProfileManager(tmp_path / "profile.json")
    uuid1 = manager.load().device_uuid
    uuid2 = manager.load().device_uuid
    assert uuid1 == uuid2

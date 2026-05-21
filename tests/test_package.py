from pathlib import Path

from cognitive_data_arcade import main
from cognitive_data_arcade.engine.i18n import get_strings
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.menu import LessonMenuScene


def test_main_exists() -> None:
    assert callable(main)


def test_main_constructs_menu_with_profile_and_strings(tmp_path: Path) -> None:
    pm = ProfileManager(tmp_path / "profile.json")
    profile = pm.load()
    strings = get_strings(profile.language)
    scene = LessonMenuScene(pm, strings)
    assert not scene.is_done()

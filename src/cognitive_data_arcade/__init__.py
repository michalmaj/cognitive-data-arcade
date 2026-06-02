"""Cognitive Data Arcade package."""

from pathlib import Path

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.game_loop import GameLoop
from cognitive_data_arcade.engine.i18n import get_strings
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.menu import LessonMenuScene


def main() -> None:
    pm = ProfileManager(Path.home() / ".cognitive_data_arcade" / "profile.json")
    profile = pm.load()
    strings = get_strings(profile.language)
    audio.init(profile)
    GameLoop(LessonMenuScene(pm, strings)).run()

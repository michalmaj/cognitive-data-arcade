"""Cognitive Data Arcade package."""

from pathlib import Path

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.game_loop import GameLoop
from cognitive_data_arcade.engine.i18n import get_strings
from cognitive_data_arcade.profile.manager import ProfileManager


def main() -> None:
    pm = ProfileManager(Path.home() / ".cognitive_data_arcade" / "profile.json")
    profile = pm.load()
    strings = get_strings(profile.language)
    audio.init(profile)
    from cognitive_data_arcade.ui.intro_scene import TitleScene
    GameLoop(TitleScene(pm, strings), pm=pm).run(profile.fullscreen)

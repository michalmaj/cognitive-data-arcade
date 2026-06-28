"""Cognitive Data Arcade package."""

from pathlib import Path

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.game_loop import GameLoop
from cognitive_data_arcade.engine.i18n import get_strings
from cognitive_data_arcade.profile.manager import ProfileManager


def main() -> None:
    pm = ProfileManager(Path.home() / ".cognitive_data_arcade" / "profile.json")
    profile = pm.load()
    audio.init(profile)

    if not profile.onboarding_done:
        from cognitive_data_arcade.ui.onboarding_scene import OnboardingScene

        first_scene = OnboardingScene(pm)
    else:
        strings = get_strings(profile.language)
        from cognitive_data_arcade.ui.intro_scene import TitleScene

        first_scene = TitleScene(pm, strings)

    GameLoop(first_scene, pm=pm).run(profile.fullscreen)

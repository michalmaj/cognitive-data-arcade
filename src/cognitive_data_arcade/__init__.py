"""Cognitive Data Arcade package."""

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.app_paths import default_app_paths
from cognitive_data_arcade.engine.game_loop import GameLoop
from cognitive_data_arcade.engine.i18n import get_strings
from cognitive_data_arcade.profile.manager import ProfileManager


def main() -> None:
    paths = default_app_paths()
    paths.profile_dir.mkdir(parents=True, exist_ok=True)
    paths.generated_data_dir.mkdir(parents=True, exist_ok=True)
    paths.export_dir.mkdir(parents=True, exist_ok=True)
    pm = ProfileManager(paths.profile_dir / "profile.json", app_paths=paths)
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

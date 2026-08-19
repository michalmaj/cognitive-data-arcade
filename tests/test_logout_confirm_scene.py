# tests/test_logout_confirm_scene.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.ui.logout_confirm_scene import LogoutConfirmScene


class _FakePM:
    def __init__(self) -> None:
        self.delete_called = False

    def load(self):
        from cognitive_data_arcade.profile.manager import Profile

        return Profile()

    def delete_profile(self, generated_dir=None) -> None:
        self.delete_called = True

    def set_onboarding_done(self):
        from cognitive_data_arcade.profile.manager import Profile

        return Profile(onboarding_done=True)


def _make_scene(language: str = "pl") -> tuple[LogoutConfirmScene, _FakePM]:
    pygame.init()
    from cognitive_data_arcade.engine.i18n import get_strings

    pm = _FakePM()
    strings = get_strings(language)
    # profile_back_scene=None → on cancel, _next=None, but is_done=True
    return LogoutConfirmScene(pm, strings), pm


def test_not_done_initially() -> None:
    scene, _ = _make_scene()
    assert not scene.is_done()


def test_enter_confirms_logout_and_routes_to_onboarding() -> None:
    from cognitive_data_arcade.ui.onboarding_scene import OnboardingScene

    scene, pm = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), OnboardingScene)
    assert pm.delete_called


def test_esc_cancels_without_deleting() -> None:
    scene, pm = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert scene.is_done()
    assert not pm.delete_called


def test_esc_with_back_scene_routes_to_fresh_profile() -> None:
    import pathlib
    import tempfile

    from cognitive_data_arcade.ui.profile_screen import ProfileScene

    pygame.init()
    from cognitive_data_arcade.engine.i18n import get_strings
    from cognitive_data_arcade.profile.manager import ProfileManager

    with tempfile.TemporaryDirectory() as td:
        pm_real = ProfileManager(pathlib.Path(td) / "profile.json")
        strings = get_strings("pl")
        from cognitive_data_arcade.engine.scene import Scene

        class _FakeMenu(Scene):
            def handle_event(self, e):
                pass

            def update(self, dt):
                pass

            def draw(self, s):
                pass

            def is_done(self):
                return False

            def next_scene(self):
                return None

        back = _FakeMenu()
        scene = LogoutConfirmScene(pm_real, strings, profile_back_scene=back)
        scene.handle_event(
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
        )
        assert scene.is_done()
        assert isinstance(scene.next_scene(), ProfileScene)


def test_draw_does_not_crash() -> None:
    pygame.display.set_mode((1024, 768), pygame.NOFRAME)
    scene, _ = _make_scene()
    scene.draw(pygame.display.get_surface())

# tests/test_onboarding_scene.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.ui.onboarding_scene import OnboardingScene


class _FakePM:
    def __init__(self) -> None:
        self.saved_alias: str | None = None
        self.saved_language: str | None = None
        self.onboarding_done_called = False

    def load(self):
        from cognitive_data_arcade.profile.manager import Profile

        return Profile(alias="anonymous", language="pl")

    def save(self, profile) -> None:
        self.saved_alias = profile.alias
        self.saved_language = profile.language

    def set_onboarding_done(self):
        self.onboarding_done_called = True
        from cognitive_data_arcade.profile.manager import Profile

        return Profile(onboarding_done=True)


def _make_scene() -> tuple[OnboardingScene, _FakePM]:
    pygame.init()
    pm = _FakePM()
    return OnboardingScene(pm), pm


def test_not_done_initially() -> None:
    scene, _ = _make_scene()
    assert not scene.is_done()
    assert scene.next_scene() is None


def test_empty_alias_does_not_submit() -> None:
    scene, pm = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert not scene.is_done()
    assert pm.saved_alias is None


def test_valid_alias_and_enter_routes_to_title() -> None:
    from cognitive_data_arcade.ui.intro_scene import TitleScene

    scene, pm = _make_scene()
    for ch in "student42":
        scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=0, mod=0, unicode=ch))
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), TitleScene)
    assert pm.saved_alias == "student42"
    assert pm.onboarding_done_called


def test_language_toggle_changes_language() -> None:
    scene, pm = _make_scene()
    # Default is PL. Toggle to EN via TAB:
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_TAB, mod=0, unicode=""))
    for ch in "alice":
        scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=0, mod=0, unicode=ch))
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert pm.saved_language == "en"


def test_backspace_removes_last_char() -> None:
    scene, _ = _make_scene()
    for ch in "abc":
        scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=0, mod=0, unicode=ch))
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, mod=0, unicode="")
    )
    assert not scene.is_done()


def test_esc_is_noop() -> None:
    scene, _ = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert not scene.is_done()


def test_draw_does_not_crash() -> None:
    pygame.display.set_mode((1024, 768), pygame.NOFRAME)
    scene, _ = _make_scene()
    scene.draw(pygame.display.get_surface())

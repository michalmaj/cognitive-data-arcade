from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.ui.app_tutorial_scene import AppTutorialScene
from cognitive_data_arcade.ui.menu import LessonMenuScene


class _FakePM:
    def __init__(self) -> None:
        self.seen_intro_set: bool | None = None

    def load(self):
        from cognitive_data_arcade.profile.manager import Profile
        return Profile()

    def set_seen_intro(self, seen: bool) -> None:
        self.seen_intro_set = seen


def _make_scene() -> tuple[AppTutorialScene, _FakePM]:
    pygame.init()
    pm = _FakePM()
    return AppTutorialScene(pm, EN), pm


def test_not_done_initially():
    scene, _ = _make_scene()
    assert not scene.is_done()
    assert scene.next_scene() is None


def test_enter_marks_seen_and_goes_to_menu():
    scene, pm = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert scene.is_done()
    assert pm.seen_intro_set is True
    assert isinstance(scene.next_scene(), LessonMenuScene)


def test_space_marks_seen_and_goes_to_menu():
    scene, pm = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=""))
    assert scene.is_done()
    assert pm.seen_intro_set is True
    assert isinstance(scene.next_scene(), LessonMenuScene)


def test_esc_marks_seen_and_goes_to_menu():
    scene, pm = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert scene.is_done()
    assert pm.seen_intro_set is True
    assert isinstance(scene.next_scene(), LessonMenuScene)


def test_mouse_click_marks_seen_and_goes_to_menu():
    scene, pm = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(400, 300)))
    assert scene.is_done()
    assert pm.seen_intro_set is True
    assert isinstance(scene.next_scene(), LessonMenuScene)


def test_draw_does_not_crash():
    pygame.display.set_mode((800, 600), pygame.NOFRAME)
    scene, _ = _make_scene()
    scene.draw(pygame.display.get_surface())

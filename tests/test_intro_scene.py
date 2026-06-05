from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.ui.app_tutorial_scene import AppTutorialScene
from cognitive_data_arcade.ui.intro_scene import TitleScene
from cognitive_data_arcade.ui.menu import LessonMenuScene


class _FakePM:
    def __init__(self, seen_intro: bool = False) -> None:
        self._seen_intro = seen_intro
        self.seen_intro_set: bool | None = None

    def load(self):
        from cognitive_data_arcade.profile.manager import Profile
        return Profile(seen_intro=self._seen_intro)

    def set_seen_intro(self, seen: bool) -> None:
        self.seen_intro_set = seen


def _make_scene(seen_intro: bool = False) -> tuple[TitleScene, _FakePM]:
    pygame.init()
    pm = _FakePM(seen_intro=seen_intro)
    return TitleScene(pm, EN), pm


def test_not_done_initially():
    scene, _ = _make_scene()
    assert not scene.is_done()
    assert scene.next_scene() is None


def test_alpha_starts_at_zero():
    scene, _ = _make_scene()
    assert scene._alpha == 0.0


def test_alpha_increases_on_update():
    scene, _ = _make_scene()
    scene.update(400)
    assert 0.0 < scene._alpha <= 255.0


def test_alpha_capped_at_255():
    scene, _ = _make_scene()
    scene.update(2000)
    assert scene._alpha == 255.0


def test_enter_on_first_run_routes_to_tutorial():
    scene, _ = _make_scene(seen_intro=False)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), AppTutorialScene)


def test_enter_on_repeat_run_routes_to_menu():
    scene, _ = _make_scene(seen_intro=True)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), LessonMenuScene)


def test_esc_routes_to_menu_and_marks_seen():
    scene, pm = _make_scene(seen_intro=False)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), LessonMenuScene)
    assert pm.seen_intro_set is True


def test_mouse_click_on_first_run_routes_to_tutorial():
    scene, _ = _make_scene(seen_intro=False)
    scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(400, 300)))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), AppTutorialScene)


def test_draw_does_not_crash():
    pygame.display.set_mode((800, 600), pygame.NOFRAME)
    scene, _ = _make_scene()
    scene.draw(pygame.display.get_surface())

import pygame
import pytest
from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.ui.stroop_level_scene import StroopLevelScene
from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene
from cognitive_data_arcade.ui.menu import LessonMenuScene


class _FakePM:
    class _Profile:
        device_uuid = "test-uuid"

    def load(self):
        return self._Profile()


def _make_scene():
    pygame.init()
    return StroopLevelScene(_FakePM(), EN)


def test_default_diff_idx():
    scene = _make_scene()
    assert scene._diff_idx == 1


def test_left_decrements():
    scene = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=0, unicode=""))
    assert scene._diff_idx == 0


def test_left_clamps_at_zero():
    scene = _make_scene()
    scene._diff_idx = 0
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=0, unicode=""))
    assert scene._diff_idx == 0


def test_right_increments():
    scene = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT, mod=0, unicode=""))
    assert scene._diff_idx == 2


def test_right_clamps_at_two():
    scene = _make_scene()
    scene._diff_idx = 2
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT, mod=0, unicode=""))
    assert scene._diff_idx == 2


def test_mouse_click_tile0():
    scene = _make_scene()
    from cognitive_data_arcade.ui.stroop_level_scene import _tile_rect, _ROW_Y
    rect = _tile_rect(0, _ROW_Y)
    scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=rect.center))
    assert scene._diff_idx == 0


def test_mouse_click_tile2():
    scene = _make_scene()
    from cognitive_data_arcade.ui.stroop_level_scene import _tile_rect, _ROW_Y
    rect = _tile_rect(2, _ROW_Y)
    scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=rect.center))
    assert scene._diff_idx == 2


def test_enter_sets_done_and_next_is_how_to_play():
    scene = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), HowToPlayScene)


def test_esc_sets_done_and_next_is_menu():
    scene = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), LessonMenuScene)


def test_draw_without_crash():
    scene = _make_scene()
    surface = pygame.Surface((1024, 768))
    scene.draw(surface)

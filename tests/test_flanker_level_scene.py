from __future__ import annotations
import dataclasses
import pygame
import pytest
from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.ui.flanker_level_scene import FlankerLevelScene, _tile_rect, _ROW1_Y, _ROW2_Y
from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene
from cognitive_data_arcade.ui.menu import LessonMenuScene

class _FakePM:
    class _Profile:
        device_uuid = "test-uuid"
    def load(self):
        return self._Profile()

def _make_scene():
    pygame.init()
    return FlankerLevelScene(_FakePM(), EN)

def test_default_indices():
    scene = _make_scene()
    assert scene._session_idx == 1
    assert scene._diff_idx == 1

def test_default_active_row_is_session():
    scene = _make_scene()
    assert scene._active_row == 0

def test_up_sets_active_row_session():
    scene = _make_scene()
    scene._active_row = 1
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=0, unicode=""))
    assert scene._active_row == 0

def test_down_sets_active_row_diff():
    scene = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode=""))
    assert scene._active_row == 1

def test_left_decrements_session_row():
    scene = _make_scene()
    scene._active_row = 0
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=0, unicode=""))
    assert scene._session_idx == 0

def test_right_increments_diff_row():
    scene = _make_scene()
    scene._active_row = 1
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT, mod=0, unicode=""))
    assert scene._diff_idx == 2

def test_left_clamps_session():
    scene = _make_scene()
    scene._session_idx = 0
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=0, unicode=""))
    assert scene._session_idx == 0

def test_right_clamps_diff():
    scene = _make_scene()
    scene._diff_idx = 2
    scene._active_row = 1
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT, mod=0, unicode=""))
    assert scene._diff_idx == 2

def test_mouse_click_session_tile0():
    scene = _make_scene()
    rect = _tile_rect(0, _ROW1_Y)
    scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=rect.center))
    assert scene._session_idx == 0
    assert not scene.is_done()  # no auto-launch

def test_mouse_click_diff_tile2():
    scene = _make_scene()
    rect = _tile_rect(2, _ROW2_Y)
    scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=rect.center))
    assert scene._diff_idx == 2
    assert not scene.is_done()

def test_enter_sets_done_and_how_to_play():
    scene = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), HowToPlayScene)

def test_esc_returns_menu():
    scene = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), LessonMenuScene)

def test_config_combining():
    # Verify that _launch produces correct config
    scene = _make_scene()
    scene._session_idx = 2  # FULL = 96 trials
    scene._diff_idx = 2     # HARD = 1000ms
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    # Can't easily inspect the config after launch, but we can verify is_done
    assert scene.is_done()

def test_draw_without_crash():
    scene = _make_scene()
    surface = pygame.Surface((1024, 768))
    scene.draw(surface)

from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.ui.event_log_level_scene import (
    EventLogLevelScene,
    _tile_rect,
    _ROW1_Y,
    _ROW2_Y,
)
from cognitive_data_arcade.ui.menu import LessonMenuScene


class _FakePM:
    class _Profile:
        device_uuid = "test-uuid"

    def load(self):
        return self._Profile()


def _make_scene():
    pygame.init()
    return EventLogLevelScene(_FakePM(), EN)


def test_default_exp_idx():
    assert _make_scene()._exp_idx == 0


def test_default_diff_idx():
    assert _make_scene()._diff_idx == 1


def test_default_active_row_is_exp():
    assert _make_scene()._active_row == 0


def test_up_sets_active_row_exp():
    scene = _make_scene()
    scene._active_row = 1
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=0, unicode=""))
    assert scene._active_row == 0


def test_down_sets_active_row_diff():
    scene = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode=""))
    assert scene._active_row == 1


def test_left_decrements_exp_row():
    scene = _make_scene()
    scene._exp_idx = 2
    scene._active_row = 0
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=0, unicode=""))
    assert scene._exp_idx == 1


def test_right_increments_diff_row():
    scene = _make_scene()
    scene._active_row = 1
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT, mod=0, unicode=""))
    assert scene._diff_idx == 2


def test_left_clamps_exp():
    scene = _make_scene()
    scene._exp_idx = 0
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=0, unicode=""))
    assert scene._exp_idx == 0


def test_right_clamps_diff():
    scene = _make_scene()
    scene._diff_idx = 2
    scene._active_row = 1
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT, mod=0, unicode=""))
    assert scene._diff_idx == 2


def test_mouse_click_exp_tile0():
    scene = _make_scene()
    rect = _tile_rect(0, _ROW1_Y)
    scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=rect.center))
    assert scene._exp_idx == 0
    assert not scene.is_done()


def test_mouse_click_diff_tile2():
    scene = _make_scene()
    rect = _tile_rect(2, _ROW2_Y)
    scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=rect.center))
    assert scene._diff_idx == 2
    assert not scene.is_done()


def test_enter_sets_done():
    scene = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert scene.is_done()
    assert scene.next_scene() is not None


def test_esc_returns_to_menu():
    scene = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), LessonMenuScene)


def test_not_done_initially():
    scene = _make_scene()
    assert not scene.is_done()
    assert scene.next_scene() is None

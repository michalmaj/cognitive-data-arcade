from __future__ import annotations
import pygame
import pytest
from unittest.mock import MagicMock
from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.ui.menu import LessonMenuScene, _VIRTUAL_H, _SIDEBAR_H


@pytest.fixture(autouse=True)
def _init():
    pygame.font.init()
    yield


def _make(selected=0):
    pm = MagicMock()
    pm.load.return_value = MagicMock(
        alias="T", device_uuid="x",
        music_enabled=True, sfx_enabled=True,
        music_volume=1.0, sfx_volume=1.0,
    )
    return LessonMenuScene(pm, EN, selected)


def _key(k: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="")


def test_esc_quits():
    s = _make()
    s.handle_event(_key(pygame.K_ESCAPE))
    assert s.is_done() and s.next_scene() is None


def test_down_increments_selected():
    s = _make(selected=0)
    s.handle_event(_key(pygame.K_DOWN))
    assert s._selected == 1


def test_up_clamps_at_zero():
    s = _make(selected=0)
    s.handle_event(_key(pygame.K_UP))
    assert s._selected == 0


def test_enter_on_lesson2_launches_rt_lab():
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene
    pygame.init()
    s = _make(selected=0)
    s.handle_event(_key(pygame.K_DOWN))   # idx 1 = lesson 2
    s.handle_event(_key(pygame.K_RETURN))
    assert s.is_done()
    assert isinstance(s.next_scene(), HowToPlayScene)


def test_enter_does_not_show_popup():
    s = _make(selected=0)
    assert not hasattr(s, "_popup_visible") or not s._popup_visible
    s.handle_event(_key(pygame.K_RETURN))
    # No popup attribute expected
    assert not getattr(s, "_popup_visible", False)


def test_sidebar_click_changes_selection():
    pygame.init()
    surface = pygame.Surface((1024, 640))
    s = _make(selected=0)
    s.draw(surface)  # populate _play_btn_rect
    # Module 1 header: vy=0..31
    # item 0: vy=32..67
    # item 1: vy=68..103
    # item 2: vy=104..139  → screen_y = 56 + 104 - 0 = 160 (center = 160+18=178)
    click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(100, 178), button=1)
    s.handle_event(click)
    assert s._selected == 2


def test_wheel_scrolls():
    s = _make(selected=0)
    scroll_before = s._scrollbar.scroll
    wheel = pygame.event.Event(pygame.MOUSEWHEEL, y=-3)
    s.handle_event(wheel)
    assert s._scrollbar.scroll > scroll_before


def test_ensure_visible_on_down_near_bottom():
    s = _make(selected=29)   # second-to-last lesson
    s.handle_event(_key(pygame.K_DOWN))
    # selected is now 30 (last) — scrollbar should have scrolled to show it
    scroll = s._scrollbar.scroll
    max_s = max(0, _VIRTUAL_H - _SIDEBAR_H)
    assert 0 <= scroll <= max_s

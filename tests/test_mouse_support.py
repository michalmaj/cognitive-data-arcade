import pygame
import pytest
from unittest.mock import MagicMock
from cognitive_data_arcade.engine.mouse import hit

pygame.init()
pygame.display.set_mode((1024, 768))


def test_hit_inside():
    rect = pygame.Rect(10, 10, 100, 50)
    assert hit(rect, (50, 30))


def test_hit_outside():
    rect = pygame.Rect(10, 10, 100, 50)
    assert not hit(rect, (200, 200))


def test_hit_edge():
    rect = pygame.Rect(10, 10, 100, 50)
    assert hit(rect, (10, 10))


def test_hit_just_outside():
    rect = pygame.Rect(10, 10, 100, 50)
    assert not hit(rect, (110, 60))


def _make_menu():
    from cognitive_data_arcade.ui.menu import LessonMenuScene
    pm = MagicMock()
    pm.load.return_value = MagicMock(
        alias="Test", device_uuid="x",
        arcade_points=0, science_points=0,
        badges=[], completed_lessons=[],
        music_enabled=True, sfx_enabled=True,
        music_volume=1.0, sfx_volume=1.0
    )
    from cognitive_data_arcade.engine.i18n import get_strings
    strings = get_strings("en")
    return LessonMenuScene(pm, strings)


def test_menu_mousemotion_sets_selected():
    menu = _make_menu()
    # Row 2 center: y = 140 + 2*44 + 22 = 250
    event = pygame.event.Event(pygame.MOUSEMOTION, pos=(200, 250))
    menu.handle_event(event)
    assert menu._selected == 2


def test_menu_mousebuttondown_shows_popup():
    menu = _make_menu()
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(200, 150), button=1)
    menu.handle_event(event)
    assert menu._popup_visible is True


def test_menu_popup_esc_closes():
    menu = _make_menu()
    # Open popup on row 0
    click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(200, 150), button=1)
    menu.handle_event(click)
    assert menu._popup_visible
    # Close with ESC
    esc = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    menu.handle_event(esc)
    assert not menu._popup_visible


def test_menu_teoria_available_for_lesson_1():
    menu = _make_menu()
    menu._selected = 0  # lesson 1
    assert menu._teoria_available()


def test_menu_teoria_not_available_for_lesson_3():
    menu = _make_menu()
    menu._selected = 2  # lesson 3 (index 2)
    assert not menu._teoria_available()

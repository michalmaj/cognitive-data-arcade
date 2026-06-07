from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine.scrollbar import ScrollBar


@pytest.fixture(scope="session")
def pg():
    pygame.init()
    yield
    pygame.quit()


def test_thumb_height_proportional():
    sb = ScrollBar(100, 15, x=0, y=0, h=300)
    # max(20, round(15/100 * 300)) = 45
    assert sb._thumb_h() == 45


def test_scroll_starts_at_zero():
    assert ScrollBar(100, 15, 0, 0, 300).scroll == 0


def test_wheel_down_increments_scroll():
    sb = ScrollBar(100, 15, 0, 0, 300)
    changed = sb.handle_wheel(1)
    assert changed and sb.scroll == 1


def test_wheel_up_at_zero_is_noop():
    sb = ScrollBar(100, 15, 0, 0, 300)
    changed = sb.handle_wheel(-1)
    assert not changed and sb.scroll == 0


def test_wheel_clamps_at_max():
    sb = ScrollBar(20, 15, 0, 0, 300)
    sb.handle_wheel(100)
    assert sb.scroll == 5  # max = total - visible = 5


def test_track_click_below_thumb_jumps():
    sb = ScrollBar(100, 15, x=0, y=0, h=300)
    # At scroll=0: thumb_y=0, thumb_h=45. Click at y=150 is below thumb.
    # new_s = round((150 - 0 - 45) / (300 - 45) * 85) = round(34.98) = 35
    sb.handle_mousedown((3, 150))
    assert sb.scroll == 35


def test_no_op_when_all_visible():
    sb = ScrollBar(10, 15, 0, 0, 300)
    assert not sb.handle_wheel(1)
    assert sb.scroll == 0


def test_draw_does_not_raise(pg):
    sb = ScrollBar(100, 15, x=740, y=100, h=420)
    surface = pygame.Surface((800, 600))
    sb.draw(surface)


def test_mousedown_in_scrollbar_area_returns_true():
    sb = ScrollBar(100, 15, x=0, y=0, h=300)
    # x=3 is within [0, 0+6], so click is consumed
    assert sb.handle_mousedown((3, 200))


def test_mousedown_outside_scrollbar_area_returns_false():
    sb = ScrollBar(100, 15, x=0, y=0, h=300)
    assert not sb.handle_mousedown((100, 150))


def test_mousedown_noop_when_all_visible():
    sb = ScrollBar(10, 15, 0, 0, 300)
    assert not sb.handle_mousedown((3, 150))


def test_set_total_clamps_scroll():
    sb = ScrollBar(100, 15, 0, 0, 300)
    sb.handle_wheel(50)   # scroll = 50
    sb.set_total(20)
    assert sb.scroll == 5  # max = 20 - 15 = 5


def test_scroll_to_clamps_to_max():
    sb = ScrollBar(20, 15, 0, 0, 300)
    sb.scroll_to(999)
    assert sb.scroll == 5


def test_scroll_to_clamps_to_zero():
    sb = ScrollBar(20, 15, 0, 0, 300)
    sb.scroll_to(-99)
    assert sb.scroll == 0


def test_drag_updates_scroll(pg):
    sb = ScrollBar(100, 15, x=0, y=0, h=300)
    # Mousedown on thumb (ty=0, th=45, click at y=22 -> anchor=22)
    sb.handle_mousedown((3, 22))
    # Drag to y=200 -> thumb_top = 200 - 22 = 178
    # new_s = round((178 - 0) / (300 - 45) * 85) = round(59.3) ~= 59
    sb.handle_mousemotion((3, 200), (1, 0, 0))
    assert sb.scroll == 59

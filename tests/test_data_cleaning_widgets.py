# tests/test_data_cleaning_widgets.py
from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.games.data_cleaning.generator import DataRow
from cognitive_data_arcade.games.data_cleaning.ui_table import TableWidget


@pytest.fixture(scope="session", autouse=True)
def pg():
    pygame.init()
    yield
    pygame.quit()


def _rows(n: int = 10) -> list[DataRow]:
    return [DataRow(i + 1, 1, i + 1, 400.0 + i * 5, 0.85) for i in range(n)]


# ── cursor navigation ───────────────────────────────────────────────────────────

def test_cursor_starts_at_zero():
    t = TableWidget(_rows())
    assert t.cursor == 0


def test_down_increments_cursor():
    t = TableWidget(_rows(10))
    t.handle_keydown(pygame.K_DOWN)
    assert t.cursor == 1


def test_up_at_zero_does_not_go_negative():
    t = TableWidget(_rows(10))
    t.handle_keydown(pygame.K_UP)
    assert t.cursor == 0


def test_down_at_last_row_does_not_overflow():
    t = TableWidget(_rows(3))
    for _ in range(10):
        t.handle_keydown(pygame.K_DOWN)
    assert t.cursor == 2


# ── flag toggling ────────────────────────────────────────────────────────────────

def test_space_flags_current_row_returns_flagged():
    t = TableWidget(_rows(10))
    result = t.handle_keydown(pygame.K_SPACE)
    assert result == "flagged"
    assert 0 in t.flagged


def test_enter_also_flags():
    t = TableWidget(_rows(10))
    result = t.handle_keydown(pygame.K_RETURN)
    assert result == "flagged"


def test_space_on_flagged_row_unflags():
    t = TableWidget(_rows(10))
    t.handle_keydown(pygame.K_SPACE)
    result = t.handle_keydown(pygame.K_SPACE)
    assert result == "unflagged"
    assert 0 not in t.flagged


def test_flagged_property_returns_copy():
    t = TableWidget(_rows(10))
    t.handle_keydown(pygame.K_SPACE)
    flagged = t.flagged
    flagged.add(99)
    assert 99 not in t.flagged


def test_nav_keys_return_none():
    t = TableWidget(_rows(10))
    assert t.handle_keydown(pygame.K_DOWN) is None
    assert t.handle_keydown(pygame.K_UP) is None


from cognitive_data_arcade.games.data_cleaning.ui_popup import DecisionPopup


def _row(accuracy: float = 0.9) -> DataRow:
    return DataRow(1, 1, 1, -55.0, accuracy)


# ── cursor ──────────────────────────────────────────────────────────────────────

def test_popup_cursor_starts_at_zero():
    p = DecisionPopup(_row(), has_format_fix=False)
    assert p.cursor == 0


def test_popup_down_increments_cursor():
    p = DecisionPopup(_row(), has_format_fix=False)
    p.handle_keydown(pygame.K_DOWN)
    assert p.cursor == 1


def test_popup_up_does_not_go_below_zero():
    p = DecisionPopup(_row(), has_format_fix=False)
    p.handle_keydown(pygame.K_UP)
    assert p.cursor == 0


def test_popup_cursor_clamps_at_last_choice():
    p = DecisionPopup(_row(), has_format_fix=False)
    for _ in range(10):
        p.handle_keydown(pygame.K_DOWN)
    assert p.cursor == 2  # 3 choices: delete / median / keep


# ── choices without format fix ──────────────────────────────────────────────────

def test_popup_enter_returns_delete_by_default():
    p = DecisionPopup(_row(), has_format_fix=False)
    result = p.handle_keydown(pygame.K_RETURN)
    assert result == "delete"


def test_popup_key1_selects_delete():
    p = DecisionPopup(_row(), has_format_fix=False)
    p.handle_keydown(pygame.K_1)
    assert p.handle_keydown(pygame.K_RETURN) == "delete"


def test_popup_key2_selects_median():
    p = DecisionPopup(_row(), has_format_fix=False)
    p.handle_keydown(pygame.K_2)
    assert p.handle_keydown(pygame.K_RETURN) == "median"


def test_popup_key3_selects_keep():
    p = DecisionPopup(_row(), has_format_fix=False)
    p.handle_keydown(pygame.K_3)
    assert p.handle_keydown(pygame.K_RETURN) == "keep"


# ── choices with format fix ─────────────────────────────────────────────────────

def test_popup_format_fix_replaces_median():
    p = DecisionPopup(_row(accuracy=85.0), has_format_fix=True)
    p.handle_keydown(pygame.K_2)  # index 1 → fix_format
    assert p.handle_keydown(pygame.K_RETURN) == "fix_format"


def test_popup_format_fix_key3_is_keep():
    p = DecisionPopup(_row(accuracy=85.0), has_format_fix=True)
    p.handle_keydown(pygame.K_3)
    assert p.handle_keydown(pygame.K_RETURN) == "keep"


def test_popup_nav_keys_return_none():
    p = DecisionPopup(_row(), has_format_fix=False)
    assert p.handle_keydown(pygame.K_DOWN) is None
    assert p.handle_keydown(pygame.K_UP) is None


# ── draw with hints_visible parameter ───────────────────────────────────────────

def test_draw_with_hints_visible_false_does_not_raise():
    surface = pygame.Surface((800, 600))
    t = TableWidget(_rows(10))
    t.handle_keydown(pygame.K_SPACE)  # flag row 0
    t.draw(surface, hints_visible=False)  # should not raise


def test_draw_with_hints_visible_true_does_not_raise():
    surface = pygame.Surface((800, 600))
    t = TableWidget(_rows(10))
    t.handle_keydown(pygame.K_SPACE)
    t.draw(surface, hints_visible=True)


# ── scroll property ──────────────────────────────────────────────────────────────

def test_scroll_property_starts_zero():
    t = TableWidget(_rows(20))
    assert t.scroll == 0


# ── set_cursor ───────────────────────────────────────────────────────────────────

def test_set_cursor_moves_cursor():
    t = TableWidget(_rows(20))
    t.set_cursor(5)
    assert t.cursor == 5


def test_set_cursor_adjusts_scroll_down():
    # VISIBLE_ROWS = 15; cursor 16 → scroll must be at least 2 (16 - 15 + 1)
    t = TableWidget(_rows(20))
    t.set_cursor(16)
    assert t.scroll == 2


def test_set_cursor_adjusts_scroll_up():
    # Move cursor down to force scroll, then move cursor back up
    t = TableWidget(_rows(20))
    t.set_cursor(16)   # scroll = 2
    t.set_cursor(1)    # cursor 1 < scroll 2 → scroll becomes 1
    assert t.scroll == 1


def test_set_cursor_out_of_range_ignored():
    t = TableWidget(_rows(5))
    t.set_cursor(99)
    assert t.cursor == 0   # unchanged


# ── flag_toggle ──────────────────────────────────────────────────────────────────

def test_flag_toggle_flags_row():
    t = TableWidget(_rows(5))
    result = t.flag_toggle(2)
    assert result == "flagged"
    assert 2 in t.flagged


def test_flag_toggle_unflags_row():
    t = TableWidget(_rows(5))
    t.flag_toggle(2)
    result = t.flag_toggle(2)
    assert result == "unflagged"
    assert 2 not in t.flagged

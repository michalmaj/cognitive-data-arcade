# tests/test_data_cleaning_widgets.py
from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.games.data_cleaning.generator import DataRow
from cognitive_data_arcade.games.data_cleaning.ui_table import TableWidget


@pytest.fixture(autouse=True)
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

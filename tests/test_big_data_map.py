from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager


@pytest.fixture
def game(tmp_path):
    pygame.init()
    pm = ProfileManager(tmp_path / "profile.json")
    from cognitive_data_arcade.games.big_data_map.game import BigDataMapGame
    return BigDataMapGame(PL, pm)


def test_initial_state_is_l1(game) -> None:
    assert game._in_l2 is False
    assert game._l1_idx == 0


def test_enter_in_l1_goes_to_l2(game) -> None:
    game.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="")
    )
    assert game._in_l2 is True


def test_enter_in_l2_returns_to_l1(game) -> None:
    game._in_l2 = True
    game.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="")
    )
    assert game._in_l2 is False


def test_backspace_in_l2_returns_to_l1(game) -> None:
    game._in_l2 = True
    game.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, mod=0, unicode="")
    )
    assert game._in_l2 is False


def test_game_never_done(game) -> None:
    assert game.is_done() is False
    game.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="")
    )
    assert game.is_done() is False


def test_next_scene_is_none(game) -> None:
    assert game.next_scene() is None


def test_draw_l1_without_crash(game) -> None:
    surface = pygame.Surface((1024, 768))
    game.draw(surface)


def test_draw_l2_without_crash(game) -> None:
    surface = pygame.Surface((1024, 768))
    game._in_l2 = True
    game.draw(surface)


def test_arrow_key_cycles_selection(game) -> None:
    initial = game._l1_idx
    game.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode="")
    )
    assert game._l1_idx == (initial + 1) % 6

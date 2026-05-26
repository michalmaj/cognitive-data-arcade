from __future__ import annotations

from pathlib import Path

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.games.big_data_map.game import BigDataMapGame
from cognitive_data_arcade.profile.manager import ProfileManager


def _make_game(tmp_path: Path) -> BigDataMapGame:
    pm = ProfileManager(tmp_path / "profile.json")
    return BigDataMapGame(PL, pm)


def _key(k: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="")


@pytest.fixture(autouse=True)
def pg() -> None:  # type: ignore[return]
    pygame.init()
    yield  # type: ignore[misc]
    pygame.quit()


def test_initial_state_is_l1(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    assert not game._in_l2
    assert not game.is_done()


def test_draw_without_crash(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    surface = pygame.Surface((1024, 768))
    game.draw(surface)  # must not raise


def test_arrow_keys_cycle_nodes(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    assert game._l1_idx == 0
    game.handle_event(_key(pygame.K_DOWN))
    assert game._l1_idx == 1
    game.handle_event(_key(pygame.K_UP))
    assert game._l1_idx == 0

from __future__ import annotations

from pathlib import Path

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.nback_level_scene import NBackLevelScene


def _make(tmp_path: Path) -> NBackLevelScene:
    pm = ProfileManager(tmp_path / "profile.json")
    return NBackLevelScene(pm, PL)


def _key(k: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="")


def test_draws_without_crash(tmp_path: Path) -> None:
    pygame.init()
    surface = pygame.Surface((1024, 768))
    scene = _make(tmp_path)
    scene.draw(surface)


def test_initial_selection_is_zero(tmp_path: Path) -> None:
    scene = _make(tmp_path)
    assert scene._selected == 0


def test_up_down_navigate(tmp_path: Path) -> None:
    scene = _make(tmp_path)
    scene.handle_event(_key(pygame.K_DOWN))
    assert scene._selected == 1
    scene.handle_event(_key(pygame.K_UP))
    assert scene._selected == 0


def test_up_clamps_at_zero(tmp_path: Path) -> None:
    scene = _make(tmp_path)
    scene.handle_event(_key(pygame.K_UP))
    assert scene._selected == 0


def test_down_clamps_at_three(tmp_path: Path) -> None:
    scene = _make(tmp_path)
    for _ in range(20):
        scene.handle_event(_key(pygame.K_DOWN))
    assert scene._selected == 3


def test_enter_launches_how_to_play_scene(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    pygame.init()
    scene = _make(tmp_path)
    scene.handle_event(_key(pygame.K_RETURN))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), HowToPlayScene)


def test_esc_returns_to_lesson_menu(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.menu import LessonMenuScene

    scene = _make(tmp_path)
    scene.handle_event(_key(pygame.K_ESCAPE))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), LessonMenuScene)


def test_not_done_initially(tmp_path: Path) -> None:
    scene = _make(tmp_path)
    assert not scene.is_done()
    assert scene.next_scene() is None

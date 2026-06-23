# tests/test_module_runner_scene.py
from __future__ import annotations

import pygame
import pytest
from unittest.mock import MagicMock

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.ui.module_runner_scene import ModuleRunnerScene


@pytest.fixture(autouse=True)
def _init():
    pygame.font.init()
    yield


def _make_pm(completed: list[int] | None = None) -> MagicMock:
    pm = MagicMock()
    pm.load.return_value = MagicMock(
        completed_lessons=completed or [],
        current_module_idx=None,
        language="pl",
    )
    return pm


def _key(k: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="")


def test_find_current_step_none_complete():
    scene = ModuleRunnerScene(0, _make_pm(), EN)
    assert scene._current_step == 0


def test_find_current_step_first_two_complete():
    # Module 0 lesson nums: [1, 2, 3, 4, 6]
    scene = ModuleRunnerScene(0, _make_pm([1, 2]), EN)
    assert scene._current_step == 2  # third lesson (index 2)


def test_find_current_step_all_complete_stays_on_last():
    scene = ModuleRunnerScene(0, _make_pm([1, 2, 3, 4, 6]), EN)
    assert scene._current_step == 4  # last index


def test_keyboard_right_advances_step():
    scene = ModuleRunnerScene(0, _make_pm(), EN)
    scene.handle_event(_key(pygame.K_RIGHT))
    assert scene._current_step == 1


def test_keyboard_right_clamps_at_last():
    scene = ModuleRunnerScene(0, _make_pm(), EN)
    scene._current_step = 4
    scene.handle_event(_key(pygame.K_RIGHT))
    assert scene._current_step == 4


def test_keyboard_left_clamps_at_zero():
    scene = ModuleRunnerScene(0, _make_pm(), EN)
    scene.handle_event(_key(pygame.K_LEFT))
    assert scene._current_step == 0


def test_escape_sets_done_and_next_is_menu():
    from cognitive_data_arcade.ui.menu import LessonMenuScene

    scene = ModuleRunnerScene(0, _make_pm(), EN)
    scene.handle_event(_key(pygame.K_ESCAPE))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), LessonMenuScene)

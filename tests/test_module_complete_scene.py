# tests/test_module_complete_scene.py
from __future__ import annotations

import pygame
import pytest
from unittest.mock import MagicMock

from cognitive_data_arcade.engine.i18n import EN


@pytest.fixture(autouse=True)
def _init():
    pygame.font.init()
    yield


def _make_pm() -> MagicMock:
    pm = MagicMock()
    pm.load.return_value = MagicMock(
        completed_lessons=[1, 2, 3, 4, 6],
        arcade_points=150,
        science_points=50,
        language="pl",
    )
    return pm


def _key(k: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="")


def test_escape_returns_to_menu():
    from cognitive_data_arcade.ui.module_complete_scene import ModuleCompleteScene
    from cognitive_data_arcade.ui.menu import LessonMenuScene
    scene = ModuleCompleteScene(0, _make_pm(), EN)
    scene.handle_event(_key(pygame.K_ESCAPE))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), LessonMenuScene)


def test_enter_goes_to_next_module():
    from cognitive_data_arcade.ui.module_complete_scene import ModuleCompleteScene
    from cognitive_data_arcade.ui.module_runner_scene import ModuleRunnerScene
    scene = ModuleCompleteScene(0, _make_pm(), EN)
    scene.handle_event(_key(pygame.K_RETURN))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), ModuleRunnerScene)


def test_last_module_enter_goes_to_menu():
    from cognitive_data_arcade.ui.module_complete_scene import ModuleCompleteScene
    from cognitive_data_arcade.ui.menu import LessonMenuScene
    scene = ModuleCompleteScene(5, _make_pm(), EN)  # module index 5 = last
    scene.handle_event(_key(pygame.K_RETURN))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), LessonMenuScene)


def test_clear_current_module_called_on_init():
    from cognitive_data_arcade.ui.module_complete_scene import ModuleCompleteScene
    pm = _make_pm()
    ModuleCompleteScene(0, pm, EN)
    pm.clear_current_module.assert_called_once()

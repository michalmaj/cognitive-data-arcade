# tests/test_hyp_menu.py
from __future__ import annotations
import pytest
import pygame


@pytest.fixture(autouse=True)
def pg():
    pygame.init()
    pygame.display.set_mode((1024, 720))
    yield
    pygame.quit()


def test_lesson_15_in_lessons_list():
    from cognitive_data_arcade.ui.menu import _LESSONS
    nums = [num for num, _ in _LESSONS]
    assert 15 in nums, "Lesson 15 must be in _LESSONS"


def test_lesson_15_name():
    from cognitive_data_arcade.ui.menu import _LESSONS
    name = next((n for num, n in _LESSONS if num == 15), None)
    assert name == "Hypothesis Arena"


def test_game_factory_for_15_returns_callable(tmp_path):
    from cognitive_data_arcade.engine.i18n import get_strings
    from cognitive_data_arcade.profile.manager import ProfileManager
    from cognitive_data_arcade.ui.menu import LessonMenuScene
    strings = get_strings("pl")
    pm = ProfileManager(tmp_path / "profile.json")
    scene = LessonMenuScene(pm, strings)
    factory = scene._game_factory_for(15)
    assert callable(factory), "_game_factory_for(15) must return a callable"

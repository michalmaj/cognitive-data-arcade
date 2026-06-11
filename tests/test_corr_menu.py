from __future__ import annotations
import pytest
import pygame


@pytest.fixture(autouse=True)
def pg():
    pygame.init()
    pygame.display.set_mode((1024, 720))
    yield
    pygame.quit()


def test_lesson_14_in_lessons_list():
    from cognitive_data_arcade.ui.menu import _LESSONS
    nums = [num for num, _ in _LESSONS]
    assert 14 in nums, "Lesson 14 must be in _LESSONS"


def test_lesson_14_name():
    from cognitive_data_arcade.ui.menu import _LESSONS
    name = next((n for num, n in _LESSONS if num == 14), None)
    assert name == "Correlation Trap"


def test_game_factory_for_14_returns_callable(tmp_path):
    from cognitive_data_arcade.engine.i18n import get_strings
    from cognitive_data_arcade.profile.manager import ProfileManager
    from cognitive_data_arcade.ui.menu import LessonMenuScene
    strings = get_strings("pl")
    pm = ProfileManager(tmp_path / "profile.json")
    scene = LessonMenuScene(pm, strings)
    factory = scene._game_factory_for(14)
    assert callable(factory), "_game_factory_for(14) must return a callable"

# tests/test_data_cleaning_menu.py
from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.games.data_cleaning.scene import DataCleaningScene
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.menu import LessonMenuScene, _LESSONS


@pytest.fixture
def pm(tmp_path):
    return ProfileManager(tmp_path / "p.json")


@pytest.fixture(autouse=True)
def pg():
    pygame.display.init()
    pygame.font.init()
    yield
    pygame.display.quit()


def test_lesson_5_not_in_lessons_list():
    lesson_nums = [num for num, _ in _LESSONS]
    assert 5 not in lesson_nums


def test_lesson_4_title_contains_0405():
    titles = {num: title for num, title in _LESSONS}
    assert "04+05" in titles[4] or "04" in titles[4]


def test_data_cleaning_scene_launched_for_lesson_4(pm):
    pygame.display.set_mode((800, 600), pygame.NOFRAME)
    menu = LessonMenuScene(pm, EN, selected=0)
    lesson_nums = [num for num, _ in _LESSONS]
    idx4 = lesson_nums.index(4)
    menu._selected = idx4
    menu._launch_selected_game()
    assert isinstance(menu._next, DataCleaningScene)

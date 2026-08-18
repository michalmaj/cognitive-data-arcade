from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.ui.menu import LessonMenuScene


class _FakePM:
    class _Profile:
        alias = "Test"
        device_uuid = "x"
        completed_lessons: list = []
        music_enabled = True
        sfx_enabled = True
        music_volume = 1.0
        sfx_volume = 1.0
        current_module_idx = None
        streak_days = 0
        seen_intro = True

    def __init__(self):
        self._completed: list[int] = []

    def load(self):
        p = self._Profile()
        p.completed_lessons = list(self._completed)
        return p

    def complete_lesson(self, lesson_num: int) -> None:
        if lesson_num not in self._completed:
            self._completed.append(lesson_num)


@pytest.fixture(autouse=True)
def _pygame():
    pygame.font.init()
    yield


def test_completed_set_empty_on_fresh_profile():
    pm = _FakePM()
    scene = LessonMenuScene(pm, EN)
    assert scene._completed == set()


def test_completed_set_populated_from_profile():
    pm = _FakePM()
    pm._completed = [1, 3, 7]
    scene = LessonMenuScene(pm, EN)
    assert scene._completed == {1, 3, 7}


def test_complete_lesson_not_called_on_launch():
    """Launching a game must NOT mark the lesson complete — only finishing does."""
    pm = _FakePM()
    scene = LessonMenuScene(pm, EN)

    assert scene._selected == 0
    scene._launch_selected_game()

    assert pm._completed == []


def test_complete_lesson_game_launches_without_marking_completion():
    """_launch_selected_game transitions to a game scene without recording completion."""
    pm = _FakePM()
    scene = LessonMenuScene(pm, EN)

    scene._launch_selected_game()
    assert scene._done is True
    assert scene._next is not None
    assert pm._completed == []


def test_draw_with_some_completed_no_crash():
    pygame.init()
    pm = _FakePM()
    pm._completed = [1, 2, 3]
    scene = LessonMenuScene(pm, EN)
    surface = pygame.Surface((1024, 768))
    scene.draw(surface)


def test_draw_all_completed_no_crash():
    pygame.init()
    pm = _FakePM()
    pm._completed = list(range(1, 33))
    scene = LessonMenuScene(pm, EN)
    surface = pygame.Surface((1024, 768))
    scene.draw(surface)


def test_topbar_progress_counter_renders_for_completed():
    pygame.init()
    pm = _FakePM()
    pm._completed = [1, 2]
    scene = LessonMenuScene(pm, EN)
    surface = pygame.Surface((1024, 768))
    scene.draw(surface)
    assert scene._completed == {1, 2}

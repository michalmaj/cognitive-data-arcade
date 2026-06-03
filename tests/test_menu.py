from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.lesson_reader import LessonReaderScene
from cognitive_data_arcade.ui.menu import LessonMenuScene


@pytest.fixture(autouse=True)
def _init_pygame():
    pygame.font.init()
    yield


def _key(k: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="")


def test_t_opens_lesson_reader_for_lesson_with_content(tmp_path):
    pm = ProfileManager(tmp_path / "profile.json")
    scene = LessonMenuScene(pm, PL)
    # Default selected is 0 = lesson 1 (BigDataMap) — has content
    scene.handle_event(_key(pygame.K_t))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), LessonReaderScene)


def test_t_opens_lesson_reader_for_lesson_3(tmp_path):
    pm = ProfileManager(tmp_path / "profile.json")
    scene = LessonMenuScene(pm, PL)
    # Move to lesson 3 (index 2) — now has content
    for _ in range(2):
        scene.handle_event(_key(pygame.K_DOWN))
    scene.handle_event(_key(pygame.K_t))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), LessonReaderScene)

from __future__ import annotations
import pygame
import pytest
from unittest.mock import MagicMock
from cognitive_data_arcade.engine.i18n import PL, EN
from cognitive_data_arcade.ui.menu import LessonMenuScene


@pytest.fixture(autouse=True)
def _init():
    pygame.font.init()
    yield


def _make(lang="pl", selected=0):
    pm = MagicMock()
    pm.load.return_value = MagicMock(
        alias="Test",
        device_uuid="x",
        music_enabled=True,
        sfx_enabled=True,
        music_volume=1.0,
        sfx_volume=1.0,
        seen_intro=False,
    )
    strings = PL if lang == "pl" else EN
    return LessonMenuScene(pm, strings, selected)


def test_draw_does_not_crash_640():
    pygame.init()
    surface = pygame.Surface((1024, 640))
    scene = _make()
    scene.draw(surface)


def test_draw_does_not_crash_selected_last():
    pygame.init()
    surface = pygame.Surface((1024, 640))
    scene = _make(selected=30)
    scene.draw(surface)


def test_draw_en_does_not_crash():
    pygame.init()
    surface = pygame.Surface((1024, 640))
    scene = _make(lang="en")
    scene.draw(surface)


def test_draw_sets_play_btn_rect():
    pygame.init()
    surface = pygame.Surface((1024, 640))
    scene = _make()
    assert scene._play_btn_rect is None
    scene.draw(surface)
    assert scene._play_btn_rect is not None
    assert scene._play_btn_rect.x >= 341  # must be in panel area


def test_draw_sets_teoria_btn_rect():
    pygame.init()
    surface = pygame.Surface((1024, 640))
    scene = _make()
    scene.draw(surface)
    assert scene._teoria_btn_rect is not None

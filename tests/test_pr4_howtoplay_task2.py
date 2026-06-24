# tests/test_pr4_howtoplay_task2.py
"""
Task 2 — HowToPlay wiring for L12, L21, L22, L27, L31.
Each test verifies that game_factory_for(N, pm, strings)() returns HowToPlayScene
when profile.seen_intro is False.
"""

from __future__ import annotations

import pytest
import pygame
from unittest.mock import MagicMock

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene


@pytest.fixture(autouse=True)
def _pygame():
    pygame.init()
    pygame.display.set_mode((1024, 720))
    yield
    pygame.quit()


def _make_pm(seen_intro: bool = False) -> MagicMock:
    pm = MagicMock()
    pm.load.return_value = MagicMock(
        seen_intro=seen_intro,
        alias="T",
        device_uuid="x",
        music_enabled=True,
        sfx_enabled=True,
        music_volume=1.0,
        sfx_volume=1.0,
    )
    return pm


@pytest.mark.parametrize("lesson_num", [12, 21, 22, 27, 31])
def test_game_factory_returns_howtoplay_when_first_play(lesson_num, tmp_path):
    """game_factory_for(N) must return HowToPlayScene on first play (seen_intro=False)."""
    from cognitive_data_arcade.ui.game_launcher import game_factory_for

    pm = _make_pm(seen_intro=False)
    factory = game_factory_for(lesson_num, pm, EN)
    assert factory is not None, f"No factory for lesson {lesson_num}"
    scene = factory()
    assert isinstance(scene, HowToPlayScene), (
        f"L{lesson_num}: expected HowToPlayScene, got {type(scene).__name__}"
    )


@pytest.mark.parametrize("lesson_num", [21, 22, 27, 31])
def test_game_factory_skips_howtoplay_when_seen_intro(lesson_num, tmp_path):
    """game_factory_for(N) must skip HowToPlayScene when seen_intro=True."""
    from cognitive_data_arcade.engine.pause import PausableGame
    from cognitive_data_arcade.ui.game_launcher import game_factory_for

    pm = _make_pm(seen_intro=True)
    factory = game_factory_for(lesson_num, pm, EN)
    assert factory is not None
    scene = factory()
    assert isinstance(scene, PausableGame), (
        f"L{lesson_num}: expected PausableGame (intro skipped), got {type(scene).__name__}"
    )

from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine import fonts as _fonts_module
from cognitive_data_arcade.engine.i18n import EN


@pytest.fixture(autouse=True)
def pg():
    pygame.init()
    _fonts_module._cache.clear()
    _fonts_module._found_name = None
    yield
    pygame.quit()


def test_l04_factory_returns_how_to_play_when_intro_not_seen(tmp_path):
    from cognitive_data_arcade.profile.manager import ProfileManager
    from cognitive_data_arcade.ui.game_launcher import game_factory_for
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    pm = ProfileManager(tmp_path / "profile.json")
    factory = game_factory_for(4, pm, EN)
    scene = factory()
    assert isinstance(scene, HowToPlayScene)


def test_l04_factory_returns_pausable_when_intro_seen(tmp_path):
    from cognitive_data_arcade.engine.pause import PausableGame
    from cognitive_data_arcade.profile.manager import ProfileManager
    from cognitive_data_arcade.ui.game_launcher import game_factory_for

    pm = ProfileManager(tmp_path / "profile.json")
    p = pm.load()
    p.seen_intro = True
    pm.save(p)
    factory = game_factory_for(4, pm, EN)
    scene = factory()
    assert isinstance(scene, PausableGame)

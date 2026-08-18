"""Baseline tests: game_factory_for_with_back returns a non-None Scene
for every PLAYABLE lesson, using the module-runner calling convention.

These tests run BEFORE the menu refactor (PR #3) and must stay green
throughout.  They document the canonical scene-creation contract and
serve as a regression guard after the menu switches to this path.
"""

from __future__ import annotations

from unittest.mock import MagicMock

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


def _pm(tmp_path, *, seen_intro: bool = True):
    from cognitive_data_arcade.profile.manager import ProfileManager

    pm = ProfileManager(tmp_path / "profile.json")
    p = pm.load()
    p.seen_intro = seen_intro
    pm.save(p)
    return pm


# ── L4 DataCleaning ───────────────────────────────────────────────────────────


def test_l04_with_back_returns_scene_intro_seen(tmp_path):
    from cognitive_data_arcade.ui.game_launcher import game_factory_for_with_back

    back = MagicMock()
    scene = game_factory_for_with_back(4, _pm(tmp_path), EN, back_scene=back)
    assert scene is not None


def test_l04_with_back_returns_scene_intro_not_seen(tmp_path):
    from cognitive_data_arcade.ui.game_launcher import game_factory_for_with_back

    back = MagicMock()
    scene = game_factory_for_with_back(4, _pm(tmp_path, seen_intro=False), EN, back_scene=back)
    assert scene is not None


# ── L6 EDA Sandbox ───────────────────────────────────────────────────────────


def test_l06_with_back_returns_scene(tmp_path):
    from cognitive_data_arcade.ui.game_launcher import game_factory_for_with_back

    back = MagicMock()
    scene = game_factory_for_with_back(6, _pm(tmp_path), EN, back_scene=back)
    assert scene is not None


# ── L13 Distribution Playground ──────────────────────────────────────────────


def test_l13_with_back_returns_scene(tmp_path):
    from cognitive_data_arcade.ui.game_launcher import game_factory_for_with_back

    back = MagicMock()
    scene = game_factory_for_with_back(13, _pm(tmp_path), EN, back_scene=back)
    assert scene is not None


def test_l13_game_factory_callable_and_produces_scene(tmp_path):
    from cognitive_data_arcade.ui.game_launcher import game_factory_for

    factory = game_factory_for(13, _pm(tmp_path), EN)
    assert factory is not None and callable(factory)
    scene = factory()
    assert scene is not None


# ── L14 Correlation Trap ──────────────────────────────────────────────────────


def test_l14_with_back_returns_scene(tmp_path):
    from cognitive_data_arcade.ui.game_launcher import game_factory_for_with_back

    back = MagicMock()
    scene = game_factory_for_with_back(14, _pm(tmp_path), EN, back_scene=back)
    assert scene is not None


def test_l14_game_factory_callable_and_produces_scene(tmp_path):
    from cognitive_data_arcade.ui.game_launcher import game_factory_for

    factory = game_factory_for(14, _pm(tmp_path), EN)
    assert factory is not None and callable(factory)
    scene = factory()
    assert scene is not None


# ── ESC wiring: back_scene surfaces in HowToPlay esc_scene ───────────────────


def test_l13_with_back_injects_esc_scene(tmp_path):
    """When seen_intro=False, game_factory_for_with_back wraps L13 in HowToPlay
    with esc_scene=back, not esc_scene=None."""
    from cognitive_data_arcade.ui.game_launcher import game_factory_for_with_back
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    back = MagicMock()
    scene = game_factory_for_with_back(13, _pm(tmp_path, seen_intro=False), EN, back_scene=back)
    assert isinstance(scene, HowToPlayScene)
    assert scene._esc_scene is back


def test_l14_with_back_injects_esc_scene(tmp_path):
    from cognitive_data_arcade.ui.game_launcher import game_factory_for_with_back
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    back = MagicMock()
    scene = game_factory_for_with_back(14, _pm(tmp_path, seen_intro=False), EN, back_scene=back)
    assert isinstance(scene, HowToPlayScene)
    assert scene._esc_scene is back

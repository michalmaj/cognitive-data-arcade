"""Tests for game_factory_for_with_back: the canonical scene-creation path
used by both the menu and the module runner after PR #3.

The parametrised test at the bottom is the regression guard: every
PLAYABLE lesson must produce a non-None Scene via game_factory_for_with_back.
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


# ── ESC wiring: back_scene is returned when ESC is pressed in HowToPlay ──────


def test_l13_esc_in_howtoplay_navigates_to_back(tmp_path):
    """When seen_intro=False, pressing ESC in the HowToPlay wrapper must
    navigate to back_scene, not to None."""
    from cognitive_data_arcade.ui.game_launcher import game_factory_for_with_back
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    back = MagicMock()
    scene = game_factory_for_with_back(13, _pm(tmp_path, seen_intro=False), EN, back_scene=back)
    assert isinstance(scene, HowToPlayScene)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert scene.is_done()
    assert scene.next_scene() is back


def test_l14_esc_in_howtoplay_navigates_to_back(tmp_path):
    from cognitive_data_arcade.ui.game_launcher import game_factory_for_with_back
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    back = MagicMock()
    scene = game_factory_for_with_back(14, _pm(tmp_path, seen_intro=False), EN, back_scene=back)
    assert isinstance(scene, HowToPlayScene)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert scene.is_done()
    assert scene.next_scene() is back


# ── Restart identity ─────────────────────────────────────────────────────────


def test_l13_restart_creates_new_inner(tmp_path):
    """Restarting L13 (Distribution Playground) must produce a PausableGame
    with a NEW inner scene, not the original object.

    This test checks object identity via _inner because there is no practical
    behavioral alternative: comparing mutable gameplay state post-restart would
    require running two full game sessions. The identity check is the minimal
    proof that restart_factory was called with a fresh closure.
    """
    from cognitive_data_arcade.engine.pause import PausableGame
    from cognitive_data_arcade.ui.game_launcher import game_factory_for_with_back

    back = MagicMock()
    # seen_intro=True → game_factory_for_with_back returns the PausableGame directly
    pausable = game_factory_for_with_back(13, _pm(tmp_path), EN, back_scene=back)
    assert isinstance(pausable, PausableGame), (
        "With seen_intro=True, game_factory_for_with_back(13) should return PausableGame directly"
    )

    original_inner = pausable._inner

    # Trigger restart via public interface: ESC to pause, RETURN on item 0
    pausable.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )
    pausable.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )

    restarted = pausable.next_scene()
    assert isinstance(restarted, PausableGame)
    assert restarted._inner is not original_inner, (
        "restart_factory returned a PausableGame with the SAME inner scene; "
        "score/progress/state would not reset"
    )


# ── Regression guard: all 31 PLAYABLE lessons ────────────────────────────────


from cognitive_data_arcade.engine.lesson_registry import LESSON_REGISTRY, LessonKind  # noqa: E402

_PLAYABLE = [ls for ls in LESSON_REGISTRY if ls.kind == LessonKind.PLAYABLE]


@pytest.mark.parametrize("spec", _PLAYABLE, ids=lambda s: f"L{s.number:02d}_{s.slug}")
def test_all_playable_lessons_produce_scene_via_with_back(spec, tmp_path):
    """game_factory_for_with_back must return a non-None Scene for every PLAYABLE lesson.

    This is the canonical code path used by both the main menu and the
    module runner after PR #3.  A None return means the lesson has no
    game factory branch — a regression that must be caught immediately.
    """
    from unittest.mock import MagicMock

    from cognitive_data_arcade.ui.game_launcher import game_factory_for_with_back

    back = MagicMock()
    pm = _pm(tmp_path)
    scene = game_factory_for_with_back(spec.number, pm, EN, back_scene=back)
    assert scene is not None, (
        f"Lesson {spec.number} ({spec.slug}) is PLAYABLE but "
        f"game_factory_for_with_back returned None"
    )

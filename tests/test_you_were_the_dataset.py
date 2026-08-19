"""Tests for L31 You Were the Dataset."""

from __future__ import annotations

from pathlib import Path


def test_game_state_defaults():
    from cognitive_data_arcade.games.you_were_the_dataset.game_state import GameState

    s = GameState()
    assert s.profile is None
    assert s.current_card == 0


def test_prerequisites_all_present(tmp_path):
    from cognitive_data_arcade.games.you_were_the_dataset.profile_loader import (
        REQUIRED_GAMES,
        check_prerequisites,
    )

    for name in REQUIRED_GAMES:
        d = tmp_path / name
        d.mkdir()
        (d / "session.csv").write_text("col\nval\n")
    result = check_prerequisites(tmp_path)
    assert all(result.values())


def test_prerequisites_some_missing(tmp_path):
    from cognitive_data_arcade.games.you_were_the_dataset.profile_loader import (
        check_prerequisites,
    )

    (tmp_path / "stroop").mkdir()
    (tmp_path / "stroop" / "s.csv").write_text("col\nval\n")
    result = check_prerequisites(tmp_path)
    assert result["stroop"] is True
    assert result["flanker"] is False


def test_rt_percentile_fast():
    from cognitive_data_arcade.games.you_were_the_dataset.profile_loader import _rt_percentile

    assert _rt_percentile(155) >= 90


def test_rt_percentile_slow():
    from cognitive_data_arcade.games.you_were_the_dataset.profile_loader import _rt_percentile

    assert _rt_percentile(560) <= 10


def test_synthetic_profile_is_synthetic():
    from cognitive_data_arcade.games.you_were_the_dataset.synthetic_data import SYNTHETIC_PROFILE

    assert SYNTHETIC_PROFILE.is_synthetic is True
    assert SYNTHETIC_PROFILE.rt_median_ms > 0
    assert 0 <= SYNTHETIC_PROFILE.gono_false_alarm_rate <= 1.0
    assert SYNTHETIC_PROFILE.nback_max_level >= 1


def test_phase_prerequisite_renders():
    import pygame

    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.you_were_the_dataset.game_state import GameState
    from cognitive_data_arcade.games.you_were_the_dataset.phase_prerequisite import (
        PhasePrerequisiteScene,
    )

    state = GameState()
    # Pass empty tmp-like path so all games show as missing (no crash expected)
    scene = PhasePrerequisiteScene(state, game_factories={}, _data_dir=Path("/nonexistent"))
    scene.update(0)
    scene.draw(surface)
    assert not scene.is_done()
    pygame.quit()


def test_phase_reveal_renders():
    import pygame

    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.you_were_the_dataset.game_state import GameState
    from cognitive_data_arcade.games.you_were_the_dataset.phase_reveal import PhaseRevealScene
    from cognitive_data_arcade.games.you_were_the_dataset.synthetic_data import SYNTHETIC_PROFILE

    state = GameState()
    state.profile = SYNTHETIC_PROFILE  # pre-load so no CSV read during test
    scene = PhaseRevealScene(state)
    scene.update(0)
    scene.draw(surface)
    assert not scene.is_done()
    pygame.quit()


def test_phase_profile_renders():
    import pygame

    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.you_were_the_dataset.game_state import GameState
    from cognitive_data_arcade.games.you_were_the_dataset.phase_profile import PhaseProfileScene
    from cognitive_data_arcade.games.you_were_the_dataset.synthetic_data import SYNTHETIC_PROFILE

    state = GameState()
    state.profile = SYNTHETIC_PROFILE
    state.current_card = 0
    scene = PhaseProfileScene(state)
    scene.update(0)
    scene.draw(surface)
    assert not scene.is_done()
    pygame.quit()


def test_phase_connection_renders():
    import pygame

    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.you_were_the_dataset.game_state import GameState
    from cognitive_data_arcade.games.you_were_the_dataset.phase_connection import (
        PhaseConnectionScene,
    )
    from cognitive_data_arcade.games.you_were_the_dataset.synthetic_data import SYNTHETIC_PROFILE

    state = GameState()
    state.profile = SYNTHETIC_PROFILE
    scene = PhaseConnectionScene(state)
    scene.update(0)
    scene.draw(surface)
    assert not scene.is_done()
    pygame.quit()


def test_phase_result_renders():
    import pygame

    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.you_were_the_dataset.game_state import GameState
    from cognitive_data_arcade.games.you_were_the_dataset.phase_result import PhaseResultScene
    from cognitive_data_arcade.games.you_were_the_dataset.synthetic_data import SYNTHETIC_PROFILE

    state = GameState()
    state.profile = SYNTHETIC_PROFILE
    scene = PhaseResultScene(state)
    scene.update(0)
    scene.draw(surface)
    pygame.quit()


def test_menu_has_lesson_31():
    from cognitive_data_arcade.ui.menu import _LESSONS

    nums = [n for n, _ in _LESSONS]
    assert 31 in nums


def test_lesson_31_structure():
    from cognitive_data_arcade.lessons.lesson_31 import CONTENT

    for lang in ("pl", "en"):
        assert len(CONTENT[lang]["theory"]) >= 4
        assert len(CONTENT[lang]["notes"]) >= 2
        assert len(CONTENT[lang]["tasks"]) == 3


def test_game_renders_3_frames():
    from unittest.mock import patch

    import pygame

    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.you_were_the_dataset.game import YouWereTheDatasetScene

    # Patch check_prerequisites so the game starts at PhasePrerequisiteScene
    # (no real CSV read during test — avoids dependency on data/generated/ files)
    _all_missing = {
        "reaction_time": False,
        "stroop": False,
        "flanker": False,
        "gono": False,
        "nback": False,
    }
    with patch(
        "cognitive_data_arcade.games.you_were_the_dataset.game.check_prerequisites",
        return_value=_all_missing,
    ):
        scene = YouWereTheDatasetScene(pm=None, strings=None)
    for _ in range(3):
        scene.update(16)
        scene.draw(surface)
    assert not scene.is_done()
    pygame.quit()

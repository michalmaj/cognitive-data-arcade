# tests/test_flanker.py
from __future__ import annotations

from pathlib import Path

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.games.flanker.config import (
    FULL,
    QUICK,
    STANDARD,
    FlankerConfig,
)
from cognitive_data_arcade.games.flanker.game import FlankerGame, _generate_trials
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.session_summary import SessionSummaryScene


def test_config_defaults() -> None:
    cfg = FlankerConfig()
    assert cfg.num_trials == 48
    assert cfg.trials_per_block == 24
    assert cfg.ap_per_correct == 2


def test_presets_ordering() -> None:
    assert QUICK.num_trials < STANDARD.num_trials < FULL.num_trials


def test_generate_trials_count() -> None:
    cfg = FlankerConfig(num_trials=48)
    trials = _generate_trials(cfg)
    assert len(trials) == 48


def test_generate_trials_equal_condition_split() -> None:
    cfg = FlankerConfig(num_trials=48)
    trials = _generate_trials(cfg)
    congruent = [t for t in trials if t["condition"] == "congruent"]
    incongruent = [t for t in trials if t["condition"] == "incongruent"]
    assert len(congruent) == 24
    assert len(incongruent) == 24


def test_generate_trials_equal_direction_split() -> None:
    cfg = FlankerConfig(num_trials=48)
    trials = _generate_trials(cfg)
    left = [t for t in trials if t["target_direction"] == "left"]
    right = [t for t in trials if t["target_direction"] == "right"]
    assert len(left) == 24
    assert len(right) == 24


def _make_game(tmp_path: Path) -> FlankerGame:
    pm = ProfileManager(tmp_path / "profile.json")
    cfg = FlankerConfig(num_trials=4, trials_per_block=4)
    csv_path = tmp_path / "flanker.csv"
    return FlankerGame(cfg, pm, PL, "test-pid", "test-sid", csv_path)


@pytest.fixture(autouse=True)
def pg() -> None:
    pygame.init()
    yield
    pygame.quit()


def test_initial_not_done(tmp_path: Path) -> None:
    assert not _make_game(tmp_path).is_done()


def test_draw_without_crash(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    surface = pygame.Surface((1024, 768))
    game.draw(surface)


def test_correct_left_response_recorded(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    from cognitive_data_arcade.games.flanker import game as gmod

    game._trials = [{"condition": "congruent", "target_direction": "left"}] * 4
    game._phase = gmod._Phase.STIMULUS
    game._rt_start = pygame.time.get_ticks()
    game.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=0, unicode="")
    )
    assert game._records[0].correct is True
    assert game._records[0].condition == "congruent"


def test_incorrect_response_recorded(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    from cognitive_data_arcade.games.flanker import game as gmod

    game._trials = [{"condition": "incongruent", "target_direction": "left"}] * 4
    game._phase = gmod._Phase.STIMULUS
    game._rt_start = pygame.time.get_ticks()
    game.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT, mod=0, unicode="")
    )
    assert game._records[0].correct is False


def test_next_scene_is_session_summary(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    from cognitive_data_arcade.games.flanker import game as gmod

    game._trials = [{"condition": "congruent", "target_direction": "left"}] * 4
    for _ in range(4):
        game._phase = gmod._Phase.STIMULUS
        game._rt_start = pygame.time.get_ticks()
        game.handle_event(
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=0, unicode="")
        )
        game._phase_timer = game._config.feedback_duration_ms + 1
        game.update(0)
    assert game.is_done()
    assert isinstance(game.next_scene(), SessionSummaryScene)

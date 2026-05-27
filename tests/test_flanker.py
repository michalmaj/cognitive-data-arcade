# tests/test_flanker.py
from __future__ import annotations

from cognitive_data_arcade.games.flanker.config import (
    FULL,
    QUICK,
    STANDARD,
    FlankerConfig,
)
from cognitive_data_arcade.games.flanker.game import _generate_trials


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

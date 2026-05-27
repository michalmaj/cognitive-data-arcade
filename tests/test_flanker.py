# tests/test_flanker.py
from __future__ import annotations

from cognitive_data_arcade.games.flanker.config import (
    FULL,
    QUICK,
    STANDARD,
    FlankerConfig,
)


def test_config_defaults() -> None:
    cfg = FlankerConfig()
    assert cfg.num_trials == 48
    assert cfg.trials_per_block == 24
    assert cfg.ap_per_correct == 2


def test_presets_ordering() -> None:
    assert QUICK.num_trials < STANDARD.num_trials < FULL.num_trials

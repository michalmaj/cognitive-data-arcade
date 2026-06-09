# tests/test_visual_search_config.py
from __future__ import annotations

from cognitive_data_arcade.games.visual_search.config import (
    VSConfig,
    SET_SIZES,
    TRIALS_PER_BLOCK,
    FIXATION_MS,
    FEEDBACK_MS,
    ITI_MS,
    TIMEOUT_MS,
)


def test_set_sizes_ordered() -> None:
    assert SET_SIZES["easy"] < SET_SIZES["medium"] < SET_SIZES["hard"]


def test_trials_per_block_ordered() -> None:
    assert TRIALS_PER_BLOCK["easy"] < TRIALS_PER_BLOCK["medium"] < TRIALS_PER_BLOCK["hard"]


def test_trials_per_block_even() -> None:
    for diff, n in TRIALS_PER_BLOCK.items():
        assert n % 2 == 0, f"{diff}: trials_per_block must be even (50% present, 50% absent)"


def test_vsconfig_defaults() -> None:
    cfg = VSConfig(mode="letters", difficulty="easy")
    assert cfg.set_size == SET_SIZES["easy"]
    assert cfg.trials_per_block == TRIALS_PER_BLOCK["easy"]


def test_vsconfig_medium() -> None:
    cfg = VSConfig(mode="shapes", difficulty="medium")
    assert cfg.set_size == 16
    assert cfg.trials_per_block == 24


def test_timing_constants_positive() -> None:
    assert FIXATION_MS > 0
    assert FEEDBACK_MS > 0
    assert ITI_MS > 0
    assert TIMEOUT_MS > 0

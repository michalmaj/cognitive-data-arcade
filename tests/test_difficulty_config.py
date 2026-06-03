from __future__ import annotations
import dataclasses
import pytest
from cognitive_data_arcade.games.flanker.config import (
    QUICK, STANDARD, FULL,
    DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD,
    FlankerConfig,
)
from cognitive_data_arcade.games.gono.config import (
    QUICK as GONO_QUICK, STANDARD as GONO_STANDARD, FULL as GONO_FULL,
    DIFFICULTY_EASY as GONO_EASY, DIFFICULTY_MEDIUM as GONO_MEDIUM, DIFFICULTY_HARD as GONO_HARD,
    GoNoGoConfig,
)


class TestFlankerDifficultyConfig:
    def test_easy_overrides_stimulus_duration(self):
        cfg = dataclasses.replace(STANDARD, **DIFFICULTY_EASY)
        assert cfg.stimulus_duration_ms == 3000

    def test_easy_preserves_trial_count(self):
        cfg = dataclasses.replace(STANDARD, **DIFFICULTY_EASY)
        assert cfg.num_trials == 48  # STANDARD trial count

    def test_medium_overrides_stimulus_duration(self):
        cfg = dataclasses.replace(QUICK, **DIFFICULTY_MEDIUM)
        assert cfg.stimulus_duration_ms == 2000
        assert cfg.num_trials == 24  # QUICK trial count

    def test_hard_overrides_stimulus_duration(self):
        cfg = dataclasses.replace(FULL, **DIFFICULTY_HARD)
        assert cfg.stimulus_duration_ms == 1000
        assert cfg.num_trials == 96  # FULL trial count

    def test_original_presets_unchanged(self):
        _ = dataclasses.replace(STANDARD, **DIFFICULTY_HARD)
        assert STANDARD.stimulus_duration_ms == 2000  # unchanged

    def test_all_combinations_return_flanker_config(self):
        for preset in [QUICK, STANDARD, FULL]:
            for diff in [DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD]:
                cfg = dataclasses.replace(preset, **diff)
                assert isinstance(cfg, FlankerConfig)


class TestGoNoGoDifficultyConfig:
    def test_easy_overrides_both_fields(self):
        cfg = dataclasses.replace(GONO_STANDARD, **GONO_EASY)
        assert cfg.stimulus_duration_ms == 2000
        assert cfg.go_ratio == 0.80

    def test_easy_preserves_trial_count(self):
        cfg = dataclasses.replace(GONO_STANDARD, **GONO_EASY)
        assert cfg.num_trials == 80

    def test_medium_overrides_both_fields(self):
        cfg = dataclasses.replace(GONO_QUICK, **GONO_MEDIUM)
        assert cfg.stimulus_duration_ms == 1000
        assert cfg.go_ratio == 0.75
        assert cfg.num_trials == 40  # QUICK trial count

    def test_hard_overrides_both_fields(self):
        cfg = dataclasses.replace(GONO_FULL, **GONO_HARD)
        assert cfg.stimulus_duration_ms == 700
        assert cfg.go_ratio == 0.60
        assert cfg.num_trials == 120  # FULL trial count

    def test_original_presets_unchanged(self):
        _ = dataclasses.replace(GONO_STANDARD, **GONO_HARD)
        assert GONO_STANDARD.stimulus_duration_ms == 1000
        assert GONO_STANDARD.go_ratio == 0.75

    def test_all_combinations_return_gono_config(self):
        for preset in [GONO_QUICK, GONO_STANDARD, GONO_FULL]:
            for diff in [GONO_EASY, GONO_MEDIUM, GONO_HARD]:
                cfg = dataclasses.replace(preset, **diff)
                assert isinstance(cfg, GoNoGoConfig)

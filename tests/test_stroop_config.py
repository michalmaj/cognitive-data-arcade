from cognitive_data_arcade.games.stroop.config import (
    COLORS,
    FULL,
    QUICK,
    STANDARD,
    StroopConfig,
)


def test_standard_preset_is_multiple_of_12() -> None:
    assert STANDARD.num_trials % 12 == 0


def test_quick_preset_is_multiple_of_12() -> None:
    assert QUICK.num_trials % 12 == 0


def test_full_preset_is_multiple_of_12() -> None:
    assert FULL.num_trials % 12 == 0


def test_preset_trial_counts() -> None:
    assert QUICK.num_trials == 36
    assert STANDARD.num_trials == 60
    assert FULL.num_trials == 96


def test_colors_has_four_entries() -> None:
    assert len(COLORS) == 4


def test_colors_names() -> None:
    names = [c[1] for c in COLORS]
    assert set(names) == {"red", "green", "blue", "yellow"}


def test_default_config_matches_standard() -> None:
    default = StroopConfig()
    assert default.num_trials == STANDARD.num_trials
    assert default.trials_per_block == STANDARD.trials_per_block

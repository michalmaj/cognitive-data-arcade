from cognitive_data_arcade.games.stroop.config import (
    COLORS,
    EASY,
    HARD,
    MEDIUM,
    STANDARD,
    StroopConfig,
)


def test_easy_preset_has_2_colors() -> None:
    assert EASY.num_colors == 2


def test_medium_preset_has_3_colors() -> None:
    assert MEDIUM.num_colors == 3


def test_hard_preset_has_4_colors() -> None:
    assert HARD.num_colors == 4


def test_all_presets_have_36_trials() -> None:
    assert EASY.num_trials == 36
    assert MEDIUM.num_trials == 36
    assert HARD.num_trials == 36


def test_standard_is_medium_alias() -> None:
    assert STANDARD is MEDIUM


def test_num_trials_divisible_by_block_size() -> None:
    for preset in (EASY, MEDIUM, HARD):
        block_size = preset.num_colors * 3
        assert preset.num_trials % block_size == 0, (
            f"{preset} num_trials={preset.num_trials} not divisible by block_size={block_size}"
        )


def test_colors_has_four_entries() -> None:
    assert len(COLORS) == 4


def test_colors_names() -> None:
    names = [c[1] for c in COLORS]
    assert set(names) == {"red", "green", "blue", "yellow"}


def test_default_config_matches_medium() -> None:
    default = StroopConfig()
    assert default.num_trials == MEDIUM.num_trials
    assert default.trials_per_block == MEDIUM.trials_per_block
    assert default.num_colors == MEDIUM.num_colors

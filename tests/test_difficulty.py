from __future__ import annotations

import pytest
from cognitive_data_arcade.games.data_cleaning.difficulty import (
    DifficultyConfig,
    EASY,
    MEDIUM,
    HARD,
    ALL_DIFFICULTIES,
)


def test_easy_fields():
    assert EASY.rows == 15
    assert EASY.errors_min == 3
    assert EASY.errors_max == 6
    assert EASY.hints_mode == "always"


def test_medium_fields():
    assert MEDIUM.rows == 50
    assert MEDIUM.errors_min == 15
    assert MEDIUM.errors_max == 20
    assert MEDIUM.hints_mode == "toggle"


def test_hard_fields():
    assert HARD.rows == 100
    assert HARD.errors_min == 25
    assert HARD.errors_max == 40
    assert HARD.hints_mode == "none"


def test_all_difficulties_has_three():
    assert len(ALL_DIFFICULTIES) == 3


def test_config_is_frozen():
    with pytest.raises((AttributeError, TypeError)):
        EASY.rows = 99  # type: ignore[misc]


def test_hints_mode_values_are_valid():
    valid = {"always", "toggle", "none"}
    for d in ALL_DIFFICULTIES:
        assert d.hints_mode in valid

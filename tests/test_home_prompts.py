# tests/test_home_prompts.py
from __future__ import annotations

import pytest

from cognitive_data_arcade.data.home_prompts import HOME_PROMPTS


@pytest.mark.parametrize("module_idx", [0, 1, 2, 3, 4, 5])
def test_all_modules_present(module_idx: int) -> None:
    assert module_idx in HOME_PROMPTS


@pytest.mark.parametrize("module_idx", [0, 1, 2, 3, 4, 5])
def test_both_languages_present(module_idx: int) -> None:
    entry = HOME_PROMPTS[module_idx]
    assert "pl" in entry
    assert "en" in entry


@pytest.mark.parametrize("module_idx", [0, 1, 2, 3, 4, 5])
def test_no_empty_strings(module_idx: int) -> None:
    entry = HOME_PROMPTS[module_idx]
    assert entry["pl"].strip()
    assert entry["en"].strip()

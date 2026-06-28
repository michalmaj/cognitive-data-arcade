from __future__ import annotations

import pytest


def _assert_reflection(mod_name: str) -> None:
    import importlib

    mod = importlib.import_module(f"cognitive_data_arcade.lessons.{mod_name}")
    r = mod.REFLECTION
    for lang in ("pl", "en"):
        assert lang in r, f"{mod_name}.REFLECTION missing '{lang}'"
        d = r[lang]
        assert "title" in d
        assert "cards" in d
        assert len(d["cards"]) == 3, f"{mod_name}.REFLECTION[{lang}]['cards'] must have 3 items"
        for card in d["cards"]:
            assert "label" in card
            assert "color" in card
            assert card["color"] in ("indigo", "orange", "green")
            assert "text" in card
        assert "question" in d


@pytest.mark.parametrize(
    "mod_name",
    [
        "lesson_01",
        "lesson_03",
        "lesson_04",
        "lesson_06",
        "lesson_13",
        "lesson_14",
        "lesson_15",
        "lesson_16",
        "lesson_17",
        "lesson_18",
        "lesson_19",
        "lesson_20",
    ],
)
def test_reflection_dict_structure(mod_name: str) -> None:
    _assert_reflection(mod_name)

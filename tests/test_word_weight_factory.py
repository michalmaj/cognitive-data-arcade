from __future__ import annotations
import string as _string

from cognitive_data_arcade.games.word_weight_factory.corpus import (
    PRESET_STROOP_PL,
    PRESET_NBACK_EN,
    PRESET_FLANKER_PL,
    PRESET_MEMORY_EN,
    CorpusState,
)


def test_presets_non_empty():
    for text in [PRESET_STROOP_PL, PRESET_NBACK_EN, PRESET_FLANKER_PL, PRESET_MEMORY_EN]:
        assert len(text.strip()) > 0


def test_presets_ascii_only():
    printable = set(_string.printable)
    for text in [PRESET_STROOP_PL, PRESET_NBACK_EN, PRESET_FLANKER_PL, PRESET_MEMORY_EN]:
        bad = [c for c in text if c not in printable]
        assert bad == [], f"Non-ASCII chars found: {bad}"

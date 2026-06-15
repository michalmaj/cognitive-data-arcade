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


def test_active_docs_default_returns_four():
    state = CorpusState()
    assert len(state.active_docs()) == 4


def test_active_docs_with_custom_returns_five():
    state = CorpusState(custom_text="hello world test")
    docs = state.active_docs()
    assert len(docs) == 5
    assert docs[-1][0] == "Wlasny"

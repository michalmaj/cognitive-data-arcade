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


import math
from cognitive_data_arcade.games.word_weight_factory.engine import WeightEngine, WeightMatrix


def _engine() -> WeightEngine:
    return WeightEngine()


def test_engine_bow_counts():
    m = _engine().process(
        docs=["czas reakcji czas", "czas pamiec"],
        titles=["D1", "D2"],
        lowercase=True, rm_punct=False, rm_stops=False, lang="pl",
    )
    idx_czas = m.vocab.index("czas")
    assert m.bow[0][idx_czas] == 2
    assert m.bow[1][idx_czas] == 1
    idx_r = m.vocab.index("reakcji")
    assert m.bow[0][idx_r] == 1
    assert m.bow[1][idx_r] == 0


def test_engine_tf_sums():
    m = _engine().process(
        docs=["a b c", "a a b"],
        titles=["D1", "D2"],
        lowercase=True, rm_punct=False, rm_stops=False, lang="en",
    )
    # TF values for each doc must sum to <= 1.0
    for row in m.tf:
        assert sum(row) <= 1.0 + 1e-9


def test_engine_idf_ordering():
    # "czas" appears in both docs → lower IDF than "reakcji" (only in D1)
    m = _engine().process(
        docs=["czas reakcji", "czas pamiec"],
        titles=["D1", "D2"],
        lowercase=True, rm_punct=False, rm_stops=False, lang="pl",
    )
    idx_czas = m.vocab.index("czas")
    idx_r = m.vocab.index("reakcji")
    assert m.idf[idx_czas] < m.idf[idx_r]


def test_engine_tfidf_formula():
    m = _engine().process(
        docs=["czas reakcji", "czas pamiec"],
        titles=["D1", "D2"],
        lowercase=True, rm_punct=False, rm_stops=False, lang="pl",
    )
    for i in range(len(m.doc_titles)):
        for j in range(len(m.vocab)):
            expected = m.tf[i][j] * m.idf[j]
            assert abs(m.tfidf[i][j] - expected) < 1e-9


def test_engine_empty_corpus():
    m = _engine().process(
        docs=[], titles=[], lowercase=True, rm_punct=True, rm_stops=False, lang="pl",
    )
    assert m.vocab == []
    assert m.bow == []
    assert m.tfidf == []


def test_engine_single_doc_idf_zero():
    # With N=1, idf = log((1+1)/(1+1)) = log(1) = 0 for every token
    m = _engine().process(
        docs=["czas reakcji"], titles=["D1"],
        lowercase=True, rm_punct=False, rm_stops=False, lang="pl",
    )
    for v in m.idf:
        assert abs(v) < 1e-9
    for row in m.tfidf:
        for v in row:
            assert abs(v) < 1e-9


def test_engine_vocab_sorted():
    m = _engine().process(
        docs=["zebra alpha mango"],
        titles=["D1"],
        lowercase=True, rm_punct=False, rm_stops=False, lang="en",
    )
    assert m.vocab == sorted(m.vocab)


import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame


def test_step_idf_scene_renders():
    pygame.init()
    pygame.display.set_mode((804, 672))
    from cognitive_data_arcade.games.word_weight_factory.corpus import CorpusState
    from cognitive_data_arcade.games.word_weight_factory.engine import WeightEngine
    from cognitive_data_arcade.games.word_weight_factory.step_idf import StepIdfScene
    state = CorpusState()
    scene = StepIdfScene(state)
    docs = state.active_docs()
    matrix = WeightEngine().process(
        docs=[t for _, t in docs],
        titles=[ti for ti, _ in docs],
        lowercase=True, rm_punct=True, rm_stops=False, lang="pl",
    )
    surface = pygame.Surface((804, 672))
    scene.draw(surface, matrix)  # must not raise
    pygame.quit()

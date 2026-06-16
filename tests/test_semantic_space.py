from __future__ import annotations


def test_words_all_in_valid_clusters():
    from cognitive_data_arcade.games.semantic_space.word_data import WORDS, CLUSTERS
    for key, wd in WORDS.items():
        assert wd["cluster"] in CLUSTERS, f"{key} has unknown cluster {wd['cluster']}"


def test_coordinates_in_range():
    from cognitive_data_arcade.games.semantic_space.word_data import WORDS
    for key, wd in WORDS.items():
        assert 0.0 <= wd["x"] <= 1.0, f"{key} x={wd['x']} out of range"
        assert 0.0 <= wd["y"] <= 1.0, f"{key} y={wd['y']} out of range"


def test_similarities_all_50():
    from cognitive_data_arcade.games.semantic_space.word_data import WORDS, SIMILARITIES
    assert len(SIMILARITIES) == len(WORDS)
    for key in WORDS:
        assert key in SIMILARITIES, f"{key} missing from SIMILARITIES"
        assert len(SIMILARITIES[key]) == 8


def test_similarities_keys_exist():
    from cognitive_data_arcade.games.semantic_space.word_data import WORDS, SIMILARITIES
    for word, neighbors in SIMILARITIES.items():
        for neighbor_key, sim in neighbors:
            assert neighbor_key in WORDS, f"neighbor {neighbor_key!r} not in WORDS"
            assert 0.0 <= sim <= 1.0, f"sim {sim} out of range for {word}->{neighbor_key}"


def test_analogies_structure():
    from cognitive_data_arcade.games.semantic_space.word_data import ANALOGIES
    assert len(ANALOGIES) == 4
    for tup in ANALOGIES:
        assert len(tup) == 7, f"Expected 7-tuple, got {len(tup)}"
        a, b, c, answer, distractors, expl_pl, expl_en = tup
        assert isinstance(distractors, list) and len(distractors) == 3
        assert isinstance(expl_pl, str) and expl_pl
        assert isinstance(expl_en, str) and expl_en


def test_bridge_words_reference_valid_clusters():
    from cognitive_data_arcade.games.semantic_space.word_data import BRIDGE_WORDS, CLUSTERS, WORDS
    for word_key, clusters, difficulty in BRIDGE_WORDS:
        assert word_key in WORDS, f"{word_key} not in WORDS"
        for c in clusters:
            assert c in CLUSTERS, f"{c} not a valid cluster"
        assert difficulty in (2, 3)

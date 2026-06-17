from __future__ import annotations

import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


def test_topics_have_enough_words():
    from cognitive_data_arcade.games.topic_detective.topic_data import TOPICS
    for key, td in TOPICS.items():
        assert len(td["words"]) >= 10, f"{key} has only {len(td['words'])} words"


def test_documents_weights_sum_to_one():
    from cognitive_data_arcade.games.topic_detective.topic_data import DOCUMENTS
    for i, doc in enumerate(DOCUMENTS):
        total = sum(doc["weights"].values())
        assert abs(total - 1.0) <= 0.01, f"doc {i} weights sum to {total}"


def test_documents_dominant_is_max_weight():
    from cognitive_data_arcade.games.topic_detective.topic_data import DOCUMENTS
    for i, doc in enumerate(DOCUMENTS):
        max_key = max(doc["weights"], key=doc["weights"].__getitem__)
        assert doc["dominant"] == max_key, (
            f"doc {i}: dominant={doc['dominant']} but max weight is {max_key}"
        )


def test_intruder_not_in_topic_words():
    from cognitive_data_arcade.games.topic_detective.topic_data import INTRUDER_SETS, TOPICS
    for s in INTRUDER_SETS:
        topic_words = TOPICS[s["topic"]]["words"]
        assert s["intruder"] not in topic_words, (
            f"intruder '{s['intruder']}' found in topic '{s['topic']}' words"
        )


def test_intruder_sets_count():
    from cognitive_data_arcade.games.topic_detective.topic_data import INTRUDER_SETS
    assert len(INTRUDER_SETS) == 8

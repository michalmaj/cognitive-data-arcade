# tests/test_emotion_classifier.py
from __future__ import annotations


def test_lexicon_classify_positive():
    from cognitive_data_arcade.games.emotion_classifier.lexicon import classify
    verdict, total = classify({"znakomite": 2, "zadowoleni": 1})
    assert verdict == "positive"
    assert total == 3


def test_lexicon_classify_negative():
    from cognitive_data_arcade.games.emotion_classifier.lexicon import classify
    verdict, total = classify({"porazka": -2, "fatalne": -2})
    assert verdict == "negative"
    assert total == -4


def test_lexicon_classify_neutral():
    from cognitive_data_arcade.games.emotion_classifier.lexicon import classify
    verdict, total = classify({"dobry": 1, "blad": -1})
    assert verdict == "neutral"
    assert total == 0


def test_classify_empty_returns_neutral():
    from cognitive_data_arcade.games.emotion_classifier.lexicon import classify
    verdict, total = classify({})
    assert verdict == "neutral"
    assert total == 0


def test_compute_round_score_correct_positive_tag():
    from cognitive_data_arcade.games.emotion_classifier.lexicon import compute_round_score
    # Player tagged "znakomite" as positive → matches lexicon score +2
    pts, neg, beat, speed = compute_round_score(
        tagged_words={"znakomite": "positive"},
        word_scores={"znakomite": 2},
        truth="positive",
        elapsed_s=10.0,
    )
    assert pts == 5
    assert neg == 0
    assert beat == 0   # lexicon also says positive == truth → no beat bonus
    assert speed == 5  # < 15s


def test_compute_round_score_wrong_tag():
    from cognitive_data_arcade.games.emotion_classifier.lexicon import compute_round_score
    pts, neg, beat, speed = compute_round_score(
        tagged_words={"znakomite": "negative"},  # wrong
        word_scores={"znakomite": 2},
        truth="positive",
        elapsed_s=20.0,
    )
    assert pts == 0
    assert neg == -2
    assert speed == 0  # >= 15s


def test_compute_round_score_beat_bonus():
    from cognitive_data_arcade.games.emotion_classifier.lexicon import compute_round_score
    # Sentence truth=neutral, lexicon sees "zadowoleni" (+1) → says positive
    # Player tagged no words → player verdict=neutral (empty) → matches truth → beat!
    pts, neg, beat, speed = compute_round_score(
        tagged_words={},
        word_scores={"zadowoleni": 1},
        truth="neutral",
        elapsed_s=5.0,
    )
    assert beat == 15
    assert speed == 5  # elapsed_s=5.0 < 15.0


def test_trap_labels_all_five():
    from cognitive_data_arcade.games.emotion_classifier.lexicon import TRAP_LABELS
    for key in ("clear_pos", "clear_neg", "negation", "intensity", "irony", "mixed"):
        assert key in TRAP_LABELS


def test_trap_hints_all_five():
    from cognitive_data_arcade.games.emotion_classifier.lexicon import TRAP_HINTS
    for key in ("clear_pos", "clear_neg", "negation", "intensity", "irony", "mixed"):
        assert key in TRAP_HINTS
        assert TRAP_HINTS[key]  # non-empty string

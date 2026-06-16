# tests/test_emotion_classifier.py
from __future__ import annotations


def test_lexicon_classify_positive():
    from cognitive_data_arcade.games.emotion_classifier.lexicon import classify
    verdict, total = classify({"znakomite": 2, "zadowoleni": 1})
    assert verdict == "positive"
    assert total == 3


def test_lexicon_classify_negative():
    from cognitive_data_arcade.games.emotion_classifier.lexicon import classify
    verdict, total = classify({"porażka": -2, "fatalne": -2})
    assert verdict == "negative"
    assert total == -4


def test_lexicon_classify_neutral():
    from cognitive_data_arcade.games.emotion_classifier.lexicon import classify
    verdict, total = classify({"dobry": 1, "błąd": -1})
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


def test_sentence_bank_non_empty():
    from cognitive_data_arcade.games.emotion_classifier.sentences import SENTENCE_BANK
    assert len(SENTENCE_BANK) >= 40



def test_chip_tokens_cover_word_scores_keys():
    from cognitive_data_arcade.games.emotion_classifier.sentences import SENTENCE_BANK
    for s in SENTENCE_BANK:
        tokens = {tok.rstrip('.,;:!?').lower() for tok in s.text.split()}
        for key in s.word_scores:
            assert key in tokens, (
                f"word_scores key '{key}' not found as chip token in: {s.text}"
            )


def test_sentence_bank_trap_types():
    from cognitive_data_arcade.games.emotion_classifier.sentences import SENTENCE_BANK
    traps = {s.trap for s in SENTENCE_BANK}
    assert traps >= {"clear_pos", "clear_neg", "negation", "intensity", "irony", "mixed"}


def test_sentence_bank_truth_values():
    from cognitive_data_arcade.games.emotion_classifier.sentences import SENTENCE_BANK
    valid = {"positive", "negative", "neutral", "mixed"}
    for s in SENTENCE_BANK:
        assert s.truth in valid, f"Bad truth '{s.truth}' in: {s.text}"


def test_session_draw_8_no_repeat():
    from cognitive_data_arcade.games.emotion_classifier.sentences import SENTENCE_BANK, draw_session
    session = draw_session(SENTENCE_BANK)
    assert len(session) == 8
    texts = [s.text for s in session]
    assert len(texts) == len(set(texts)), "Duplicate sentence in session"


def test_session_draw_first_two_clear():
    from cognitive_data_arcade.games.emotion_classifier.sentences import SENTENCE_BANK, draw_session
    for _ in range(10):  # random draw, repeat to be sure
        session = draw_session(SENTENCE_BANK)
        assert session[0].trap == "clear_pos"
        assert session[1].trap == "clear_neg"


import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


def _pygame():
    import pygame
    pygame.init()
    return pygame


def test_phase_intro_scene_renders():
    pg = _pygame()
    from cognitive_data_arcade.games.emotion_classifier.phase_intro import PhaseIntroScene
    scene = PhaseIntroScene()
    surf = pg.Surface((1024, 720))
    assert not scene.is_done()
    scene.draw(surf)  # must not raise
    assert scene.next_scene() is None


def test_calc_stats_groups_clear():
    from cognitive_data_arcade.games.emotion_classifier.phase_session_result import _calc_stats
    results = [
        {"trap": "clear_pos", "beat_lexicon": True},
        {"trap": "clear_neg", "beat_lexicon": False},
        {"trap": "negation", "beat_lexicon": True},
    ]
    stats = _calc_stats(results)
    assert stats["clear"] == (1, 2)
    assert stats["negation"] == (1, 1)
    assert stats["intensity"] == (0, 0)


def test_calc_stats_empty():
    from cognitive_data_arcade.games.emotion_classifier.phase_session_result import _calc_stats
    stats = _calc_stats([])
    for cat in ("clear", "negation", "intensity", "irony", "mixed"):
        assert stats[cat] == (0, 0)


def test_phase_session_result_renders():
    pg = _pygame()
    from cognitive_data_arcade.games.emotion_classifier.phase_session_result import PhaseSessionResultScene
    round_results = [
        {"trap": "clear_pos", "beat_lexicon": True},
        {"trap": "negation", "beat_lexicon": False},
    ]
    scene = PhaseSessionResultScene(session_score=75, round_results=round_results)
    surf = pg.Surface((1024, 720))
    assert not scene.is_done()
    scene.draw(surf)  # must not raise
    assert scene.next_scene() is None


def test_emotion_classifier_scene_instantiates():
    _pygame()
    from cognitive_data_arcade.games.emotion_classifier.game import EmotionClassifierScene
    scene = EmotionClassifierScene()
    assert not scene.is_done()
    assert scene.next_scene() is None


def test_lesson_23_content_structure():
    from cognitive_data_arcade.lessons.lesson_23 import CONTENT
    for lang in ("pl", "en"):
        assert lang in CONTENT
        for key in ("theory", "notes", "tasks"):
            assert key in CONTENT[lang]
            assert len(CONTENT[lang][key]) >= 2


def test_menu_has_lesson_23():
    from cognitive_data_arcade.ui.menu import _LESSONS
    lesson_nums = [n for n, _ in _LESSONS]
    assert 23 in lesson_nums

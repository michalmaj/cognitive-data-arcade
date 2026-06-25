"""Tests for act content data — narrative texts and quiz questions."""

from cognitive_data_arcade.data.act_content import ACT_INTROS, ACT_BRIDGES
from cognitive_data_arcade.data.quiz_data import QUIZ_QUESTIONS, get_question


def test_act_intros_has_6_entries() -> None:
    assert len(ACT_INTROS) == 6


def test_act_intros_have_required_keys() -> None:
    for i, entry in enumerate(ACT_INTROS):
        assert "title_pl" in entry, f"Act {i} missing title_pl"
        assert "title_en" in entry, f"Act {i} missing title_en"
        assert "text_pl" in entry, f"Act {i} missing text_pl"
        assert "text_en" in entry, f"Act {i} missing text_en"


def test_act_bridges_has_6_entries() -> None:
    assert len(ACT_BRIDGES) == 6


def test_act_bridges_have_pl_and_en() -> None:
    for i, entry in enumerate(ACT_BRIDGES):
        assert "text_pl" in entry, f"Bridge {i} missing text_pl"
        assert "text_en" in entry, f"Bridge {i} missing text_en"


def test_quiz_questions_covers_all_lessons() -> None:
    expected = {
        1,
        2,
        3,
        4,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
    }
    assert set(QUIZ_QUESTIONS.keys()) == expected


def test_each_question_has_required_fields() -> None:
    for lesson_num, q in QUIZ_QUESTIONS.items():
        assert "q_pl" in q, f"L{lesson_num} missing q_pl"
        assert "q_en" in q, f"L{lesson_num} missing q_en"
        assert "options_pl" in q and len(q["options_pl"]) == 3, f"L{lesson_num} options_pl"
        assert "options_en" in q and len(q["options_en"]) == 3, f"L{lesson_num} options_en"
        assert "correct" in q and q["correct"] in (0, 1, 2), f"L{lesson_num} correct"


def test_get_question_returns_dict_for_known_lesson() -> None:
    q = get_question(2)
    assert q is not None
    assert "q_pl" in q


def test_get_question_returns_none_for_unknown() -> None:
    assert get_question(999) is None

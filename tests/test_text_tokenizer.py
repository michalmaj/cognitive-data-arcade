import pytest


def test_stop_words_pl_nonempty():
    from cognitive_data_arcade.games.text_tokenizer.stop_words import STOP_WORDS_PL
    assert len(STOP_WORDS_PL) >= 20


def test_stop_words_en_nonempty():
    from cognitive_data_arcade.games.text_tokenizer.stop_words import STOP_WORDS_EN
    assert len(STOP_WORDS_EN) >= 20


def test_stop_words_disjoint():
    from cognitive_data_arcade.games.text_tokenizer.stop_words import STOP_WORDS_PL, STOP_WORDS_EN
    assert STOP_WORDS_PL.isdisjoint(STOP_WORDS_EN)


def test_stop_words_are_frozensets():
    from cognitive_data_arcade.games.text_tokenizer.stop_words import STOP_WORDS_PL, STOP_WORDS_EN
    assert isinstance(STOP_WORDS_PL, frozenset)
    assert isinstance(STOP_WORDS_EN, frozenset)

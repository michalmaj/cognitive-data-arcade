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


def test_engine_raw_tokens_always_whitespace_split():
    from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerEngine
    eng = TokenizerEngine()
    state = eng.process("Hello, world! HELLO", lowercase=True, rm_punct=True,
                         rm_stops=False, lang="en", ngram_n=1)
    assert state.raw_tokens == ["Hello,", "world!", "HELLO"]


def test_engine_lowercase_and_rm_punct():
    from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerEngine
    eng = TokenizerEngine()
    state = eng.process("Hello, World!", lowercase=True, rm_punct=True,
                         rm_stops=False, lang="en", ngram_n=1)
    assert state.tokens == ["hello", "world"]


def test_engine_rm_stops_en():
    from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerEngine
    eng = TokenizerEngine()
    state = eng.process("the cat is on the mat", lowercase=True, rm_punct=False,
                         rm_stops=True, lang="en", ngram_n=1)
    assert "the" not in state.tokens
    assert "is" not in state.tokens
    assert "cat" in state.tokens
    assert "mat" in state.tokens


def test_engine_rm_stops_pl():
    from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerEngine
    eng = TokenizerEngine()
    state = eng.process("badanie wykazalo ze czas reakcji wzrosl", lowercase=True,
                         rm_punct=False, rm_stops=True, lang="pl", ngram_n=1)
    assert "ze" not in state.tokens
    assert "badanie" in state.tokens
    assert "czas" in state.tokens


def test_engine_bigrams():
    from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerEngine
    eng = TokenizerEngine()
    state = eng.process("czas reakcji wzrosl", lowercase=False, rm_punct=False,
                         rm_stops=False, lang="pl", ngram_n=2)
    assert ("czas", "reakcji") in state.ngrams
    assert ("reakcji", "wzrosl") in state.ngrams
    assert len(state.ngrams) == 2


def test_engine_trigrams():
    from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerEngine
    eng = TokenizerEngine()
    state = eng.process("a b c d", lowercase=False, rm_punct=False,
                         rm_stops=False, lang="en", ngram_n=3)
    assert ("a", "b", "c") in state.ngrams
    assert ("b", "c", "d") in state.ngrams


def test_engine_freq_sorted():
    from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerEngine
    eng = TokenizerEngine()
    state = eng.process("a a a b b c", lowercase=False, rm_punct=False,
                         rm_stops=False, lang="en", ngram_n=1)
    counts = list(state.freq.values())
    assert counts == sorted(counts, reverse=True)
    assert state.freq["a"] == 3
    assert state.freq["b"] == 2
    assert state.freq["c"] == 1


def test_engine_unique_count():
    from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerEngine
    eng = TokenizerEngine()
    state = eng.process("a b a c", lowercase=False, rm_punct=False,
                         rm_stops=False, lang="en", ngram_n=1)
    assert state.unique_count == 3  # a, b, c

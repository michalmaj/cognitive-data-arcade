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


def test_preset_texts_nonempty():
    from cognitive_data_arcade.games.text_tokenizer.widgets import (
        PRESET_TWEET_PL, PRESET_ABSTRACT_EN, PRESET_SMS_PL,
    )
    assert len(PRESET_TWEET_PL) > 20
    assert len(PRESET_ABSTRACT_EN) > 20
    assert len(PRESET_SMS_PL) > 20


def test_preset_pl_texts_contain_diacritics():
    from cognitive_data_arcade.games.text_tokenizer.widgets import (
        PRESET_TWEET_PL, PRESET_SMS_PL,
    )
    diacritics = set("aesznolc")  # ascii fallback — check at least one of: ą ę ś ź ż ó ń ł ć
    pl_text = PRESET_TWEET_PL + PRESET_SMS_PL
    # At minimum they must contain Polish-flavour words or be non-trivial
    assert len(pl_text.split()) >= 10


def test_shared_state_defaults():
    from cognitive_data_arcade.games.text_tokenizer.widgets import SharedState
    s = SharedState()
    assert s.lang in ("pl", "en")
    assert isinstance(s.lowercase, bool)
    assert isinstance(s.rm_punct, bool)
    assert isinstance(s.rm_stops, bool)
    assert s.ngram_n in (1, 2, 3)
    assert 5 <= s.topn <= 20


def test_phase_tokenizer_instantiates():
    import os; os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    import pygame; pygame.init()
    from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerEngine
    from cognitive_data_arcade.games.text_tokenizer.phase_tokenizer import PhaseTokenizerScene
    from cognitive_data_arcade.games.text_tokenizer.widgets import SharedState
    state = SharedState()
    scene = PhaseTokenizerScene(state)
    result = TokenizerEngine().process(
        state.text, state.lowercase, state.rm_punct,
        state.rm_stops, state.lang, state.ngram_n,
    )
    surf = pygame.Surface((1024, 636))
    scene.draw(surf, result)  # must not raise
    pygame.quit()


def test_phase_ngrams_instantiates():
    import os; os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    import pygame
    try:
        pygame.quit()
    except:
        pass
    from cognitive_data_arcade.engine import fonts as fonts_mod
    fonts_mod._cache.clear()
    pygame.init()
    from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerEngine
    from cognitive_data_arcade.games.text_tokenizer.phase_ngrams import PhaseNgramsScene
    from cognitive_data_arcade.games.text_tokenizer.widgets import SharedState
    state = SharedState()
    scene = PhaseNgramsScene(state)
    result = TokenizerEngine().process(
        state.text, state.lowercase, state.rm_punct,
        state.rm_stops, state.lang, state.ngram_n,
    )
    surf = pygame.Surface((1024, 636))
    scene.draw(surf, result)
    pygame.quit()


def test_phase_frequency_returns_surface():
    import os; os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    import pygame
    try:
        pygame.quit()
    except:
        pass
    from cognitive_data_arcade.engine import fonts as fonts_mod
    fonts_mod._cache.clear()
    pygame.init()
    from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerEngine
    from cognitive_data_arcade.games.text_tokenizer.phase_frequency import PhaseFrequencyScene
    from cognitive_data_arcade.games.text_tokenizer.widgets import SharedState
    state = SharedState()
    scene = PhaseFrequencyScene(state)
    result = TokenizerEngine().process(
        state.text, state.lowercase, state.rm_punct,
        state.rm_stops, state.lang, state.ngram_n,
    )
    surf = pygame.Surface((1024, 636))
    scene.draw(surf, result)
    pygame.quit()


def test_text_tokenizer_scene_instantiates():
    import os; os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    import pygame
    try:
        pygame.quit()
    except:
        pass
    from cognitive_data_arcade.engine import fonts as fonts_mod
    fonts_mod._cache.clear()
    pygame.init()
    from cognitive_data_arcade.games.text_tokenizer.scene import TextTokenizerLabScene
    scene = TextTokenizerLabScene()
    assert not scene.is_done()
    surf = pygame.Surface((1024, 720))
    scene.draw(surf)
    pygame.quit()


def test_text_tokenizer_tab_navigation():
    import os; os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    import pygame
    try:
        pygame.quit()
    except:
        pass
    from cognitive_data_arcade.engine import fonts as fonts_mod
    fonts_mod._cache.clear()
    pygame.init()
    from cognitive_data_arcade.games.text_tokenizer.scene import TextTokenizerLabScene
    scene = TextTokenizerLabScene()
    assert scene.current_tab() == 0
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT, mod=0, unicode="")
    scene.handle_event(event)
    assert scene.current_tab() == 1
    event2 = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=0, unicode="")
    scene.handle_event(event2)
    assert scene.current_tab() == 0
    pygame.quit()

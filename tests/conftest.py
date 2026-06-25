import os

import pytest

# Must be set before any pygame import so tests run without a display.
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"


@pytest.fixture(autouse=True)
def _reset_font_cache():
    from cognitive_data_arcade.engine import fonts

    fonts.reset()
    yield


@pytest.fixture(autouse=True)
def _mock_audio(monkeypatch):
    """Prevent real pygame.mixer calls during tests.

    Multiple pygame.init()/quit() cycles across test files leave stale
    Sound objects in audio._sfx.  Calling .play() on a stale Sound after
    a mixer restart causes a C-level SIGSEGV that pytest cannot catch.
    Stubbing the three public audio helpers avoids the crash without
    affecting any game-logic assertions.
    """
    import cognitive_data_arcade.engine.audio as _audio

    monkeypatch.setattr(_audio, "play_sfx", lambda *_a, **_kw: None)

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

from __future__ import annotations
import pytest
import pygame
from pathlib import Path
from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager


@pytest.fixture(autouse=True)
def pg():
    pygame.init()
    pygame.display.set_mode((1024, 720))
    yield
    pygame.quit()


@pytest.fixture()
def pm(tmp_path: Path) -> ProfileManager:
    p = ProfileManager(tmp_path / "profile.json")
    p.load()
    return p


def _right():
    return pygame.event.Event(
        pygame.KEYDOWN, {"key": pygame.K_RIGHT, "mod": 0, "unicode": "", "scancode": 0}
    )


def _left():
    return pygame.event.Event(
        pygame.KEYDOWN, {"key": pygame.K_LEFT, "mod": 0, "unicode": "", "scancode": 0}
    )


def test_initial_phase_idx(pm):
    from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene

    s = PredictionSliderScene(pm, PL)
    assert s._phase_idx == 0


def test_right_key_advances(pm):
    from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene

    s = PredictionSliderScene(pm, PL)
    s.handle_event(_right())
    assert s._phase_idx == 1
    s.handle_event(_right())
    assert s._phase_idx == 2
    s.handle_event(_right())
    assert s._phase_idx == 0


def test_left_key_wraps(pm):
    from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene

    s = PredictionSliderScene(pm, PL)
    s.handle_event(_left())
    assert s._phase_idx == 2


def test_is_done_false(pm):
    from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene

    s = PredictionSliderScene(pm, PL)
    assert s.is_done() is False


def test_next_scene_none(pm):
    from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene

    s = PredictionSliderScene(pm, PL)
    assert s.next_scene() is None


def test_mouse_event_offset(pm):
    from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene

    s = PredictionSliderScene(pm, PL)
    ev = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (200, 300), "touch": False}
    )
    offset = s._offset_mouse_event(ev, dy=-48)
    assert offset.pos == (200, 252)

from __future__ import annotations
import pytest
import pygame


@pytest.fixture(autouse=True)
def pg():
    pygame.init()
    pygame.display.set_mode((1024, 720))
    yield
    pygame.quit()


def _right():
    return pygame.event.Event(pygame.KEYDOWN,
        {"key": pygame.K_RIGHT, "mod": 0, "unicode": "", "scancode": 0})

def _left():
    return pygame.event.Event(pygame.KEYDOWN,
        {"key": pygame.K_LEFT, "mod": 0, "unicode": "", "scancode": 0})


def test_initial_phase_idx():
    from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene
    s = PredictionSliderScene()
    assert s._phase_idx == 0


def test_right_key_advances():
    from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene
    s = PredictionSliderScene()
    s.handle_event(_right())
    assert s._phase_idx == 1
    s.handle_event(_right())
    assert s._phase_idx == 2
    s.handle_event(_right())
    assert s._phase_idx == 0


def test_left_key_wraps():
    from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene
    s = PredictionSliderScene()
    s.handle_event(_left())
    assert s._phase_idx == 2


def test_is_done_false():
    from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene
    s = PredictionSliderScene()
    assert s.is_done() is False


def test_next_scene_none():
    from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene
    s = PredictionSliderScene()
    assert s.next_scene() is None


def test_mouse_event_offset():
    from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene
    s = PredictionSliderScene()
    ev = pygame.event.Event(pygame.MOUSEBUTTONDOWN,
        {"button": 1, "pos": (200, 300), "touch": False})
    offset = s._offset_mouse_event(ev, dy=-48)
    assert offset.pos == (200, 252)

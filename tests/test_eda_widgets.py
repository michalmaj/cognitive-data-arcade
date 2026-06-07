# tests/test_eda_widgets.py
from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.games.eda.ui_controls import (
    ControlPanel, Slider, SliderGroup, SliderSpec,
)


@pytest.fixture(scope="session", autouse=True)
def pg():
    pygame.init()
    yield
    pygame.quit()


def _spec(default=50, step=10, min_val=0, max_val=100):
    return SliderSpec("TEST", min_val=min_val, max_val=max_val, default=default, step=step)


# -- Slider ------------------------------------------------------------------

def test_slider_starts_at_default():
    s = Slider(_spec(default=42), x=0, y=0)
    assert s.value == 42


def test_slider_key_left_decrements_by_step():
    s = Slider(_spec(default=50, step=10), x=0, y=0)
    s.handle_keydown(pygame.K_LEFT)
    assert s.value == 40


def test_slider_key_right_increments_by_step():
    s = Slider(_spec(default=50, step=10), x=0, y=0)
    s.handle_keydown(pygame.K_RIGHT)
    assert s.value == 60


def test_slider_clamps_at_min():
    s = Slider(_spec(default=0, step=10, min_val=0), x=0, y=0)
    s.handle_keydown(pygame.K_LEFT)
    assert s.value == 0


def test_slider_clamps_at_max():
    s = Slider(_spec(default=100, step=10, max_val=100), x=0, y=0)
    s.handle_keydown(pygame.K_RIGHT)
    assert s.value == 100


def test_slider_nav_keys_return_true():
    s = Slider(_spec(default=50), x=0, y=0)
    assert s.handle_keydown(pygame.K_LEFT) is True
    assert s.handle_keydown(pygame.K_RIGHT) is True


def test_slider_other_key_returns_false():
    s = Slider(_spec(), x=0, y=0)
    assert s.handle_keydown(pygame.K_SPACE) is False


def test_slider_draw_does_not_raise():
    surface = pygame.Surface((800, 600))
    s = Slider(_spec(default=50), x=30, y=80, w=280)
    s.draw(surface)


# -- SliderGroup -------------------------------------------------------------

def test_slider_group_params_has_all_keys():
    sg = SliderGroup()
    assert set(sg.params.keys()) == {"n", "baseline_ms", "effect_ms", "noise_sd", "outlier_pct"}


def test_slider_group_outlier_pct_is_float_fraction():
    sg = SliderGroup()
    p = sg.params["outlier_pct"]
    assert isinstance(p, float)
    assert 0.0 <= p <= 1.0


def test_slider_group_n_within_range():
    sg = SliderGroup()
    assert 5 <= sg.params["n"] <= 100


# -- ControlPanel ------------------------------------------------------------

def test_control_panel_empty_hypothesis_returns_none():
    cp = ControlPanel()
    assert cp.get_hypothesis_threshold() is None


def test_control_panel_hypothesis_text_parsed():
    cp = ControlPanel()
    cp._hyp_text = "50"
    assert cp.get_hypothesis_threshold() == 50


def test_control_panel_enter_returns_generate():
    cp = ControlPanel()
    ev = pygame.event.Event(
        pygame.KEYDOWN,
        key=pygame.K_RETURN, unicode="\r", mod=0, scancode=0,
    )
    assert cp.handle_event(ev) == "generate"


def test_control_panel_button_click_returns_generate():
    cp = ControlPanel()
    pos = cp._btn_rect.center
    ev = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos)
    assert cp.handle_event(ev) == "generate"


def test_control_panel_get_params_keys():
    cp = ControlPanel()
    assert set(cp.get_params().keys()) == {"n", "baseline_ms", "effect_ms", "noise_sd", "outlier_pct"}


def test_control_panel_draw_does_not_raise():
    surface = pygame.Surface((800, 600))
    ControlPanel().draw(surface)

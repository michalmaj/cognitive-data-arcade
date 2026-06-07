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


# -- ChartPanel + ResultsPanel ────────────────────────────────────────────────────

from cognitive_data_arcade.games.eda.simulator import simulate
from cognitive_data_arcade.games.eda.ui_results import ChartPanel, ResultsPanel


def _sim():
    return simulate(n=20, baseline_ms=400, effect_ms=50, noise_sd=80,
                    outlier_pct=0.05, rng_seed=42)


def test_chart_panel_draw_empty_does_not_raise():
    surface = pygame.Surface((800, 600))
    ChartPanel().draw(surface, x=360, y=30)


def test_chart_panel_update_and_draw_does_not_raise():
    surface = pygame.Surface((800, 600))
    cp = ChartPanel()
    cp.update(_sim())
    cp.draw(surface, x=360, y=30)


def test_results_panel_draw_empty_does_not_raise():
    surface = pygame.Surface((800, 600))
    ResultsPanel().draw(surface, x=360, y=270)


def test_results_panel_verdict_confirmed():
    rp = ResultsPanel()
    r = _sim()
    threshold = int(r.observed_diff) - 10
    rp.update(r, threshold)
    surface = pygame.Surface((800, 600))
    rp.draw(surface, x=360, y=270)


def test_results_panel_verdict_rejected():
    rp = ResultsPanel()
    r = _sim()
    threshold = int(r.observed_diff) + 100
    rp.update(r, threshold)
    surface = pygame.Surface((800, 600))
    rp.draw(surface, x=360, y=270)


def test_results_panel_no_threshold_no_raise():
    rp = ResultsPanel()
    rp.update(_sim(), threshold=None)
    surface = pygame.Surface((800, 600))
    rp.draw(surface, x=360, y=270)


# ── EDAScene ─────────────────────────────────────────────────────────────────────

from cognitive_data_arcade.games.eda.scene import EDAScene


def test_eda_scene_is_done_always_false():
    scene = EDAScene()
    assert scene.is_done() is False


def test_eda_scene_next_scene_is_none():
    scene = EDAScene()
    assert scene.next_scene() is None


def test_eda_scene_generate_via_enter_does_not_raise():
    scene = EDAScene()
    ev = pygame.event.Event(
        pygame.KEYDOWN, key=pygame.K_RETURN, unicode="\r", mod=0, scancode=0,
    )
    scene.handle_event(ev)   # triggers simulate() + updates panels


def test_eda_scene_draw_after_generate_does_not_raise():
    scene = EDAScene()
    ev = pygame.event.Event(
        pygame.KEYDOWN, key=pygame.K_RETURN, unicode="\r", mod=0, scancode=0,
    )
    scene.handle_event(ev)
    surface = pygame.Surface((800, 600))
    scene.draw(surface)


def test_eda_scene_draw_before_generate_does_not_raise():
    scene = EDAScene()
    surface = pygame.Surface((800, 600))
    scene.draw(surface)

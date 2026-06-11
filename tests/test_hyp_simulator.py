# tests/test_hyp_simulator.py
from __future__ import annotations
import pytest
import numpy as np


def test_generate_two_groups_shape():
    from cognitive_data_arcade.games.hypothesis_arena.simulator import generate_two_groups
    res = generate_two_groups(n=30, true_d=0.5, seed=42)
    assert len(res.x_ctrl) == 30
    assert len(res.x_treat) == 30


def test_cohens_d_zero_when_equal_means():
    from cognitive_data_arcade.games.hypothesis_arena.simulator import cohens_d
    rng = np.random.default_rng(0)
    x = rng.standard_normal(100)
    d = cohens_d(x, x)
    assert abs(d) < 1e-9


def test_cohens_d_positive():
    from cognitive_data_arcade.games.hypothesis_arena.simulator import cohens_d
    x1 = np.zeros(50)
    x2 = np.ones(50)
    assert cohens_d(x1, x2) > 0.5


def test_compute_power_increases_with_n():
    from cognitive_data_arcade.games.hypothesis_arena.simulator import compute_power
    p50  = compute_power(n=50,  d=0.5, alpha=0.05)
    p200 = compute_power(n=200, d=0.5, alpha=0.05)
    assert p200 > p50


def test_compute_power_zero_effect():
    from cognitive_data_arcade.games.hypothesis_arena.simulator import compute_power
    power = compute_power(n=100, d=0.0, alpha=0.05)
    assert abs(power - 0.05) < 0.02


def test_min_n_for_power_achieves_target():
    from cognitive_data_arcade.games.hypothesis_arena.simulator import min_n_for_power, compute_power
    n = min_n_for_power(target_power=0.80, d=0.5, alpha=0.05)
    assert compute_power(n=n, d=0.5, alpha=0.05) >= 0.80


def test_strength_label_small():
    from cognitive_data_arcade.games.hypothesis_arena.simulator import strength_label
    lbl = strength_label(0.20)
    assert "mały" in lbl


def test_strength_label_medium():
    from cognitive_data_arcade.games.hypothesis_arena.simulator import strength_label
    lbl = strength_label(0.40)
    assert "średni" in lbl


def test_scenarios_count():
    from cognitive_data_arcade.games.hypothesis_arena.simulator import _SCENARIOS
    assert len(_SCENARIOS) == 6


def test_scenarios_have_required_keys():
    from cognitive_data_arcade.games.hypothesis_arena.simulator import _SCENARIOS
    for s in _SCENARIOS:
        assert s.key
        assert s.title_pl
        assert s.context_pl
        assert isinstance(s.true_d, float)
        assert isinstance(s.max_n, int)
        assert isinstance(s.seed, int)


def test_scenario_placebo_zero_d():
    from cognitive_data_arcade.games.hypothesis_arena.simulator import _SCENARIOS
    placebo = next(s for s in _SCENARIOS if s.key == "placebo_pain")
    assert placebo.true_d == 0.0

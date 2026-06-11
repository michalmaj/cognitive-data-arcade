from __future__ import annotations
import numpy as np
import pytest
from cognitive_data_arcade.games.correlation_trap.simulator import (
    generate_correlated, pearson_r, strength_label,
    _SCENARIOS, _SANDBOX_VARS, _VAR_CORRELATIONS,
    _sandbox_corr, _sandbox_seed,
)


# ── generate_correlated ──────────────────────────────────────────────────────

def test_generate_correlated_r_close_positive():
    result = generate_correlated(0.9, noise=0.0, n=500, seed=42)
    assert abs(result.r - 0.9) < 0.10

def test_generate_correlated_r_close_negative():
    result = generate_correlated(-0.7, noise=0.0, n=500, seed=42)
    assert abs(result.r - (-0.7)) < 0.10

def test_generate_correlated_r_near_zero():
    result = generate_correlated(0.0, noise=0.0, n=500, seed=42)
    assert abs(result.r) < 0.15

def test_noise_reduces_apparent_r():
    r_clean = generate_correlated(0.8, noise=0.0, n=300, seed=1).r
    r_noisy = generate_correlated(0.8, noise=1.0, n=300, seed=1).r
    assert abs(r_noisy) < abs(r_clean)

def test_generate_correlated_deterministic():
    a = generate_correlated(0.7, 0.0, 100, seed=99)
    b = generate_correlated(0.7, 0.0, 100, seed=99)
    np.testing.assert_array_equal(a.x, b.x)
    np.testing.assert_array_equal(a.y, b.y)

def test_generate_correlated_returns_n_points():
    result = generate_correlated(0.5, 0.0, 80, seed=7)
    assert len(result.x) == 80
    assert len(result.y) == 80

def test_corrresult_r2_is_r_squared():
    result = generate_correlated(0.6, 0.0, 300, seed=3)
    assert abs(result.r2 - result.r ** 2) < 1e-9

def test_corrresult_strength_field_set():
    result = generate_correlated(0.6, 0.0, 100, seed=4)
    assert isinstance(result.strength, str)
    assert len(result.strength) > 0


# ── pearson_r ────────────────────────────────────────────────────────────────

def test_pearson_r_zero_std_x():
    x = np.ones(20)
    y = np.arange(20, dtype=float)
    assert pearson_r(x, y) == 0.0

def test_pearson_r_zero_std_y():
    x = np.arange(20, dtype=float)
    y = np.ones(20)
    assert pearson_r(x, y) == 0.0

def test_pearson_r_perfect_positive():
    x = np.arange(10, dtype=float)
    assert abs(pearson_r(x, x) - 1.0) < 1e-9

def test_pearson_r_perfect_negative():
    x = np.arange(10, dtype=float)
    assert abs(pearson_r(x, -x) - (-1.0)) < 1e-9


# ── strength_label ───────────────────────────────────────────────────────────

def test_strength_label_brak():
    assert "brak" in strength_label(0.05)

def test_strength_label_slaba():
    lbl = strength_label(0.25)
    assert "słaba" in lbl
    assert "+" in lbl

def test_strength_label_slaba_negative():
    lbl = strength_label(-0.25)
    assert "słaba" in lbl
    assert "-" in lbl

def test_strength_label_umiarkowana():
    lbl = strength_label(0.40)
    assert "umiarkowana" in lbl

def test_strength_label_silna():
    lbl = strength_label(0.60)
    assert "silna" in lbl
    assert "bardzo" not in lbl

def test_strength_label_bardzo_silna():
    lbl = strength_label(0.80)
    assert "bardzo silna" in lbl


# ── _SCENARIOS ───────────────────────────────────────────────────────────────

def test_scenarios_count():
    assert len(_SCENARIOS) == 8

def test_scenarios_causal_count():
    assert len([s for s in _SCENARIOS if s.is_causal]) == 3

def test_scenarios_spurious_count():
    assert len([s for s in _SCENARIOS if not s.is_causal]) == 5

def test_scenario_keys_unique():
    keys = [s.key for s in _SCENARIOS]
    assert len(keys) == len(set(keys))

def test_scenario_r_display_in_range():
    for s in _SCENARIOS:
        assert -1.0 <= s.r_display <= 1.0

def test_scenario_n_positive():
    for s in _SCENARIOS:
        assert s.n > 0


# ── _SANDBOX_VARS ────────────────────────────────────────────────────────────

def test_sandbox_vars_count():
    assert len(_SANDBOX_VARS) == 12

def test_sandbox_vars_have_key_and_label():
    for v in _SANDBOX_VARS:
        assert "key" in v
        assert "label" in v


# ── _sandbox_corr / _sandbox_seed ───────────────────────────────────────────

def test_sandbox_corr_symmetric():
    assert _sandbox_corr("lody", "utonecia") == _sandbox_corr("utonecia", "lody")

def test_sandbox_corr_known_value():
    assert abs(_sandbox_corr("lody", "utonecia") - 0.88) < 1e-9

def test_sandbox_corr_missing_returns_zero():
    assert _sandbox_corr("wzrost", "cage") == 0.0

def test_sandbox_seed_symmetric():
    assert _sandbox_seed("lody", "utonecia") == _sandbox_seed("utonecia", "lody")

def test_sandbox_seed_returns_int():
    assert isinstance(_sandbox_seed("lody", "utonecia"), int)

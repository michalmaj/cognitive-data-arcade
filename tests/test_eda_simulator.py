# tests/test_eda_simulator.py
from __future__ import annotations

import numpy as np
import pytest

from cognitive_data_arcade.games.eda.simulator import SimResult, simulate


def _run(**kw):
    defaults = dict(n=20, baseline_ms=400, effect_ms=50, noise_sd=80, outlier_pct=0.05, rng_seed=42)
    return simulate(**{**defaults, **kw})


def test_result_arrays_have_correct_length():
    r = _run()
    assert len(r.cond1) == 20
    assert len(r.cond2) == 20
    assert len(r.outlier_mask1) == 20
    assert len(r.outlier_mask2) == 20


def test_outlier_count_matches_pct():
    # round(20 * 0.05) = 1
    r = _run()
    assert r.outlier_mask1.sum() == 1
    assert r.outlier_mask2.sum() == 1


def test_zero_outlier_pct_produces_no_outliers():
    r = _run(outlier_pct=0.0)
    assert r.outlier_mask1.sum() == 0
    assert r.outlier_mask2.sum() == 0


def test_outlier_values_are_large():
    r = _run(n=40, outlier_pct=0.10, noise_sd=10)
    assert all(v >= 800 for v in r.cond1[r.outlier_mask1])
    assert all(v >= 800 for v in r.cond2[r.outlier_mask2])


def test_effect_shifts_cond2_higher():
    r = _run(n=100, effect_ms=100, noise_sd=20, outlier_pct=0.0)
    assert r.observed_diff > 0  # mean2 - mean1 > 0
    assert abs(r.observed_diff - 100) < 35


def test_zero_effect_diff_near_zero():
    r = _run(n=200, effect_ms=0, noise_sd=30, outlier_pct=0.0)
    assert abs(r.observed_diff) < 20


def test_p_value_in_range():
    r = _run()
    assert 0.0 <= r.p_value <= 1.0


def test_large_effect_has_low_p_value():
    r = _run(n=100, effect_ms=150, noise_sd=20, outlier_pct=0.0)
    assert r.p_value < 0.01


def test_small_n_high_noise_has_high_p_value():
    r = _run(n=5, effect_ms=10, noise_sd=150, outlier_pct=0.0, rng_seed=7)
    assert r.p_value > 0.05


def test_mean_no_outlier_differs_when_outliers_present():
    r = _run(n=30, outlier_pct=0.10, noise_sd=10)
    # With 3 outliers (800-1500ms) in a 400ms distribution, means must differ
    assert abs(r.mean1 - r.mean1_no_out) > 10


def test_rng_seed_gives_deterministic_results():
    r1 = _run(rng_seed=99)
    r2 = _run(rng_seed=99)
    np.testing.assert_array_equal(r1.cond1, r2.cond1)

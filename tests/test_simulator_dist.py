# tests/test_simulator_dist.py
from __future__ import annotations
import numpy as np
from cognitive_data_arcade.games.distribution_playground.simulator import (
    SimResult, CompareResult, simulate, compare, random_target, match_score,
)

def test_simresult_has_expected_fields():
    r = SimResult(
        samples=np.array([400.0, 420.0]),
        mean=410.0, median=410.0, sd=10.0, iqr=20.0, skewness=0.0,
        dist_type="normal", params={"mu": 400, "sigma": 80, "N": 50},
    )
    assert r.dist_type == "normal"
    assert len(r.samples) == 2

def test_compareresult_has_expected_fields():
    c = CompareResult(delta_mean=50.0, cohens_d=0.8, p_value=0.03, sd_ratio=1.0)
    assert c.p_value == 0.03


# ── Normal ──────────────────────────────────────────────────────────────────
def test_normal_sample_length():
    r = simulate("normal", {"mu": 400, "sigma": 80, "N": 50}, rng_seed=1)
    assert len(r.samples) == 50

def test_normal_mean_close_to_mu():
    r = simulate("normal", {"mu": 400, "sigma": 80, "N": 500}, rng_seed=2)
    assert abs(r.mean - 400) < 20

def test_normal_sd_close_to_sigma():
    r = simulate("normal", {"mu": 400, "sigma": 80, "N": 500}, rng_seed=3)
    assert abs(r.sd - 80) < 15

def test_normal_skewness_near_zero():
    r = simulate("normal", {"mu": 400, "sigma": 80, "N": 500}, rng_seed=4)
    assert abs(r.skewness) < 0.4

def test_normal_dist_type():
    r = simulate("normal", {"mu": 400, "sigma": 80, "N": 50}, rng_seed=1)
    assert r.dist_type == "normal"

# ── Uniform ─────────────────────────────────────────────────────────────────
def test_uniform_sample_length():
    r = simulate("uniform", {"min": 300, "max": 600, "N": 40}, rng_seed=5)
    assert len(r.samples) == 40

def test_uniform_samples_in_range():
    r = simulate("uniform", {"min": 300, "max": 600, "N": 200}, rng_seed=6)
    assert r.samples.min() >= 300
    assert r.samples.max() <= 600

def test_uniform_skewness_near_zero():
    r = simulate("uniform", {"min": 300, "max": 600, "N": 500}, rng_seed=7)
    assert abs(r.skewness) < 0.4

# ── Ex-Gaussian ──────────────────────────────────────────────────────────────
def test_exgaussian_sample_length():
    r = simulate("exgaussian", {"mu": 350, "sigma": 60, "tau": 100, "N": 50}, rng_seed=8)
    assert len(r.samples) == 50

def test_exgaussian_positive_skewness():
    r = simulate("exgaussian", {"mu": 350, "sigma": 60, "tau": 100, "N": 500}, rng_seed=9)
    assert r.skewness > 0.3

def test_exgaussian_mean_close_to_mu_plus_tau():
    r = simulate("exgaussian", {"mu": 350, "sigma": 40, "tau": 100, "N": 1000}, rng_seed=10)
    expected_mean = 350 + 100
    assert abs(r.mean - expected_mean) < 25

def test_simulate_stores_params():
    params = {"mu": 400, "sigma": 80, "N": 50}
    r = simulate("normal", params, rng_seed=1)
    assert r.params == params

def test_iqr_positive():
    r = simulate("normal", {"mu": 400, "sigma": 80, "N": 100}, rng_seed=11)
    assert r.iqr > 0

def test_median_stored():
    r = simulate("normal", {"mu": 400, "sigma": 80, "N": 50}, rng_seed=12)
    assert isinstance(r.median, float)

# ── compare() ───────────────────────────────────────────────────────────────

def test_compare_delta_mean_sign():
    a = simulate("normal", {"mu": 400, "sigma": 80, "N": 100}, rng_seed=1)
    b = simulate("normal", {"mu": 500, "sigma": 80, "N": 100}, rng_seed=2)
    c = compare(a, b)
    assert c.delta_mean > 0   # mean_b - mean_a > 0

def test_compare_p_value_range():
    a = simulate("normal", {"mu": 400, "sigma": 80, "N": 100}, rng_seed=1)
    b = simulate("normal", {"mu": 500, "sigma": 80, "N": 100}, rng_seed=2)
    c = compare(a, b)
    assert 0.0 <= c.p_value <= 1.0

def test_compare_cohens_d_large_effect():
    a = simulate("normal", {"mu": 400, "sigma": 50, "N": 100}, rng_seed=1)
    b = simulate("normal", {"mu": 600, "sigma": 50, "N": 100}, rng_seed=2)
    c = compare(a, b)
    assert abs(c.cohens_d) > 1.0

def test_compare_sd_ratio():
    a = simulate("normal", {"mu": 400, "sigma": 80, "N": 100}, rng_seed=1)
    b = simulate("normal", {"mu": 400, "sigma": 160, "N": 100}, rng_seed=2)
    c = compare(a, b)
    assert abs(c.sd_ratio - 0.5) < 0.2

# ── random_target() ────────────────────────────────────────────────────────

def test_random_target_returns_simresult():
    rng = np.random.default_rng(42)
    r = random_target(rng)
    assert isinstance(r, SimResult)
    assert r.dist_type in ("normal", "uniform", "exgaussian")

def test_random_target_params_within_range():
    from cognitive_data_arcade.games.distribution_playground.simulator import _PARAM_RANGES
    for seed in range(20):
        rng = np.random.default_rng(seed)
        r = random_target(rng)
        ranges = _PARAM_RANGES[r.dist_type]
        for k, (lo, hi) in ranges.items():
            assert lo <= r.params[k] <= hi, f"{k}={r.params[k]} out of [{lo},{hi}]"

# ── match_score() ──────────────────────────────────────────────────────────

def test_match_score_perfect():
    rng = np.random.default_rng(7)
    target = random_target(rng)
    score = match_score(target.dist_type, target.params, target.dist_type, target.params)
    assert score == 100.0

def test_match_score_wrong_type_is_zero():
    rng = np.random.default_rng(7)
    target = random_target(rng)
    if target.dist_type == "normal":
        student_type = "uniform"
        student_params = {"min": 300, "max": 600, "N": 50}
    else:
        student_type = "normal"
        student_params = {"mu": 400, "sigma": 80, "N": 50}
    score = match_score(student_type, student_params, target.dist_type, target.params)
    assert score == 0.0

def test_match_score_partial():
    target_params = {"mu": 400, "sigma": 80, "N": 50}
    student_params = {"mu": 600, "sigma": 80, "N": 50}
    score = match_score("normal", student_params, "normal", target_params)
    assert 0.0 < score < 100.0

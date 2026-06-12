from __future__ import annotations
import pytest
import numpy as np


def test_simulate_data_length():
    from cognitive_data_arcade.games.prediction_slider.simulator import simulate_data
    x, y = simulate_data(n=30, slope=1.0, intercept=0.0, noise=0.5, seed=1)
    assert len(x) == 30
    assert len(y) == 30


def test_simulate_data_seed_deterministic():
    from cognitive_data_arcade.games.prediction_slider.simulator import simulate_data
    x1, y1 = simulate_data(n=20, slope=2.0, intercept=1.0, noise=0.3, seed=42)
    x2, y2 = simulate_data(n=20, slope=2.0, intercept=1.0, noise=0.3, seed=42)
    np.testing.assert_array_equal(x1, x2)
    np.testing.assert_array_equal(y1, y2)


def test_fit_line_perfect():
    from cognitive_data_arcade.games.prediction_slider.simulator import simulate_data, fit_line
    x, y = simulate_data(n=50, slope=2.5, intercept=1.0, noise=0.0, seed=7)
    slope, intercept, r2, residuals = fit_line(x, y)
    assert abs(slope - 2.5) < 0.01
    assert abs(intercept - 1.0) < 0.01
    assert abs(r2 - 1.0) < 0.001


def test_fit_line_r_squared_range():
    from cognitive_data_arcade.games.prediction_slider.simulator import simulate_data, fit_line
    x, y = simulate_data(n=50, slope=1.0, intercept=0.0, noise=1.0, seed=9)
    _, _, r2, residuals = fit_line(x, y)
    assert 0.0 <= r2 <= 1.0


def test_predict_value():
    from cognitive_data_arcade.games.prediction_slider.simulator import predict
    result = predict(x_val=5.0, slope=2.0, intercept=1.0)
    assert abs(result - 11.0) < 1e-9

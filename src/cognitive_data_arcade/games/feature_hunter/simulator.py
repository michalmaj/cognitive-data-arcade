from __future__ import annotations

import numpy as np

from cognitive_data_arcade.games.feature_hunter.features import Feature


def simulate_scatter(
    feature: Feature,
    n_points: int = 60,
    seed: int = 0,
) -> tuple[np.ndarray, np.ndarray]:
    """Return (x, y) arrays both normalised to [0, 1].

    Generates y = correlation * x + noise * N(0, 1), then maps both
    axes to [0, 1] via min-max scaling so the scatter fills the card.
    """
    rng = np.random.default_rng(seed)
    x_raw = rng.standard_normal(n_points)
    y_raw = feature.correlation * x_raw + feature.noise * rng.standard_normal(n_points)

    def _norm(arr: np.ndarray) -> np.ndarray:
        lo, hi = arr.min(), arr.max()
        if hi - lo < 1e-9:
            return np.full_like(arr, 0.5)
        return (arr - lo) / (hi - lo)

    return _norm(x_raw), _norm(y_raw)


def compute_accuracy_delta(feature: Feature, seed: int = 0) -> tuple[float, float]:
    """Return (acc_with_feature, acc_without_feature) as floats in [0, 1].

    Simulated logistic model:
      acc_with    = sigmoid(3 * abs(correlation))
      acc_without = 0.52 + small_random_offset
    """
    rng = np.random.default_rng(seed)

    def _sigmoid(z: float) -> float:
        return 1.0 / (1.0 + float(np.exp(-z)))

    acc_with = _sigmoid(3.0 * abs(feature.correlation))
    acc_without = 0.52 + float(rng.uniform(-0.04, 0.04))
    return acc_with, acc_without

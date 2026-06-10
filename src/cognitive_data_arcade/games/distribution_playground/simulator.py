# src/cognitive_data_arcade/games/distribution_playground/simulator.py
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np


@dataclass
class SimResult:
    samples:   np.ndarray
    mean:      float
    median:    float
    sd:        float
    iqr:       float
    skewness:  float
    dist_type: str        # "normal" | "uniform" | "exgaussian"
    params:    dict[str, float]


@dataclass
class CompareResult:
    delta_mean: float    # mean_b - mean_a
    cohens_d:   float    # (mean_a - mean_b) / pooled_sd
    p_value:    float    # Welch t-test
    sd_ratio:   float    # sd_a / sd_b


_PARAM_RANGES: dict[str, dict[str, tuple[float, float]]] = {
    "normal":     {"mu": (200, 800), "sigma": (20, 200), "N": (20, 200)},
    "uniform":    {"min": (100, 600), "max": (300, 1000), "N": (20, 200)},
    "exgaussian": {"mu": (200, 600), "sigma": (20, 150), "tau": (20, 300), "N": (20, 200)},
}


def _fisher_skewness(x: np.ndarray) -> float:
    n = len(x)
    if n < 3:
        return 0.0
    m = x.mean()
    s = x.std(ddof=1)
    if s == 0:
        return 0.0
    return float(((x - m) ** 3).mean() / s ** 3)


def simulate(
    dist_type: str,
    params: dict[str, float],
    rng_seed: int | None = None,
) -> SimResult:
    rng = np.random.default_rng(rng_seed)
    n = int(params["N"])

    if dist_type == "normal":
        samples = rng.normal(params["mu"], params["sigma"], n)
    elif dist_type == "uniform":
        samples = rng.uniform(params["min"], params["max"], n)
    elif dist_type == "exgaussian":
        norm_part = rng.normal(params["mu"], params["sigma"], n)
        exp_part = rng.exponential(params["tau"], n)
        samples = norm_part + exp_part
    else:
        raise ValueError(f"Unknown dist_type: {dist_type!r}")

    q1, q3 = float(np.percentile(samples, 25)), float(np.percentile(samples, 75))
    return SimResult(
        samples=samples,
        mean=float(samples.mean()),
        median=float(np.median(samples)),
        sd=float(samples.std(ddof=1)) if n > 1 else 0.0,
        iqr=q3 - q1,
        skewness=_fisher_skewness(samples),
        dist_type=dist_type,
        params=dict(params),
    )

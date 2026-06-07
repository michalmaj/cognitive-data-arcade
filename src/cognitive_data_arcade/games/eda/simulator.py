# src/cognitive_data_arcade/games/eda/simulator.py
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass
class SimResult:
    cond1: np.ndarray
    cond2: np.ndarray
    outlier_mask1: np.ndarray
    outlier_mask2: np.ndarray
    mean1: float
    mean2: float
    sd1: float
    sd2: float
    observed_diff: float       # mean2 - mean1
    mean1_no_out: float
    mean2_no_out: float
    t_stat: float              # positive when cond2 > cond1; computed on raw data (outliers included)
    p_value: float             # two-tailed Welch t-test


def _betacf(a: float, b: float, x: float) -> float:
    """Lentz continued-fraction expansion for regularised incomplete beta."""
    qab, qap = a + b, a + 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < 1e-30:
        d = 1e-30
    d = 1.0 / d
    h = d
    for m in range(1, 201):
        m2 = 2 * m
        aa = m * (b - m) * x / ((a - 1.0 + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 3e-7:
            break
    return h


def _betainc(x: float, a: float, b: float) -> float:
    """Regularised incomplete beta I(x, a, b). Accuracy ~1e-6."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(a * math.log(x) + b * math.log(1.0 - x) - lbeta)
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def _welch_t(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    """Two-sample Welch t-test, signed (b - a). Returns (t, p)."""
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return 0.0, 1.0
    ma, mb = float(a.mean()), float(b.mean())
    va = float(a.var(ddof=1))
    vb = float(b.var(ddof=1))
    se2 = va / na + vb / nb
    if se2 <= 0.0:
        return 0.0, 1.0
    t = (mb - ma) / math.sqrt(se2)
    df = se2 ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
    x = df / (df + t ** 2)
    p = float(np.clip(_betainc(x, df / 2.0, 0.5), 0.0, 1.0))
    return t, p


def simulate(
    n: int,
    baseline_ms: int,
    effect_ms: int,
    noise_sd: int,
    outlier_pct: float,
    rng_seed: int | None = None,
) -> SimResult:
    rng = np.random.default_rng(rng_seed)

    c1 = rng.normal(baseline_ms, noise_sd, n)
    c2 = rng.normal(baseline_ms + effect_ms, noise_sd, n)

    k = round(n * outlier_pct)
    mask1 = np.zeros(n, dtype=bool)
    mask2 = np.zeros(n, dtype=bool)

    if k > 0:
        idx1 = rng.choice(n, size=k, replace=False)
        idx2 = rng.choice(n, size=k, replace=False)
        c1[idx1] = rng.uniform(800, 1500, k)
        c2[idx2] = rng.uniform(800, 1500, k)
        mask1[idx1] = True
        mask2[idx2] = True

    mean1, mean2 = float(c1.mean()), float(c2.mean())
    sd1 = float(c1.std(ddof=1)) if n > 1 else 0.0
    sd2 = float(c2.std(ddof=1)) if n > 1 else 0.0

    c1_clean, c2_clean = c1[~mask1], c2[~mask2]
    mean1_no = float(c1_clean.mean()) if len(c1_clean) > 0 else mean1
    mean2_no = float(c2_clean.mean()) if len(c2_clean) > 0 else mean2

    t_stat, p_value = _welch_t(c1, c2)

    return SimResult(
        cond1=c1, cond2=c2,
        outlier_mask1=mask1, outlier_mask2=mask2,
        mean1=mean1, mean2=mean2, sd1=sd1, sd2=sd2,
        observed_diff=mean2 - mean1,
        mean1_no_out=mean1_no, mean2_no_out=mean2_no,
        t_stat=t_stat, p_value=p_value,
    )

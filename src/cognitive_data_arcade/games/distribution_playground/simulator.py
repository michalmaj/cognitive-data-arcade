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


# ── Welch t-test (pure numpy, no scipy) ─────────────────────────────────────

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


# ── Public functions ─────────────────────────────────────────────────────────

def compare(a: SimResult, b: SimResult) -> CompareResult:
    pooled_sd = (a.sd + b.sd) / 2.0
    cohens_d = (a.mean - b.mean) / pooled_sd if pooled_sd > 0 else 0.0
    _, p = _welch_t(a.samples, b.samples)
    sd_ratio = a.sd / b.sd if b.sd > 0 else 1.0
    return CompareResult(
        delta_mean=b.mean - a.mean,
        cohens_d=cohens_d,
        p_value=p,
        sd_ratio=sd_ratio,
    )


def random_target(rng: np.random.Generator) -> SimResult:
    dist_type = rng.choice(["normal", "uniform", "exgaussian"])
    ranges = _PARAM_RANGES[dist_type]
    params: dict[str, float] = {}
    for k, (lo, hi) in ranges.items():
        if k == "N":
            params[k] = float(int(rng.integers(int(lo), int(hi) + 1, endpoint=True)))
        else:
            step = 10.0
            steps = int((hi - lo) / step)
            params[k] = min(hi, lo + float(rng.integers(0, steps + 1, endpoint=True)) * step)
    # For uniform distribution ensure min < max (independent sampling can violate this)
    if dist_type == "uniform" and params.get("min", 0) >= params.get("max", 1):
        params["min"] = params["max"] - 10.0
    return simulate(dist_type, params, rng_seed=int(rng.integers(0, 2**31)))


def match_score(
    student_type: str,
    student_params: dict[str, float],
    target_type: str,
    target_params: dict[str, float],
) -> float:
    """0-100 match score. Type mismatch returns 0."""
    if student_type != target_type:
        return 0.0
    ranges = _PARAM_RANGES[target_type]
    proximities = []
    for k, (lo, hi) in ranges.items():
        span = hi - lo
        if span <= 0:
            continue
        student_val = student_params.get(k, lo)
        target_val = target_params.get(k, lo)
        prox = max(0.0, 1.0 - abs(student_val - target_val) / span)
        proximities.append(prox)
    if not proximities:
        return 100.0
    return round(sum(proximities) / len(proximities) * 100.0, 1)

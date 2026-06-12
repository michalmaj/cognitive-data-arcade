from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Scenario:
    key: str
    title_pl: str
    x_label_pl: str
    y_label_pl: str
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    true_slope: float
    true_intercept: float
    noise: float
    n: int
    seed: int


def _seed(key: str) -> int:
    return int(hashlib.md5(key.encode()).hexdigest(), 16) & 0xFFFF


_SCENARIOS: list[Scenario] = [
    Scenario(
        key="sleep_test",
        title_pl="Godziny snu → wynik testu",
        x_label_pl="Godziny snu (h)",
        y_label_pl="Wynik testu (pkt)",
        x_min=4.0, x_max=10.0, y_min=40.0, y_max=100.0,
        true_slope=8.0, true_intercept=10.0, noise=7.0, n=25,
        seed=_seed("sleep_test"),
    ),
    Scenario(
        key="temp_icecream",
        title_pl="Temperatura → sprzedaż lodów",
        x_label_pl="Temperatura (°C)",
        y_label_pl="Sprzedaż lodów (szt.)",
        x_min=10.0, x_max=35.0, y_min=0.0, y_max=200.0,
        true_slope=7.0, true_intercept=-40.0, noise=18.0, n=28,
        seed=_seed("temp_icecream"),
    ),
    Scenario(
        key="age_rt",
        title_pl="Wiek → czas reakcji",
        x_label_pl="Wiek (lata)",
        y_label_pl="Czas reakcji (ms)",
        x_min=20.0, x_max=70.0, y_min=150.0, y_max=450.0,
        true_slope=5.0, true_intercept=50.0, noise=28.0, n=30,
        seed=_seed("age_rt"),
    ),
    Scenario(
        key="exercise_hr",
        title_pl="Ćwiczenia → tętno spoczynkowe",
        x_label_pl="Ćwiczenia (h/tydzień)",
        y_label_pl="Tętno spoczynkowe (bpm)",
        x_min=0.0, x_max=10.0, y_min=50.0, y_max=90.0,
        true_slope=-3.5, true_intercept=90.0, noise=4.0, n=25,
        seed=_seed("exercise_hr"),
    ),
    Scenario(
        key="height_weight",
        title_pl="Wzrost → waga",
        x_label_pl="Wzrost (cm)",
        y_label_pl="Waga (kg)",
        x_min=155.0, x_max=195.0, y_min=50.0, y_max=110.0,
        true_slope=1.4, true_intercept=-168.0, noise=7.0, n=30,
        seed=_seed("height_weight"),
    ),
]


def simulate_data(
    n: int,
    slope: float,
    intercept: float,
    noise: float,
    seed: int | None,
) -> tuple[np.ndarray, np.ndarray]:
    """Returns (x, y) from y = slope*x + intercept + N(0, noise)."""
    rng = np.random.default_rng(seed)
    x = rng.uniform(0, 10, n)
    y = slope * x + intercept + rng.normal(0, noise, n)
    return x, y


def simulate_scenario(sc: Scenario) -> tuple[np.ndarray, np.ndarray]:
    """Generate data for a Scenario, x sampled from [x_min, x_max]."""
    rng = np.random.default_rng(sc.seed)
    x = rng.uniform(sc.x_min, sc.x_max, sc.n)
    y = sc.true_slope * x + sc.true_intercept + rng.normal(0, sc.noise, sc.n)
    return x, y


def fit_line(
    x: np.ndarray, y: np.ndarray
) -> tuple[float, float, float, np.ndarray]:
    """Returns (slope, intercept, r_squared, residuals)."""
    coeffs = np.polyfit(x, y, 1)
    slope, intercept = float(coeffs[0]), float(coeffs[1])
    y_hat = slope * x + intercept
    residuals = y - y_hat
    ss_res = float(np.sum(residuals ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 0.0
    r2 = float(np.clip(r2, 0.0, 1.0))
    return slope, intercept, r2, residuals


def predict(x_val: float, slope: float, intercept: float) -> float:
    return slope * x_val + intercept

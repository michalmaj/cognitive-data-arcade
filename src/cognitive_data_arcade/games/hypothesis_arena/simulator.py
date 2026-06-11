# src/cognitive_data_arcade/games/hypothesis_arena/simulator.py
from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass
class TwoGroupResult:
    x_ctrl:   np.ndarray
    x_treat:  np.ndarray
    t_stat:   float
    p_value:  float
    cohens_d: float
    power:    float


@dataclass(frozen=True)
class Scenario:
    key:        str
    title_pl:   str
    context_pl: str
    true_d:     float
    max_n:      int
    seed:       int


def _scenario_seed(key: str) -> int:
    return int(hashlib.md5(key.encode()).hexdigest(), 16) & 0xFFFF


_SCENARIOS: list[Scenario] = [
    Scenario(
        key="caffeine_rt",
        title_pl="Kofeina → czas reakcji",
        context_pl="Połowa uczestników dostaje kawę (200mg kofeiny), połowa placebo. Mierzysz czas reakcji w teście komputerowym.",
        true_d=0.35,
        max_n=200,
        seed=_scenario_seed("caffeine_rt"),
    ),
    Scenario(
        key="study_technique",
        title_pl="Technika nauki → wynik testu",
        context_pl="Grupa A uczy się metodą powtórzeń rozłożonych w czasie, grupa B uczy się raz intensywnie. Sprawdzian po tygodniu.",
        true_d=0.50,
        max_n=150,
        seed=_scenario_seed("study_technique"),
    ),
    Scenario(
        key="music_focus",
        title_pl="Muzyka → koncentracja",
        context_pl="Uczestnicy rozwiązują zadania logiczne — jedni w ciszy, drudzy przy muzyce klasycznej. Mierzysz liczbę poprawnych odpowiedzi.",
        true_d=0.15,
        max_n=300,
        seed=_scenario_seed("music_focus"),
    ),
    Scenario(
        key="sleep_memory",
        title_pl="Sen → pamięć robocza",
        context_pl="Grupa śpiąca 8h vs. 5h. Następnego ranka test pamięci roboczej n-back.",
        true_d=0.60,
        max_n=100,
        seed=_scenario_seed("sleep_memory"),
    ),
    Scenario(
        key="mindfulness_stress",
        title_pl="Mindfulness → poziom stresu",
        context_pl="4-tygodniowy program mindfulness vs. lista oczekujących. Pomiar kortyzolu i samooceny stresu.",
        true_d=0.40,
        max_n=200,
        seed=_scenario_seed("mindfulness_stress"),
    ),
    Scenario(
        key="placebo_pain",
        title_pl="Placebo → odczucie bólu",
        context_pl="Podajesz cukrową tabletkę jako 'nowy lek na ból głowy'. Mierzysz odczucie bólu na skali 1-10 po 30 min.",
        true_d=0.00,
        max_n=150,
        seed=_scenario_seed("placebo_pain"),
    ),
]


def cohens_d(x1: np.ndarray, x2: np.ndarray) -> float:
    n1, n2 = len(x1), len(x2)
    if n1 < 2 or n2 < 2:
        return 0.0
    pooled_std = np.sqrt(((n1 - 1) * x1.std(ddof=1) ** 2 + (n2 - 1) * x2.std(ddof=1) ** 2) / (n1 + n2 - 2))
    if pooled_std < 1e-12:
        # Degenerate case: zero variance — return signed infinity if means differ, else 0
        diff = float(x2.mean() - x1.mean())
        return float(np.sign(diff) * np.inf) if abs(diff) > 1e-12 else 0.0
    return float((x2.mean() - x1.mean()) / pooled_std)


def compute_power(n: int, d: float, alpha: float) -> float:
    """Power of two-sample t-test via normal approximation."""
    if d == 0.0:
        return alpha
    delta = abs(d) * np.sqrt(n / 2)
    z_alpha2 = stats.norm.ppf(1 - alpha / 2)
    power = stats.norm.cdf(delta - z_alpha2) + stats.norm.cdf(-delta - z_alpha2)
    return float(np.clip(power, 0.0, 1.0))


def min_n_for_power(target_power: float, d: float, alpha: float) -> int:
    """Binary search for minimum N achieving target_power."""
    if d == 0.0:
        return 9999
    lo, hi = 2, 10_000
    while lo < hi:
        mid = (lo + hi) // 2
        if compute_power(mid, d, alpha) >= target_power:
            hi = mid
        else:
            lo = mid + 1
    return lo


def strength_label(d: float) -> str:
    a = abs(d)
    if a < 0.10:
        return "pomijalny"
    if a < 0.30:
        return "mały"
    if a < 0.50:
        return "średni"
    if a < 0.80:
        return "duży"
    return "bardzo duży"


def generate_two_groups(n: int, true_d: float, seed: int) -> TwoGroupResult:
    rng = np.random.default_rng(seed)
    x_ctrl  = rng.standard_normal(n)
    x_treat = rng.standard_normal(n) + true_d
    t_stat, p_value = stats.ttest_ind(x_ctrl, x_treat)
    d = cohens_d(x_ctrl, x_treat)
    power = compute_power(n, true_d, 0.05)
    return TwoGroupResult(
        x_ctrl=x_ctrl,
        x_treat=x_treat,
        t_stat=float(t_stat),
        p_value=float(p_value),
        cohens_d=d,
        power=power,
    )

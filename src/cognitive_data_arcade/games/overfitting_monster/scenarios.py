from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Scenario:
    name_pl: str
    kind: str   # blobs | moons | circles | noisy_blobs | moons_noisy
    n_points: int
    noise: float
    hint_pl: str
    insight_pl: str


SCENARIOS: list[Scenario] = [
    Scenario(
        name_pl="Oddzielone chmury",
        kind="blobs",
        n_points=60,
        noise=0.05,
        hint_pl=(
            "Dwie wyraźnie oddzielone grupy. Granica KNN powinna być prosta i gładka. "
            "Przy tak czystych danych małe k (np. 5-9) działa świetnie — "
            "nie ma potrzeby wygładzania. Duże k może underfittować."
        ),
        insight_pl=(
            "Przy czystych, oddzielonych grupach KNN z małym k osiąga doskonałą dokładność "
            "bez ryzyka overfittingu. Gap train-test powinien być bliski zera."
        ),
    ),
    Scenario(
        name_pl="Półksiężyce",
        kind="moons",
        n_points=60,
        noise=0.10,
        hint_pl=(
            "Dwie splecione grupy w kształcie półksiężyców. "
            "Potrzebujesz wystarczająco małego k, by KNN mógł śledzić krzywą granicę. "
            "Spróbuj k=3-7 — za duże k wygłodzi granicę i straci kształt."
        ),
        insight_pl=(
            "Nieliniowa granica wymaga mniejszego k. Zbyt duże k traci zakrzywienie "
            "i spada poniżej 80% dokładności. Sweet spot to kompromis elastyczności i szumu."
        ),
    ),
    Scenario(
        name_pl="Kółko w kółku",
        kind="circles",
        n_points=60,
        noise=0.05,
        hint_pl=(
            "Klasa czerwona w środku, niebieska dookoła. "
            "KNN z małym k (3-5) rysuje okrągłą granicę — właśnie tego potrzeba. "
            "Duże k całkowicie gubi ten wzorzec i klasyfikuje wszystko jako klasę zewnętrzną."
        ),
        insight_pl=(
            "Koncentryczne kółka to klasyczny test dla KNN. Małe k pozwala widzieć "
            "strukturę pierścienia. Duże k traci ją — underfitting strukturalny."
        ),
    ),
    Scenario(
        name_pl="Zaszumione chmury",
        kind="noisy_blobs",
        n_points=80,
        noise=0.35,
        hint_pl=(
            "Chmury z dużym szumem — klasy częściowo się mieszają. "
            "Małe k zapamiętuje każdy szumowy punkt i overfittuje. "
            "Przy zaszumionych danych potrzeba większego k (9-13), "
            "żeby wygładzić szum i dobrze generalizować."
        ),
        insight_pl=(
            "Zaszumione dane to sytuacja, gdy większe k pomaga — wygładza szum "
            "zamiast zapamiętywać go. Gap train-test przy małym k będzie duży."
        ),
    ),
    Scenario(
        name_pl="Zaszumione półksiężyce",
        kind="moons_noisy",
        n_points=80,
        noise=0.30,
        hint_pl=(
            "Najtrudniejszy scenariusz: nieliniowa granica i duży szum. "
            "Za małe k overfittuje szum, za duże k gubi kształt półksiężyców. "
            "Spróbuj k=7-11 i obserwuj, jak zmienia się gap train-test."
        ),
        insight_pl=(
            "Zaszumione półksiężyce to kompromis bias-variance w czystej postaci. "
            "Nie ma idealnego k — jest sweet spot. Split też ma znaczenie: "
            "mały zbiór testowy daje niepewną estymację dokładności."
        ),
    ),
]


def generate_data(scenario: Scenario, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Returns X (n, 2) normalised to [0,1]x[0,1], y (n,) with values 0 or 1."""
    rng = np.random.default_rng(seed)
    n = scenario.n_points
    noise = scenario.noise
    half = n // 2

    if scenario.kind in ("blobs", "noisy_blobs"):
        std = max(noise * 3, 0.05)
        X0 = rng.normal([0.25, 0.5], std, (half, 2))
        X1 = rng.normal([0.75, 0.5], std, (n - half, 2))
        X = np.clip(np.vstack([X0, X1]), 0.0, 1.0)
        y = np.array([0] * half + [1] * (n - half), dtype=np.int32)

    elif scenario.kind in ("moons", "moons_noisy"):
        t0 = np.linspace(0, np.pi, half)
        t1 = np.linspace(np.pi, 2 * np.pi, n - half)
        X0 = np.column_stack([np.cos(t0), np.sin(t0)])
        X1 = np.column_stack([1 - np.cos(t1), 1 - np.sin(t1) - 0.5])
        X = np.vstack([X0, X1])
        X += rng.normal(0, noise, X.shape)
        lo, hi = X.min(axis=0), X.max(axis=0)
        X = (X - lo) / (hi - lo + 1e-9)
        X = np.clip(X, 0.0, 1.0)
        y = np.array([0] * half + [1] * (n - half), dtype=np.int32)

    elif scenario.kind == "circles":
        t0 = rng.uniform(0, 2 * np.pi, half)
        X0 = np.column_stack([0.5 + 0.2 * np.cos(t0), 0.5 + 0.2 * np.sin(t0)])
        t1 = rng.uniform(0, 2 * np.pi, n - half)
        X1 = np.column_stack([0.5 + 0.4 * np.cos(t1), 0.5 + 0.4 * np.sin(t1)])
        X = np.vstack([X0, X1])
        X += rng.normal(0, noise, X.shape)
        X = np.clip(X, 0.0, 1.0)
        y = np.array([0] * half + [1] * (n - half), dtype=np.int32)

    else:
        raise ValueError(f"Unknown scenario kind: {scenario.kind!r}")

    return X, y

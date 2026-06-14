from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Scenario:
    name_pl: str
    kind: str        # blobs | moons | circles | noisy_blobs | moons_noisy
    n_points: int
    noise: float
    hint_pl: str     # right-click popup text
    insight_pl: str  # round-result educational blurb


SCENARIOS: list[Scenario] = [
    Scenario(
        name_pl="Oddzielone chmury",
        kind="blobs",
        n_points=40,
        noise=0.05,
        hint_pl=(
            "Dwie oddzielone grupy punktów. Klasa czerwona po lewej, niebieska po prawej. "
            "Wystarczy narysować pionową linię między nimi. "
            "To klasyczny przypadek dla klasyfikatora liniowego."
        ),
        insight_pl=(
            "Oddzielone chmury to idealne dane dla klasyfikatora liniowego — "
            "prosta pionowa linia wystarczy, by osiągnąć prawie 100% dokładności. "
            "Gdy dane są liniowo separowalne, regresja logistyczna i KNN osiągają podobne wyniki."
        ),
    ),
    Scenario(
        name_pl="Półksiężyce",
        kind="moons",
        n_points=50,
        noise=0.10,
        hint_pl=(
            "Dane w kształcie dwóch półksiężyców — klasy są splecione. "
            "Linia prosta nie oddzieli ich dobrze. "
            "Spróbuj narysować łukową granicę wzdłuż górnej grupy. "
            "KNN radzi sobie tu lepiej niż klasyfikator liniowy."
        ),
        insight_pl=(
            "Kształt półksiężyca jest nieliniowo separowalny — żadna prosta linia nie poradzi sobie dobrze. "
            "KNN zapamiętuje lokalne sąsiedztwo i rysuje giętką granicę, "
            "dlatego bije klasyfikator liniowy."
        ),
    ),
    Scenario(
        name_pl="Kółko w kółku",
        kind="circles",
        n_points=50,
        noise=0.05,
        hint_pl=(
            "Klasa czerwona jest w środku, niebieska otacza ją z zewnątrz. "
            "Żadna prosta linia nie oddzieli ich — potrzebujesz granicy w kształcie koła. "
            "To klasyczny przykład ograniczeń klasyfikatorów liniowych."
        ),
        insight_pl=(
            "Koncentryczne kółka dowodzą, że klasyfikator liniowy ma fundamentalne ograniczenia. "
            "KNN rozpoznaje wzorzec 'bliskie = ta sama klasa' i osiąga wysoką dokładność, "
            "podczas gdy linia prosta skazana jest na porażkę."
        ),
    ),
    Scenario(
        name_pl="Zaszumione chmury",
        kind="noisy_blobs",
        n_points=60,
        noise=0.30,
        hint_pl=(
            "Dwie chmury z dużym szumem — klasy częściowo się mieszają. "
            "Nikt nie osiągnie tu 100% dokładności, to normalne! "
            "Spróbuj znaleźć granicę minimalizującą błędy, "
            "ale nie staraj się być zbyt dokładny przy każdym punkcie."
        ),
        insight_pl=(
            "Gdy dane są zaszumione, nie ma idealnej granicy decyzyjnej. "
            "Zbyt precyzyjna granica działa świetnie na danych treningowych, "
            "ale słabo na nowych — to właśnie overfitting. "
            "Akceptacja 80–90% dokładności jest tu mądrzejsza."
        ),
    ),
    Scenario(
        name_pl="Zaszumione półksiężyce",
        kind="moons_noisy",
        n_points=60,
        noise=0.25,
        hint_pl=(
            "Półksiężyce z szumem — najtrudniejszy scenariusz. "
            "Klasy są splecione i chaotyczne. "
            "Narysuj granicę, która ogólnie oddziela górną od dolnej grupy, "
            "nie martwiąc się o każdy odstający punkt. To test intuicji, nie perfekcji."
        ),
        insight_pl=(
            "Zaszumione, nieliniowe dane to rzeczywistość uczenia maszynowego. "
            "Żaden klasyfikator nie dominuje jednoznacznie — "
            "to właśnie moment, gdy ważna jest walidacja krzyżowa "
            "i wybór progu akceptowalnego błędu."
        ),
    ),
]


def generate_data(scenario: Scenario, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Returns X (n, 2) normalised to [0,1]×[0,1], y (n,) with values 0 or 1."""
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

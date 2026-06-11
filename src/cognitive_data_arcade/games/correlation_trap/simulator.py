from __future__ import annotations
from dataclasses import dataclass
import hashlib
import math
import numpy as np


@dataclass
class CorrResult:
    x:        np.ndarray
    y:        np.ndarray
    r:        float
    r2:       float
    strength: str


@dataclass(frozen=True)
class Scenario:
    key:            str
    claim_pl:       str
    r_display:      float
    n:              int
    is_causal:      bool
    confound_pl:    str
    explanation_pl: str


def pearson_r(x: np.ndarray, y: np.ndarray) -> float:
    if x.std() == 0 or y.std() == 0:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def strength_label(r: float) -> str:
    sign = "+" if r >= 0 else "-"
    a = abs(r)
    if a < 0.10:
        return "brak"
    if a < 0.30:
        return f"słaba {sign}"
    if a < 0.50:
        return f"umiarkowana {sign}"
    if a < 0.70:
        return f"silna {sign}"
    return f"bardzo silna {sign}"


def generate_correlated(
    r: float,
    noise: float,
    n: int,
    seed: int | None = None,
) -> CorrResult:
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(n)
    z = rng.standard_normal(n)
    w = rng.standard_normal(n)
    y_base = r * x + math.sqrt(max(0.0, 1.0 - r * r)) * z
    y = y_base + noise * w
    actual_r = pearson_r(x, y)
    return CorrResult(
        x=x,
        y=y,
        r=actual_r,
        r2=actual_r ** 2,
        strength=strength_label(actual_r),
    )


_SCENARIOS: list[Scenario] = [
    Scenario(
        key="ice_cream",
        claim_pl="Wyższe spożycie lodów koreluje z liczbą utonięć w danym miesiącu.",
        r_display=0.88,
        n=120,
        is_causal=False,
        confound_pl="Pora roku (lato)",
        explanation_pl=(
            "Latem jest cieplej — więcej osób pływa (-> utonięcia) i je lody.\n"
            "Pora roku jest wspólną przyczyną obu zmiennych!"
        ),
    ),
    Scenario(
        key="cage_films",
        claim_pl="Liczba filmów z Nicolasem Cage koreluje z liczbą utonięć w basenach.",
        r_display=0.67,
        n=11,
        is_causal=False,
        confound_pl="Brak — czysto przypadkowa",
        explanation_pl=(
            "Klasyczny przykład ze spurious-correlations.com.\n"
            "Przy małym N (11 lat) łatwo o przypadkową korelację!"
        ),
    ),
    Scenario(
        key="iphone_suicide",
        claim_pl="Sprzedaż iPhone koreluje ze wskaźnikiem samobójstw w USA.",
        r_display=0.93,
        n=10,
        is_causal=False,
        confound_pl="Trend czasowy (2007-2017)",
        explanation_pl=(
            "Obie zmienne rosły w czasie z różnych powodów.\n"
            "Trend czasowy tworzy korelację bez związku przyczynowego!"
        ),
    ),
    Scenario(
        key="storks",
        claim_pl="Liczba bocianów w krajach Europy koreluje z liczbą urodzeń.",
        r_display=0.62,
        n=17,
        is_causal=False,
        confound_pl="Obszary wiejskie / rolnicze",
        explanation_pl=(
            "Bociany gniazdują na wsi, gdzie też rodzi się więcej dzieci.\n"
            "Wiejski charakter regionu to zmienna ukryta!"
        ),
    ),
    Scenario(
        key="shoe_reading",
        claim_pl="U dzieci rozmiar buta koreluje z umiejętnością czytania.",
        r_display=0.78,
        n=60,
        is_causal=False,
        confound_pl="Wiek dziecka",
        explanation_pl=(
            "Starsze dzieci mają większe stopy i lepiej czytają.\n"
            "Wiek jest zmienną ukrytą łączącą obie obserwacje!"
        ),
    ),
    Scenario(
        key="smoking_cancer",
        claim_pl="Liczba wypalanych papierosów dziennie koreluje z ryzykiem raka płuc.",
        r_display=0.85,
        n=200,
        is_causal=True,
        confound_pl="",
        explanation_pl=(
            "Zależność przyczynowa potwierdzona eksperymentami i badaniami kohortowymi!\n"
            "Substancje smoliste uszkadzają DNA komórek płuc."
        ),
    ),
    Scenario(
        key="sleep_rt",
        claim_pl="Krótszy czas snu koreluje z dłuższym czasem reakcji (r = -0.72).",
        r_display=-0.72,
        n=80,
        is_causal=True,
        confound_pl="",
        explanation_pl=(
            "Eksperymenty ze zmienionym snem potwierdzają przyczynowość.\n"
            "Mniej snu -> wolniejsze przetwarzanie poznawcze -> dłuższy RT."
        ),
    ),
    Scenario(
        key="study_exam",
        claim_pl="Liczba godzin nauki koreluje z wynikiem egzaminu.",
        r_display=0.71,
        n=150,
        is_causal=True,
        confound_pl="",
        explanation_pl=(
            "Eksperymenty potwierdzają: więcej nauki -> lepszy wynik.\n"
            "Uwaga: zdolności bazowe też mają rolę (zmienna moderująca)!"
        ),
    ),
]


_SANDBOX_VARS: list[dict] = [
    {"key": "lody",         "label": "Lody"},
    {"key": "utonecia",     "label": "Utonięcia"},
    {"key": "cage",         "label": "Cage (filmy)"},
    {"key": "iphone",       "label": "iPhone (sprzedaż)"},
    {"key": "czas_reakcji", "label": "Czas reakcji"},
    {"key": "nback",        "label": "N-back (wynik)"},
    {"key": "slonce",       "label": "Słońce (dni)"},
    {"key": "temperatura",  "label": "Temperatura"},
    {"key": "sen",          "label": "Sen (godz.)"},
    {"key": "nauka",        "label": "Nauka (godz.)"},
    {"key": "papierosy",    "label": "Papierosy"},
    {"key": "wzrost",       "label": "Wzrost (cm)"},
]

_VAR_CORRELATIONS: dict[tuple[str, str], float] = {
    ("lody",        "utonecia"):      0.88,
    ("lody",        "temperatura"):   0.91,
    ("utonecia",    "temperatura"):   0.85,
    ("cage",        "utonecia"):      0.67,
    ("iphone",      "utonecia"):      0.93,
    ("sen",         "czas_reakcji"):  -0.72,
    ("sen",         "nback"):         0.52,
    ("nauka",       "nback"):         0.45,
    ("slonce",      "temperatura"):   0.88,
    ("papierosy",   "czas_reakcji"):  0.38,
    ("wzrost",      "nback"):         0.05,
    ("wzrost",      "czas_reakcji"):  0.02,
}


def _sandbox_corr(x_key: str, y_key: str) -> float:
    r = _VAR_CORRELATIONS.get((x_key, y_key))
    if r is None:
        r = _VAR_CORRELATIONS.get((y_key, x_key), 0.0)
    return r


def _sandbox_seed(x_key: str, y_key: str) -> int:
    pair = "_".join(sorted([x_key, y_key]))
    return int(hashlib.md5(pair.encode()).hexdigest(), 16) & 0xFFFF

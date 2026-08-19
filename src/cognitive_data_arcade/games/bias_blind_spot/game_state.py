from __future__ import annotations

from dataclasses import dataclass, field

FEATURES: list[str] = ["income", "employment", "credit_history", "zip_code", "debt_ratio"]

ACT1_CORRECT = "zipcode"

STARTING_BIAS: float = 33.0
STARTING_ACC: float = 0.79

APPLICANTS: list[dict] = [
    {
        "name": "Amina B.",
        "income": 4100,
        "employment": "stable",
        "credit": "good",
        "zip": "Praga Pd.",
        "debt": 45,
        "approved": False,
    },
    {
        "name": "Fatima N.",
        "income": 4500,
        "employment": "stable",
        "credit": "good",
        "zip": "Praga Pd.",
        "debt": 42,
        "approved": False,
    },
    {
        "name": "Ibrahim O.",
        "income": 3900,
        "employment": "stable",
        "credit": "good",
        "zip": "Praga Pd.",
        "debt": 48,
        "approved": False,
    },
    {
        "name": "Marek W.",
        "income": 2900,
        "employment": "contract",
        "credit": "fair",
        "zip": "Wola",
        "debt": 30,
        "approved": True,
    },
    {
        "name": "Piotr M.",
        "income": 3200,
        "employment": "stable",
        "credit": "fair",
        "zip": "Zoliborz",
        "debt": 28,
        "approved": True,
    },
    {
        "name": "Jan K.",
        "income": 3800,
        "employment": "stable",
        "credit": "good",
        "zip": "Mokotow",
        "debt": 35,
        "approved": True,
    },
]

FEATURE_OUTCOMES: dict[frozenset, tuple[float, float]] = {
    frozenset(): (33.0, 0.79),
    frozenset({"zip_code"}): (21.0, 0.76),
    frozenset({"debt_ratio"}): (30.0, 0.77),
    frozenset({"income"}): (32.0, 0.75),
    frozenset({"employment"}): (32.0, 0.77),
    frozenset({"credit_history"}): (31.0, 0.74),
    frozenset({"zip_code", "debt_ratio"}): (14.0, 0.71),
    frozenset({"zip_code", "income"}): (19.0, 0.72),
    frozenset({"zip_code", "employment"}): (20.0, 0.73),
    frozenset({"zip_code", "credit_history"}): (20.0, 0.70),
    frozenset({"zip_code", "debt_ratio", "income"}): (9.0, 0.58),
    frozenset({"zip_code", "debt_ratio", "employment"}): (10.0, 0.61),
    frozenset({"zip_code", "debt_ratio", "credit_history"}): (11.0, 0.60),
    frozenset({"zip_code", "debt_ratio", "income", "employment"}): (7.0, 0.48),
    frozenset({"zip_code", "debt_ratio", "income", "credit_history"}): (7.0, 0.50),
    frozenset({"zip_code", "debt_ratio", "employment", "credit_history"}): (8.0, 0.52),
    frozenset({"zip_code", "debt_ratio", "income", "employment", "credit_history"}): (5.0, 0.41),
}

CONSEQUENCE_TABLE: dict[str, dict] = {
    "parity": {
        "parity": True,
        "opportunity": False,
        "calibration": False,
        "accuracy": 0.68,
    },
    "opportunity": {
        "parity": False,
        "opportunity": True,
        "calibration": False,
        "accuracy": 0.74,
    },
    "calibration": {
        "parity": False,
        "opportunity": False,
        "calibration": True,
        "accuracy": 0.79,
    },
}


def compute_round_result(removed: frozenset) -> tuple[float, float]:
    """Return (bias_gap_pp, accuracy) for given set of removed features."""
    if removed in FEATURE_OUTCOMES:
        return FEATURE_OUTCOMES[removed]
    has_zip = "zip_code" in removed
    has_debt = "debt_ratio" in removed
    n_other = len(removed) - (1 if has_zip else 0) - (1 if has_debt else 0)
    bias = STARTING_BIAS - (12.0 if has_zip else 0) - (7.0 if has_debt else 0) - n_other * 1.5
    acc = STARTING_ACC - (0.03 if has_zip else 0) - (0.08 if has_debt else 0) - n_other * 0.05
    return max(5.0, bias), max(0.35, min(STARTING_ACC, acc))


def compute_score_engineer(bias_reduction: float, accuracy_final: float) -> int:
    """Score in [0, 100]. max_possible_reduction=24 (33-9), baseline_acc=0.79."""
    raw = (bias_reduction / 24.0) * 50.0 + (accuracy_final / STARTING_ACC) * 50.0
    return max(0, min(100, int(raw)))


def stars_from_score(score: int) -> int:
    if score >= 70:
        return 3
    if score >= 45:
        return 2
    return 1


@dataclass
class GameState:
    act1_choice: str = ""
    act1_correct: bool = False
    bias_rounds: list[float] = field(default_factory=list)
    accuracy_rounds: list[float] = field(default_factory=list)
    regulator_choice: str = ""
    score_engineer: int = 0

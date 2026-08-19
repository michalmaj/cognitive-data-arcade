from __future__ import annotations

import random
import tomllib
from datetime import date
from pathlib import Path

_DEFAULT_PATH = Path(__file__).parent.parent / "data" / "daily_challenges.toml"

_REQUIRED_KEYS = {
    "id",
    "module_idx",
    "q_pl",
    "q_en",
    "options_pl",
    "options_en",
    "correct_idx",
    "explanation_pl",
    "explanation_en",
}


def load_questions(path: Path | None = None) -> list[dict]:
    """Load and validate questions from a TOML file.

    Raises FileNotFoundError if the file doesn't exist.
    Silently drops questions missing required keys.
    """
    p = path if path is not None else _DEFAULT_PATH
    with open(p, "rb") as f:
        data = tomllib.load(f)
    questions = data.get("questions", [])
    return [q for q in questions if q.keys() >= _REQUIRED_KEYS]


def pick_daily(questions: list[dict], today: date, n: int = 5) -> list[dict]:
    """Return n questions for today, deterministically seeded by date.

    If the bank has fewer than n questions, returns all questions.
    """
    if not questions:
        return []
    rng = random.Random(today.toordinal())
    shuffled = questions.copy()
    rng.shuffle(shuffled)
    return shuffled[:n]

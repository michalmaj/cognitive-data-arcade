from datetime import date
from pathlib import Path

import pytest

from cognitive_data_arcade.engine.challenge_loader import load_questions, pick_daily

SAMPLE_TOML = """\
[[questions]]
id = "t001"
module_idx = 0
q_pl = "Pytanie 1 PL"
q_en = "Question 1 EN"
options_pl = ["A", "B", "C", "D"]
options_en = ["A", "B", "C", "D"]
correct_idx = 0
explanation_pl = "Wyjasnienie 1"
explanation_en = "Explanation 1"

[[questions]]
id = "t002"
module_idx = 1
q_pl = "Pytanie 2 PL"
q_en = "Question 2 EN"
options_pl = ["A", "B", "C", "D"]
options_en = ["A", "B", "C", "D"]
correct_idx = 1
explanation_pl = "Wyjasnienie 2"
explanation_en = "Explanation 2"

[[questions]]
id = "t003"
module_idx = 2
q_pl = "Pytanie 3 PL"
q_en = "Question 3 EN"
options_pl = ["A", "B", "C", "D"]
options_en = ["A", "B", "C", "D"]
correct_idx = 2
explanation_pl = "Wyjasnienie 3"
explanation_en = "Explanation 3"
"""


@pytest.fixture
def toml_file(tmp_path):
    f = tmp_path / "daily_challenges.toml"
    f.write_text(SAMPLE_TOML, encoding="utf-8")
    return f


def test_load_questions_returns_list(toml_file):
    qs = load_questions(toml_file)
    assert len(qs) == 3
    assert qs[0]["id"] == "t001"
    assert qs[1]["correct_idx"] == 1


def test_load_questions_has_required_keys(toml_file):
    qs = load_questions(toml_file)
    required = {
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
    for q in qs:
        assert required <= q.keys()


def test_pick_daily_deterministic(toml_file):
    today = date(2026, 6, 26)
    qs1 = load_questions(toml_file)
    qs2 = load_questions(toml_file)
    result1 = pick_daily(qs1, today, n=2)
    result2 = pick_daily(qs2, today, n=2)
    assert [q["id"] for q in result1] == [q["id"] for q in result2]


def test_pick_daily_different_days(toml_file):
    qs = load_questions(toml_file)
    day_a = pick_daily(qs, date(2026, 6, 26), n=2)
    day_b = pick_daily(qs, date(2026, 6, 27), n=2)
    ids_a = [q["id"] for q in day_a]
    ids_b = [q["id"] for q in day_b]
    # Can't guarantee different order but seeds are different — just verify no crash
    assert len(ids_a) == 2
    assert len(ids_b) == 2


def test_pick_daily_fewer_than_n(toml_file):
    qs = load_questions(toml_file)
    result = pick_daily(qs, date(2026, 6, 26), n=10)
    assert len(result) == 3  # returns all when bank < n


def test_load_questions_missing_file():
    with pytest.raises(FileNotFoundError):
        load_questions(Path("/nonexistent/daily_challenges.toml"))

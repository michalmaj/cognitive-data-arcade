from __future__ import annotations

import csv
from pathlib import Path

import pytest

from cognitive_data_arcade.games.cognitive_dashboard.csv_loader import (
    has_any_csv_data,
    load_session_from_csv,
)
from cognitive_data_arcade.games.cognitive_dashboard.session import TaskResult


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def _stroop_row(condition: str, correct: bool, rt: float) -> dict:
    return {
        "participant_id": "p1",
        "session_id": "s1",
        "trial_id": "1",
        "task_name": "stroop",
        "condition": condition,
        "stimulus": "RED",
        "ink_color": "red",
        "word_color": "red",
        "expected_response": "r",
        "actual_response": "r" if correct else "g",
        "correct": str(correct),
        "reaction_time_ms": str(rt),
        "timestamp": "2026-01-01T00:00:00",
    }


def _flanker_row(condition: str, correct: bool, rt: float) -> dict:
    return {
        "participant_id": "p1",
        "session_id": "s1",
        "trial_id": "1",
        "task_name": "flanker",
        "condition": condition,
        "target_direction": "left",
        "correct": str(correct),
        "reaction_time_ms": str(rt),
        "timestamp": "2026-01-01T00:00:00",
    }


def _gono_row(trial_type: str, correct: bool, rt: float) -> dict:
    return {
        "participant_id": "p1",
        "session_id": "s1",
        "trial_id": "1",
        "task_name": "gono",
        "trial_type": trial_type,
        "response": "hit",
        "correct": str(correct),
        "reaction_time_ms": str(rt),
        "timestamp": "2026-01-01T00:00:00",
    }


def _rt_row(correct: bool, rt: float) -> dict:
    return {
        "participant_id": "p1",
        "session_id": "s1",
        "trial_id": "1",
        "task_name": "reaction_time",
        "condition": "simple",
        "stimulus": "circle",
        "expected_response": "space",
        "actual_response": "space" if correct else "",
        "correct": str(correct),
        "reaction_time_ms": str(rt),
        "timestamp": "2026-01-01T00:00:00",
        "distractor_count": "0",
    }


@pytest.fixture()
def data_root(tmp_path, monkeypatch):
    """Redirect _DATA_ROOT to tmp_path so tests are isolated."""
    import cognitive_data_arcade.games.cognitive_dashboard.csv_loader as mod

    monkeypatch.setattr(mod, "_DATA_ROOT", tmp_path)
    return tmp_path


def test_has_any_csv_data_false_when_empty(data_root):
    assert not has_any_csv_data()


def test_has_any_csv_data_true_when_stroop_csv_exists(data_root):
    _write_csv(data_root / "stroop" / "s1.csv", [_stroop_row("congruent", True, 500.0)])
    assert has_any_csv_data()


def test_load_session_all_none_when_no_files(data_root):
    session = load_session_from_csv()
    assert session.rt is None
    assert session.stroop is None
    assert session.flanker is None
    assert session.gonogo is None
    assert not session.synthetic


def test_load_stroop_csv(data_root):
    rows = [
        _stroop_row("congruent", True, 400.0),
        _stroop_row("incongruent", False, 600.0),
    ]
    _write_csv(data_root / "stroop" / "s1.csv", rows)
    session = load_session_from_csv()
    assert isinstance(session.stroop, TaskResult)
    assert session.stroop.rt_ms == [400.0, 600.0]
    assert session.stroop.correct == [True, False]
    assert session.stroop.condition == ["congruent", "incongruent"]


def test_load_flanker_csv(data_root):
    rows = [_flanker_row("congruent", True, 350.0), _flanker_row("incongruent", True, 500.0)]
    _write_csv(data_root / "flanker" / "s1.csv", rows)
    session = load_session_from_csv()
    assert isinstance(session.flanker, TaskResult)
    assert len(session.flanker.rt_ms) == 2


def test_load_gono_uses_trial_type_as_condition(data_root):
    rows = [_gono_row("go", True, 280.0), _gono_row("nogo", False, 0.0)]
    _write_csv(data_root / "gono" / "s1.csv", rows)
    session = load_session_from_csv()
    assert isinstance(session.gonogo, TaskResult)
    assert session.gonogo.condition == ["go", "nogo"]


def test_load_rt_csv(data_root):
    rows = [_rt_row(True, 220.0), _rt_row(True, 250.0)]
    _write_csv(data_root / "reaction_time" / "s1.csv", rows)
    session = load_session_from_csv()
    assert isinstance(session.rt, TaskResult)
    assert session.rt.condition == ["simple", "simple"]


def test_multiple_csv_files_combined(data_root):
    _write_csv(
        data_root / "stroop" / "s1.csv",
        [_stroop_row("congruent", True, 400.0)],
    )
    _write_csv(
        data_root / "stroop" / "s2.csv",
        [_stroop_row("incongruent", False, 600.0)],
    )
    session = load_session_from_csv()
    assert len(session.stroop.rt_ms) == 2


def test_max_trials_cap(data_root, monkeypatch):
    import cognitive_data_arcade.games.cognitive_dashboard.csv_loader as mod

    monkeypatch.setattr(mod, "_MAX_TRIALS", 3)
    rows = [_stroop_row("congruent", True, float(i)) for i in range(10)]
    _write_csv(data_root / "stroop" / "s1.csv", rows)
    session = load_session_from_csv()
    assert len(session.stroop.rt_ms) == 3


def test_malformed_row_skipped(data_root):
    path = data_root / "stroop" / "s1.csv"
    path.parent.mkdir(parents=True)
    path.write_text(
        "participant_id,reaction_time_ms,correct,condition\np1,not_a_number,True,congruent\n"
    )
    session = load_session_from_csv()
    assert session.stroop is None

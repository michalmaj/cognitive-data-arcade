import csv
from pathlib import Path

import pytest
from matplotlib.figure import Figure

from cognitive_data_arcade.analytics.stroop_analysis import (
    build_stroop_chart,
    load_session,
    session_stats,
)

# 12 trials: 4 congruent avg=265, 4 neutral avg=315, 4 incongruent avg=415
_ROWS = [
    # congruent
    {"participant_id": "p1", "session_id": "s1", "trial_id": "1",
     "task_name": "stroop", "condition": "congruent",
     "stimulus": "CZERWONY", "ink_color": "red", "word_color": "red",
     "expected_response": "r", "actual_response": "r", "correct": "True",
     "reaction_time_ms": "250.0", "timestamp": "2026-01-01T00:00:00+00:00"},
    {"participant_id": "p1", "session_id": "s1", "trial_id": "2",
     "task_name": "stroop", "condition": "congruent",
     "stimulus": "ZIELONY", "ink_color": "green", "word_color": "green",
     "expected_response": "g", "actual_response": "g", "correct": "True",
     "reaction_time_ms": "270.0", "timestamp": "2026-01-01T00:00:01+00:00"},
    {"participant_id": "p1", "session_id": "s1", "trial_id": "3",
     "task_name": "stroop", "condition": "congruent",
     "stimulus": "NIEBIESKI", "ink_color": "blue", "word_color": "blue",
     "expected_response": "b", "actual_response": "b", "correct": "True",
     "reaction_time_ms": "260.0", "timestamp": "2026-01-01T00:00:02+00:00"},
    {"participant_id": "p1", "session_id": "s1", "trial_id": "4",
     "task_name": "stroop", "condition": "congruent",
     "stimulus": "ŻÓŁTY", "ink_color": "yellow", "word_color": "yellow",
     "expected_response": "y", "actual_response": "y", "correct": "True",
     "reaction_time_ms": "280.0", "timestamp": "2026-01-01T00:00:03+00:00"},
    # neutral
    {"participant_id": "p1", "session_id": "s1", "trial_id": "5",
     "task_name": "stroop", "condition": "neutral",
     "stimulus": "XXXXX", "ink_color": "red", "word_color": "none",
     "expected_response": "r", "actual_response": "r", "correct": "True",
     "reaction_time_ms": "300.0", "timestamp": "2026-01-01T00:00:04+00:00"},
    {"participant_id": "p1", "session_id": "s1", "trial_id": "6",
     "task_name": "stroop", "condition": "neutral",
     "stimulus": "XXXXX", "ink_color": "green", "word_color": "none",
     "expected_response": "g", "actual_response": "g", "correct": "True",
     "reaction_time_ms": "320.0", "timestamp": "2026-01-01T00:00:05+00:00"},
    {"participant_id": "p1", "session_id": "s1", "trial_id": "7",
     "task_name": "stroop", "condition": "neutral",
     "stimulus": "XXXXX", "ink_color": "blue", "word_color": "none",
     "expected_response": "b", "actual_response": "b", "correct": "True",
     "reaction_time_ms": "310.0", "timestamp": "2026-01-01T00:00:06+00:00"},
    {"participant_id": "p1", "session_id": "s1", "trial_id": "8",
     "task_name": "stroop", "condition": "neutral",
     "stimulus": "XXXXX", "ink_color": "yellow", "word_color": "none",
     "expected_response": "y", "actual_response": "y", "correct": "True",
     "reaction_time_ms": "330.0", "timestamp": "2026-01-01T00:00:07+00:00"},
    # incongruent
    {"participant_id": "p1", "session_id": "s1", "trial_id": "9",
     "task_name": "stroop", "condition": "incongruent",
     "stimulus": "CZERWONY", "ink_color": "green", "word_color": "red",
     "expected_response": "g", "actual_response": "g", "correct": "True",
     "reaction_time_ms": "400.0", "timestamp": "2026-01-01T00:00:08+00:00"},
    {"participant_id": "p1", "session_id": "s1", "trial_id": "10",
     "task_name": "stroop", "condition": "incongruent",
     "stimulus": "ZIELONY", "ink_color": "blue", "word_color": "green",
     "expected_response": "b", "actual_response": "b", "correct": "True",
     "reaction_time_ms": "420.0", "timestamp": "2026-01-01T00:00:09+00:00"},
    {"participant_id": "p1", "session_id": "s1", "trial_id": "11",
     "task_name": "stroop", "condition": "incongruent",
     "stimulus": "NIEBIESKI", "ink_color": "yellow", "word_color": "blue",
     "expected_response": "y", "actual_response": "y", "correct": "True",
     "reaction_time_ms": "410.0", "timestamp": "2026-01-01T00:00:10+00:00"},
    {"participant_id": "p1", "session_id": "s1", "trial_id": "12",
     "task_name": "stroop", "condition": "incongruent",
     "stimulus": "ŻÓŁTY", "ink_color": "red", "word_color": "yellow",
     "expected_response": "r", "actual_response": "r", "correct": "True",
     "reaction_time_ms": "430.0", "timestamp": "2026-01-01T00:00:11+00:00"},
]

_TIMEOUT_ROWS = [
    {"participant_id": "p1", "session_id": "s2", "trial_id": "1",
     "task_name": "stroop", "condition": "congruent",
     "stimulus": "CZERWONY", "ink_color": "red", "word_color": "red",
     "expected_response": "r", "actual_response": "none", "correct": "False",
     "reaction_time_ms": "-1.0", "timestamp": "2026-01-01T00:00:00+00:00"},
    {"participant_id": "p1", "session_id": "s2", "trial_id": "2",
     "task_name": "stroop", "condition": "neutral",
     "stimulus": "XXXXX", "ink_color": "green", "word_color": "none",
     "expected_response": "g", "actual_response": "none", "correct": "False",
     "reaction_time_ms": "-1.0", "timestamp": "2026-01-01T00:00:01+00:00"},
    {"participant_id": "p1", "session_id": "s2", "trial_id": "3",
     "task_name": "stroop", "condition": "incongruent",
     "stimulus": "CZERWONY", "ink_color": "green", "word_color": "red",
     "expected_response": "g", "actual_response": "none", "correct": "False",
     "reaction_time_ms": "-1.0", "timestamp": "2026-01-01T00:00:02+00:00"},
]


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def test_load_session_returns_dataframe(tmp_path: Path) -> None:
    csv_path = tmp_path / "s1.csv"
    _write_csv(csv_path, _ROWS)
    df = load_session(csv_path)
    assert list(df.columns[:4]) == [
        "participant_id", "session_id", "trial_id", "task_name"
    ]
    assert len(df) == 12


def test_session_stats_per_condition(tmp_path: Path) -> None:
    csv_path = tmp_path / "s1.csv"
    _write_csv(csv_path, _ROWS)
    df = load_session(csv_path)
    stats = session_stats(df)
    # congruent: (250+270+260+280)/4 = 265
    assert stats["avg_rt_congruent"] == pytest.approx(265.0)
    # neutral: (300+320+310+330)/4 = 315
    assert stats["avg_rt_neutral"] == pytest.approx(315.0)
    # incongruent: (400+420+410+430)/4 = 415
    assert stats["avg_rt_incongruent"] == pytest.approx(415.0)


def test_session_stats_facilitation_interference(tmp_path: Path) -> None:
    csv_path = tmp_path / "s1.csv"
    _write_csv(csv_path, _ROWS)
    df = load_session(csv_path)
    stats = session_stats(df)
    # facilitation = neutral - congruent = 315 - 265 = 50
    assert stats["facilitation_ms"] == pytest.approx(50.0)
    # interference = incongruent - neutral = 415 - 315 = 100
    assert stats["interference_ms"] == pytest.approx(100.0)
    # stroop_effect = incongruent - congruent = 415 - 265 = 150
    assert stats["stroop_effect_ms"] == pytest.approx(150.0)


def test_session_stats_all_timeouts(tmp_path: Path) -> None:
    csv_path = tmp_path / "s2.csv"
    _write_csv(csv_path, _TIMEOUT_ROWS)
    df = load_session(csv_path)
    stats = session_stats(df)
    assert stats["avg_rt_congruent"] == 0.0
    assert stats["avg_rt_neutral"] == 0.0
    assert stats["avg_rt_incongruent"] == 0.0
    assert stats["facilitation_ms"] == 0.0
    assert stats["interference_ms"] == 0.0
    assert stats["stroop_effect_ms"] == 0.0
    assert stats["accuracy"] == 0.0
    assert stats["n_trials"] == 3


def test_build_stroop_chart_returns_figure(tmp_path: Path) -> None:
    csv_path = tmp_path / "s1.csv"
    _write_csv(csv_path, _ROWS)
    df = load_session(csv_path)
    fig = build_stroop_chart(df)
    assert isinstance(fig, Figure)

import csv
from pathlib import Path

import pytest
from matplotlib.figure import Figure

from cognitive_data_arcade.analytics.rt_analysis import (
    build_histogram,
    load_session,
    session_stats,
)

# Fixture rows: 2 correct (200 ms, 300 ms), 1 timeout (-1)
_ROWS = [
    {
        "participant_id": "p1",
        "session_id": "s1",
        "trial_id": 1,
        "task_name": "reaction_time",
        "condition": "simple",
        "stimulus": "circle",
        "expected_response": "space",
        "actual_response": "space",
        "correct": "True",
        "reaction_time_ms": "200.0",
        "timestamp": "2026-05-26T10:00:00+00:00",
        "distractor_count": "3",
    },
    {
        "participant_id": "p1",
        "session_id": "s1",
        "trial_id": 2,
        "task_name": "reaction_time",
        "condition": "simple",
        "stimulus": "circle",
        "expected_response": "space",
        "actual_response": "space",
        "correct": "True",
        "reaction_time_ms": "300.0",
        "timestamp": "2026-05-26T10:00:01+00:00",
        "distractor_count": "3",
    },
    {
        "participant_id": "p1",
        "session_id": "s1",
        "trial_id": 3,
        "task_name": "reaction_time",
        "condition": "simple",
        "stimulus": "circle",
        "expected_response": "space",
        "actual_response": "none",
        "correct": "False",
        "reaction_time_ms": "-1.0",
        "timestamp": "2026-05-26T10:00:02+00:00",
        "distractor_count": "3",
    },
]

_TIMEOUT_ROWS = [
    {
        "participant_id": "p1",
        "session_id": "s2",
        "trial_id": 1,
        "task_name": "reaction_time",
        "condition": "simple",
        "stimulus": "circle",
        "expected_response": "space",
        "actual_response": "none",
        "correct": "False",
        "reaction_time_ms": "-1.0",
        "timestamp": "2026-05-26T10:00:00+00:00",
        "distractor_count": "3",
    },
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
        "participant_id",
        "session_id",
        "trial_id",
        "task_name",
    ]
    assert len(df) == 3


def test_session_stats_correct_values(tmp_path: Path) -> None:
    csv_path = tmp_path / "s1.csv"
    _write_csv(csv_path, _ROWS)
    df = load_session(csv_path)
    stats = session_stats(df)
    assert stats["avg_rt"] == pytest.approx(250.0)
    assert stats["median_rt"] == pytest.approx(250.0)
    assert stats["min_rt"] == pytest.approx(200.0)
    assert stats["max_rt"] == pytest.approx(300.0)
    assert stats["accuracy"] == pytest.approx(2 / 3)
    assert stats["n_trials"] == 3
    assert stats["n_correct"] == 2


def test_session_stats_all_timeouts(tmp_path: Path) -> None:
    csv_path = tmp_path / "s2.csv"
    _write_csv(csv_path, _TIMEOUT_ROWS)
    df = load_session(csv_path)
    stats = session_stats(df)
    assert stats["avg_rt"] == 0.0
    assert stats["accuracy"] == 0.0
    assert stats["n_trials"] == 1


def test_build_histogram_returns_figure(tmp_path: Path) -> None:
    csv_path = tmp_path / "s1.csv"
    _write_csv(csv_path, _ROWS)
    df = load_session(csv_path)
    fig = build_histogram(df)
    assert isinstance(fig, Figure)

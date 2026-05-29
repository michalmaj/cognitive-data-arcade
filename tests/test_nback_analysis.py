from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd
import pytest
from matplotlib.figure import Figure

from cognitive_data_arcade.analytics.nback_analysis import (
    build_chart,
    load_session,
    session_stats,
)

_COLS = [
    "task_name", "participant_id", "session_id", "trial_id", "block_id", "n_level",
    "position", "letter", "pos_match", "let_match", "key_a_pressed", "key_l_pressed",
    "pos_correct", "let_correct", "rt_a_ms", "rt_l_ms",
]


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_COLS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _row(i: int, block: int = 1, n: int = 1, pos_match: bool = False,
         let_match: bool = False, key_a: bool = False, key_l: bool = False) -> dict:
    return {
        "task_name": "nback", "participant_id": "p1", "session_id": "s1",
        "trial_id": i, "block_id": block, "n_level": n,
        "position": 0, "letter": "B",
        "pos_match": pos_match, "let_match": let_match,
        "key_a_pressed": key_a, "key_l_pressed": key_l,
        "pos_correct": pos_match == key_a,
        "let_correct": let_match == key_l,
        "rt_a_ms": 350.0 if key_a else 0.0,
        "rt_l_ms": 400.0 if key_l else 0.0,
    }


@pytest.fixture
def fixture_csv(tmp_path: Path) -> Path:
    rows = [_row(i + 1) for i in range(20)]
    path = tmp_path / "nback" / "test.csv"
    _write_csv(path, rows)
    return path


@pytest.fixture
def adaptive_csv(tmp_path: Path) -> Path:
    rows = (
        [_row(i + 1, block=1, n=1) for i in range(10)]
        + [_row(i + 11, block=2, n=2) for i in range(10)]
    )
    path = tmp_path / "nback" / "adaptive.csv"
    _write_csv(path, rows)
    return path


def test_load_session_returns_dataframe(fixture_csv: Path) -> None:
    df = load_session(fixture_csv)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 20


def test_load_session_bool_columns(fixture_csv: Path) -> None:
    df = load_session(fixture_csv)
    for col in ("pos_match", "let_match", "key_a_pressed", "key_l_pressed",
                "pos_correct", "let_correct"):
        assert df[col].dtype == bool


def test_session_stats_all_keys_present(fixture_csv: Path) -> None:
    df = load_session(fixture_csv)
    stats = session_stats(df)
    for key in ("pos_accuracy", "let_accuracy", "pos_dprime", "let_dprime",
                "mean_n_level", "final_n_level", "total_trials"):
        assert key in stats, f"missing key: {key}"


def test_session_stats_total_trials(fixture_csv: Path) -> None:
    df = load_session(fixture_csv)
    assert session_stats(df)["total_trials"] == 20.0


def test_session_stats_accuracy_range(fixture_csv: Path) -> None:
    df = load_session(fixture_csv)
    stats = session_stats(df)
    assert 0.0 <= stats["pos_accuracy"] <= 1.0
    assert 0.0 <= stats["let_accuracy"] <= 1.0


def test_build_chart_returns_figure(fixture_csv: Path) -> None:
    df = load_session(fixture_csv)
    fig = build_chart(df)
    assert isinstance(fig, Figure)


def test_build_chart_adaptive_includes_n_subplot(adaptive_csv: Path) -> None:
    df = load_session(adaptive_csv)
    fig = build_chart(df)
    assert len(fig.axes) == 2

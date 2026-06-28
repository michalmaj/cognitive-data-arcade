# tests/test_data_stats.py
from __future__ import annotations

from pathlib import Path

from cognitive_data_arcade.ui.data_stats import compute_data_stats, compute_quiz_accuracy


def test_empty_dir_returns_zeros(tmp_path: Path) -> None:
    stats = compute_data_stats(tmp_path / "nonexistent")
    assert stats["sessions"] == 0
    assert stats["data_points"] == 0
    assert stats["active_days"] == 0


def test_counts_csv_files_as_sessions(tmp_path: Path) -> None:
    gen = tmp_path / "generated"
    (gen / "task_a").mkdir(parents=True)
    (gen / "task_a" / "20260101_120000.csv").write_text("col\n1\n2\n")
    (gen / "task_a" / "20260102_130000.csv").write_text("col\n3\n")
    stats = compute_data_stats(gen)
    assert stats["sessions"] == 2


def test_counts_data_points_across_files(tmp_path: Path) -> None:
    gen = tmp_path / "generated"
    (gen / "rt").mkdir(parents=True)
    # 2 data rows + header
    (gen / "rt" / "20260101_120000.csv").write_text("col\n1\n2\n")
    # 3 data rows + header
    (gen / "rt" / "20260102_130000.csv").write_text("col\n3\n4\n5\n")
    stats = compute_data_stats(gen)
    assert stats["data_points"] == 5


def test_counts_unique_active_days(tmp_path: Path) -> None:
    gen = tmp_path / "generated" / "rt"
    gen.mkdir(parents=True)
    (gen / "20260101_090000.csv").write_text("col\n1\n")
    (gen / "20260101_150000.csv").write_text("col\n1\n")  # same day
    (gen / "20260102_100000.csv").write_text("col\n1\n")
    stats = compute_data_stats(gen.parent)
    assert stats["active_days"] == 2


def test_compute_quiz_accuracy_empty() -> None:
    assert compute_quiz_accuracy({}) is None


def test_compute_quiz_accuracy_all_correct() -> None:
    assert compute_quiz_accuracy({"L1": True, "L2": True}) == 100


def test_compute_quiz_accuracy_mixed() -> None:
    result = compute_quiz_accuracy({"L1": True, "L2": False, "L3": True, "L4": True})
    assert result == 75

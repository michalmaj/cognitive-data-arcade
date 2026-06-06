# tests/test_data_cleaning_generator.py
from __future__ import annotations

import pytest

from cognitive_data_arcade.games.data_cleaning.difficulty import EASY, MEDIUM, HARD
from cognitive_data_arcade.games.data_cleaning.generator import (
    CleaningSession,
    DataRow,
    ErrorType,
    apply_fixes,
    compute_score,
    compute_stats,
    generate_dataset,
    get_fix_feedback,
)


def test_generate_dataset_easy_returns_15_rows():
    session = generate_dataset(EASY, seed=42)
    assert len(session.rows) == 15


def test_generate_dataset_hard_returns_100_rows():
    session = generate_dataset(HARD, seed=42)
    assert len(session.rows) == 100


def test_generate_dataset_easy_error_count_in_range():
    for seed in range(20):
        session = generate_dataset(EASY, seed=seed)
        n = len(session.ground_truth)
        assert EASY.errors_min <= n <= EASY.errors_max, f"seed={seed}: {n} errors"


def test_generate_dataset_medium_error_count_in_range():
    for seed in range(10):
        session = generate_dataset(MEDIUM, seed=seed)
        n = len(session.ground_truth)
        assert MEDIUM.errors_min <= n <= MEDIUM.errors_max, f"seed={seed}: {n} errors"


def test_generate_dataset_hard_error_count_in_range():
    for seed in range(10):
        session = generate_dataset(HARD, seed=seed)
        n = len(session.ground_truth)
        assert HARD.errors_min <= n <= HARD.errors_max, f"seed={seed}: {n} errors"


def test_generate_dataset_is_deterministic():
    s1 = generate_dataset(EASY, seed=99)
    s2 = generate_dataset(EASY, seed=99)
    assert s1.ground_truth == s2.ground_truth
    for r1, r2 in zip(s1.rows, s2.rows):
        assert r1 == r2


def test_ground_truth_indices_within_range():
    session = generate_dataset(EASY, seed=0)
    for idx in session.ground_truth:
        assert 0 <= idx < len(session.rows)


def test_negative_rt_error_has_negative_value():
    for seed in range(20):
        session = generate_dataset(EASY, seed=seed)
        for idx, etype in session.ground_truth.items():
            if etype == ErrorType.NEGATIVE_RT:
                assert session.rows[idx].rt_ms is not None
                assert session.rows[idx].rt_ms < 0


def test_outlier_placeholder_has_known_value():
    _OUTLIER_VALUES = (9999.0, -99.0, 0.0)
    for seed in range(20):
        session = generate_dataset(EASY, seed=seed)
        for idx, etype in session.ground_truth.items():
            if etype == ErrorType.OUTLIER_PLACEHOLDER:
                assert session.rows[idx].rt_ms in _OUTLIER_VALUES


def test_missing_value_has_none_rt():
    for seed in range(20):
        session = generate_dataset(EASY, seed=seed)
        for idx, etype in session.ground_truth.items():
            if etype == ErrorType.MISSING_VALUE:
                assert session.rows[idx].rt_ms is None


def test_wrong_format_accuracy_above_one():
    for seed in range(20):
        session = generate_dataset(EASY, seed=seed)
        for idx, etype in session.ground_truth.items():
            if etype == ErrorType.WRONG_FORMAT_ACCURACY:
                assert session.rows[idx].accuracy is not None
                assert session.rows[idx].accuracy > 1.0


def test_get_fix_feedback_correct_for_delete_negative_rt():
    assert get_fix_feedback(ErrorType.NEGATIVE_RT, "delete") == "correct"


def test_get_fix_feedback_suboptimal_for_median_negative_rt():
    assert get_fix_feedback(ErrorType.NEGATIVE_RT, "median") == "suboptimal"


def test_get_fix_feedback_wrong_for_keep_negative_rt():
    assert get_fix_feedback(ErrorType.NEGATIVE_RT, "keep") == "wrong"


def test_get_fix_feedback_none_error_keep_is_correct():
    assert get_fix_feedback(None, "keep") == "correct"


def test_get_fix_feedback_none_error_delete_is_wrong():
    assert get_fix_feedback(None, "delete") == "wrong"


def test_compute_stats_returns_expected_keys():
    session = generate_dataset(EASY, seed=42)
    stats = compute_stats(session.rows)
    assert "n_rows" in stats
    assert "mean_rt" in stats
    assert "std_rt" in stats
    assert "mean_accuracy" in stats


def test_compute_score_perfect_detection():
    session = generate_dataset(EASY, seed=42)
    flagged = set(session.ground_truth.keys())
    fixes = {i: "delete" for i in flagged}
    d, f, total = compute_score(session, flagged, fixes)
    assert d == 60
    assert total >= 60


def test_compute_score_no_flags():
    session = generate_dataset(EASY, seed=42)
    d, f, total = compute_score(session, set(), {})
    assert d == 0
    assert total == 0


def test_apply_fixes_delete_removes_row():
    session = generate_dataset(EASY, seed=42)
    idx = next(iter(session.ground_truth))
    flagged = {idx}
    fixes = {idx: "delete"}
    result = apply_fixes(session, flagged, fixes)
    assert len(result) == len(session.rows) - 1


def test_apply_fixes_keep_preserves_row():
    session = generate_dataset(EASY, seed=42)
    idx = next(iter(session.ground_truth))
    flagged = {idx}
    fixes = {idx: "keep"}
    result = apply_fixes(session, flagged, fixes)
    assert len(result) == len(session.rows)


def test_compute_stats_std_uses_bessel_correction():
    rows = [
        DataRow(1, 1, 1, 300.0, 0.9),
        DataRow(1, 1, 2, 400.0, 0.9),
        DataRow(1, 1, 3, 500.0, 0.9),
    ]
    stats = compute_stats(rows)
    import math
    expected_std = math.sqrt(((300-400)**2 + (400-400)**2 + (500-400)**2) / 2)
    assert abs(stats["std_rt"] - expected_std) < 0.01


def test_apply_fixes_fix_format_divides_accuracy():
    rows = [DataRow(1, 1, 1, 300.0, 85.0)]
    from cognitive_data_arcade.games.data_cleaning.generator import CleaningSession, ErrorType
    session = CleaningSession(rows=rows, ground_truth={0: ErrorType.WRONG_FORMAT_ACCURACY})
    result = apply_fixes(session, {0}, {0: "fix_format"})
    assert abs(result[0].accuracy - 0.85) < 0.001


def test_compute_stats_excludes_outlier_placeholders():
    rows = [
        DataRow(1, 1, 1, 9999.0, 0.9),
        DataRow(1, 1, 2, 400.0, 0.9),
    ]
    stats = compute_stats(rows)
    assert abs(stats["mean_rt"] - 400.0) < 0.01

# tests/test_data_cleaning_generator.py
from __future__ import annotations

import pytest

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


def test_generate_dataset_returns_30_rows():
    session = generate_dataset(seed=42)
    assert len(session.rows) == 30


def test_generate_dataset_error_count_in_range():
    for seed in range(20):
        session = generate_dataset(seed=seed)
        n = len(session.ground_truth)
        assert 6 <= n <= 12, f"seed={seed}: {n} errors"


def test_generate_dataset_is_deterministic():
    s1 = generate_dataset(seed=99)
    s2 = generate_dataset(seed=99)
    assert s1.ground_truth == s2.ground_truth
    for r1, r2 in zip(s1.rows, s2.rows):
        assert r1 == r2


def test_ground_truth_indices_within_range():
    session = generate_dataset(seed=0)
    for idx in session.ground_truth:
        assert 0 <= idx < len(session.rows)


def test_negative_rt_error_has_negative_value():
    for seed in range(20):
        session = generate_dataset(seed=seed)
        for idx, etype in session.ground_truth.items():
            if etype == ErrorType.NEGATIVE_RT:
                assert session.rows[idx].rt_ms is not None
                assert session.rows[idx].rt_ms < 0


def test_outlier_placeholder_has_known_value():
    outlier_vals = {9999.0, -99.0, 0.0}
    for seed in range(20):
        session = generate_dataset(seed=seed)
        for idx, etype in session.ground_truth.items():
            if etype == ErrorType.OUTLIER_PLACEHOLDER:
                assert session.rows[idx].rt_ms in outlier_vals


def test_missing_value_has_none_rt():
    for seed in range(20):
        session = generate_dataset(seed=seed)
        for idx, etype in session.ground_truth.items():
            if etype == ErrorType.MISSING_VALUE:
                assert session.rows[idx].rt_ms is None


def test_wrong_format_accuracy_above_one():
    for seed in range(20):
        session = generate_dataset(seed=seed)
        for idx, etype in session.ground_truth.items():
            if etype == ErrorType.WRONG_FORMAT_ACCURACY:
                assert session.rows[idx].accuracy is not None
                assert session.rows[idx].accuracy > 1.0


def test_duplicate_row_creates_matching_participant_trial():
    for seed in range(20):
        session = generate_dataset(seed=seed)
        for idx, etype in session.ground_truth.items():
            if etype == ErrorType.DUPLICATE_ROW:
                row = session.rows[idx]
                others = [r for j, r in enumerate(session.rows) if j != idx]
                has_match = any(
                    r.participant_id == row.participant_id and r.trial == row.trial
                    for r in others
                )
                assert has_match, f"seed={seed}, idx={idx}"


# ── get_fix_feedback ────────────────────────────────────────────────────────────

def test_delete_is_correct_for_negative_rt():
    assert get_fix_feedback(ErrorType.NEGATIVE_RT, "delete") == "correct"


def test_keep_is_wrong_for_negative_rt():
    assert get_fix_feedback(ErrorType.NEGATIVE_RT, "keep") == "wrong"


def test_median_is_suboptimal_for_negative_rt():
    assert get_fix_feedback(ErrorType.NEGATIVE_RT, "median") == "suboptimal"


def test_both_delete_and_median_correct_for_missing_value():
    assert get_fix_feedback(ErrorType.MISSING_VALUE, "delete") == "correct"
    assert get_fix_feedback(ErrorType.MISSING_VALUE, "median") == "correct"


def test_fix_format_correct_for_wrong_format_accuracy():
    assert get_fix_feedback(ErrorType.WRONG_FORMAT_ACCURACY, "fix_format") == "correct"


def test_delete_is_suboptimal_for_wrong_format_accuracy():
    assert get_fix_feedback(ErrorType.WRONG_FORMAT_ACCURACY, "delete") == "suboptimal"


def test_false_positive_keep_is_correct():
    assert get_fix_feedback(None, "keep") == "correct"


def test_false_positive_delete_is_wrong():
    assert get_fix_feedback(None, "delete") == "wrong"


# ── compute_score ───────────────────────────────────────────────────────────────

def _make_session(*error_types: ErrorType) -> CleaningSession:
    rows = [DataRow(i + 1, 1, i + 1, -55.0, 0.9) for i in range(len(error_types))]
    gt = {i: et for i, et in enumerate(error_types)}
    return CleaningSession(rows=rows, ground_truth=gt)


def test_score_all_detected_all_correct():
    session = _make_session(ErrorType.NEGATIVE_RT, ErrorType.NEGATIVE_RT)
    d, f, total = compute_score(session, {0, 1}, {0: "delete", 1: "delete"})
    assert total == 100


def test_score_nothing_flagged_gives_zero():
    session = _make_session(ErrorType.NEGATIVE_RT)
    d, f, total = compute_score(session, set(), {})
    assert d == 0 and f == 0 and total == 0


def test_detection_is_60_for_full_detection_correct_fix():
    session = _make_session(ErrorType.NEGATIVE_RT)
    d, f, total = compute_score(session, {0}, {0: "delete"})
    assert d == 60 and f == 40 and total == 100


def test_score_half_detected():
    session = _make_session(ErrorType.NEGATIVE_RT, ErrorType.NEGATIVE_RT)
    d, f, total = compute_score(session, {0}, {0: "delete"})
    assert d == 30 and f == 40 and total == 70


# ── compute_stats ───────────────────────────────────────────────────────────────

def test_compute_stats_returns_four_keys():
    rows = [DataRow(1, 1, i + 1, 400.0 + i * 10, 0.9) for i in range(5)]
    stats = compute_stats(rows)
    assert set(stats.keys()) == {"n_rows", "mean_rt", "std_rt", "mean_accuracy"}


def test_compute_stats_excludes_none_rt():
    rows = [DataRow(1, 1, 1, None, 0.9), DataRow(1, 1, 2, 500.0, 0.9)]
    stats = compute_stats(rows)
    assert stats["mean_rt"] == pytest.approx(500.0)


def test_compute_stats_excludes_wrong_format_accuracy():
    rows = [DataRow(1, 1, 1, 400.0, 85.0), DataRow(1, 1, 2, 500.0, 0.9)]
    stats = compute_stats(rows)
    assert stats["mean_accuracy"] == pytest.approx(0.9)


# ── apply_fixes ─────────────────────────────────────────────────────────────────

def test_apply_fixes_delete_removes_row():
    session = CleaningSession(
        rows=[DataRow(1, 1, 1, -55.0, 0.9), DataRow(1, 1, 2, 400.0, 0.85)],
        ground_truth={0: ErrorType.NEGATIVE_RT},
    )
    result = apply_fixes(session, {0}, {0: "delete"})
    assert len(result) == 1
    assert result[0].trial == 2


def test_apply_fixes_keep_leaves_row():
    session = CleaningSession(
        rows=[DataRow(1, 1, 1, -55.0, 0.9)],
        ground_truth={0: ErrorType.NEGATIVE_RT},
    )
    result = apply_fixes(session, {0}, {0: "keep"})
    assert len(result) == 1
    assert result[0].rt_ms == pytest.approx(-55.0)


def test_apply_fixes_fix_format_divides_accuracy():
    session = CleaningSession(
        rows=[DataRow(1, 1, 1, 400.0, 85.0)],
        ground_truth={0: ErrorType.WRONG_FORMAT_ACCURACY},
    )
    result = apply_fixes(session, {0}, {0: "fix_format"})
    assert len(result) == 1
    assert result[0].accuracy == pytest.approx(0.85)


def test_apply_fixes_median_replaces_rt():
    session = CleaningSession(
        rows=[
            DataRow(1, 1, 1, None, 0.9),
            DataRow(1, 1, 2, 400.0, 0.9),
            DataRow(1, 1, 3, 600.0, 0.9),
        ],
        ground_truth={0: ErrorType.MISSING_VALUE},
    )
    result = apply_fixes(session, {0}, {0: "median"})
    assert len(result) == 3
    # median of clean rows [400.0, 600.0] = 500.0
    assert result[0].rt_ms == pytest.approx(500.0)

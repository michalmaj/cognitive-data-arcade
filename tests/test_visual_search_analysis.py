from __future__ import annotations

import math
import textwrap
from pathlib import Path

from matplotlib.figure import Figure

from cognitive_data_arcade.analytics.visual_search_analysis import (
    build_comparison_chart,
    load_session,
    session_stats,
)

_MINIMAL_CSV = textwrap.dedent(
    """\
    participant_id,session_id,trial_id,mode,condition,set_size,target_present,response,correct,rt_ms,timestamp
    p1,s1,1,letters,feature,8,True,present,True,320.0,2026-01-01T10:00:00
    p1,s1,2,letters,feature,8,False,absent,True,290.0,2026-01-01T10:00:01
    p1,s1,3,letters,conjunction,8,True,present,True,520.0,2026-01-01T10:00:02
    p1,s1,4,letters,conjunction,8,False,present,False,480.0,2026-01-01T10:00:03
    """
)

_EFFECT_CSV = textwrap.dedent(
    """\
    participant_id,session_id,trial_id,mode,condition,set_size,target_present,response,correct,rt_ms,timestamp
    p1,s1,1,letters,feature,8,True,present,True,300.0,2026-01-01T10:00:00
    p1,s1,2,letters,feature,8,False,absent,True,320.0,2026-01-01T10:00:01
    p1,s1,3,letters,conjunction,8,True,present,True,600.0,2026-01-01T10:00:02
    p1,s1,4,letters,conjunction,8,False,absent,True,580.0,2026-01-01T10:00:03
    """
)


def _write_csv(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "session.csv"
    p.write_text(content)
    return p


def test_load_session_shape(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path, _MINIMAL_CSV)
    df = load_session(csv_path)
    assert df.shape[0] == 4
    assert df.shape[1] >= 9


def test_session_stats_keys(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path, _MINIMAL_CSV)
    df = load_session(csv_path)
    stats = session_stats(df)
    required_keys = {
        "feature_mean_rt",
        "conjunction_mean_rt",
        "search_cost_ms",
        "feature_accuracy",
        "conjunction_accuracy",
        "overall_accuracy",
    }
    assert required_keys == set(stats.keys())


def test_search_cost_positive(tmp_path: Path) -> None:
    """search_cost_ms is positive when conjunction RT > feature RT."""
    csv_path = _write_csv(tmp_path, _EFFECT_CSV)
    df = load_session(csv_path)
    stats = session_stats(df)
    assert stats["search_cost_ms"] > 0


def test_feature_accuracy(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path, _MINIMAL_CSV)
    df = load_session(csv_path)
    stats = session_stats(df)
    assert stats["feature_accuracy"] == 1.0


def test_conjunction_accuracy_partial(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path, _MINIMAL_CSV)
    df = load_session(csv_path)
    stats = session_stats(df)
    assert stats["conjunction_accuracy"] == 0.5


def test_build_comparison_chart_returns_figure(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path, _MINIMAL_CSV)
    df = load_session(csv_path)
    fig = build_comparison_chart(df)
    assert isinstance(fig, Figure)


def test_empty_condition_yields_nan(tmp_path: Path) -> None:
    """If a condition has no data, mean RT is nan."""
    only_feature_csv = textwrap.dedent(
        """\
        participant_id,session_id,trial_id,mode,condition,set_size,target_present,response,correct,rt_ms,timestamp
        p1,s1,1,letters,feature,8,True,present,True,300.0,2026-01-01T10:00:00
        """
    )
    csv_path = _write_csv(tmp_path, only_feature_csv)
    df = load_session(csv_path)
    stats = session_stats(df)
    assert math.isnan(stats["conjunction_mean_rt"])

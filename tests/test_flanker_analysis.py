from __future__ import annotations

import textwrap
from pathlib import Path

from matplotlib.figure import Figure

from cognitive_data_arcade.analytics.flanker_analysis import (
    build_comparison_chart,
    load_session,
    session_stats,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_MINIMAL_CSV = textwrap.dedent(
    """\
    participant_id,session_id,trial_id,task_name,condition,target_direction,correct,reaction_time_ms,timestamp
    p1,s1,1,flanker,congruent,left,True,320.0,2026-01-01T10:00:00
    p1,s1,2,flanker,congruent,right,False,450.0,2026-01-01T10:00:01
    p1,s1,3,flanker,incongruent,left,True,500.0,2026-01-01T10:00:02
    p1,s1,4,flanker,incongruent,right,False,600.0,2026-01-01T10:00:03
    """
)

_EFFECT_CSV = textwrap.dedent(
    """\
    participant_id,session_id,trial_id,task_name,condition,target_direction,correct,reaction_time_ms,timestamp
    p1,s1,1,flanker,congruent,left,True,300.0,2026-01-01T10:00:00
    p1,s1,2,flanker,congruent,right,True,300.0,2026-01-01T10:00:01
    p1,s1,3,flanker,incongruent,left,True,500.0,2026-01-01T10:00:02
    p1,s1,4,flanker,incongruent,right,True,500.0,2026-01-01T10:00:03
    """
)


def _write_csv(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "session.csv"
    p.write_text(content)
    return p


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_load_session_shape(tmp_path: Path) -> None:
    """load_session returns a DataFrame with 4 rows and at least 7 columns."""
    csv_path = _write_csv(tmp_path, _MINIMAL_CSV)
    df = load_session(csv_path)
    assert df.shape[0] == 4
    assert df.shape[1] >= 7


def test_session_stats_keys(tmp_path: Path) -> None:
    """session_stats returns a dict with all 6 required keys."""
    csv_path = _write_csv(tmp_path, _MINIMAL_CSV)
    df = load_session(csv_path)
    stats = session_stats(df)
    required_keys = {
        "congruent_mean_rt",
        "incongruent_mean_rt",
        "flanker_effect_ms",
        "congruent_accuracy",
        "incongruent_accuracy",
        "overall_accuracy",
    }
    assert required_keys == set(stats.keys())


def test_flanker_effect_positive(tmp_path: Path) -> None:
    """flanker_effect_ms is positive when incongruent RT > congruent RT."""
    csv_path = _write_csv(tmp_path, _EFFECT_CSV)
    df = load_session(csv_path)
    stats = session_stats(df)
    assert stats["flanker_effect_ms"] > 0


def test_build_comparison_chart_returns_figure(tmp_path: Path) -> None:
    """build_comparison_chart returns a matplotlib Figure without displaying it."""
    csv_path = _write_csv(tmp_path, _MINIMAL_CSV)
    df = load_session(csv_path)
    fig = build_comparison_chart(df)
    assert isinstance(fig, Figure)

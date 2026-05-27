from __future__ import annotations

import textwrap
from pathlib import Path

from matplotlib.figure import Figure

from cognitive_data_arcade.analytics.gono_analysis import (
    build_stats_chart,
    load_session,
    session_stats,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_MINIMAL_CSV = textwrap.dedent(
    """\
    participant_id,session_id,trial_id,task_name,trial_type,response,correct,reaction_time_ms,timestamp
    p1,s1,1,gono,go,hit,True,280.0,2026-01-01T10:00:00+00:00
    p1,s1,2,gono,go,hit,True,310.0,2026-01-01T10:00:01+00:00
    p1,s1,3,gono,go,miss,False,0.0,2026-01-01T10:00:02+00:00
    p1,s1,4,gono,nogo,false_alarm,False,150.0,2026-01-01T10:00:03+00:00
    p1,s1,5,gono,nogo,correct_rejection,True,0.0,2026-01-01T10:00:04+00:00
    p1,s1,6,gono,nogo,correct_rejection,True,0.0,2026-01-01T10:00:05+00:00
    """
)

_PERFECT_CSV = textwrap.dedent(
    """\
    participant_id,session_id,trial_id,task_name,trial_type,response,correct,reaction_time_ms,timestamp
    p1,s1,1,gono,go,hit,True,280.0,2026-01-01T10:00:00+00:00
    p1,s1,2,gono,go,hit,True,310.0,2026-01-01T10:00:01+00:00
    p1,s1,3,gono,go,hit,True,290.0,2026-01-01T10:00:02+00:00
    p1,s1,4,gono,nogo,correct_rejection,True,0.0,2026-01-01T10:00:03+00:00
    p1,s1,5,gono,nogo,correct_rejection,True,0.0,2026-01-01T10:00:04+00:00
    p1,s1,6,gono,nogo,correct_rejection,True,0.0,2026-01-01T10:00:05+00:00
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
    """load_session returns a DataFrame with 6 rows and 9 columns."""
    csv_path = _write_csv(tmp_path, _MINIMAL_CSV)
    df = load_session(csv_path)
    assert df.shape == (6, 9)


def test_session_stats_keys(tmp_path: Path) -> None:
    """session_stats returns a dict with all 6 required keys."""
    csv_path = _write_csv(tmp_path, _MINIMAL_CSV)
    df = load_session(csv_path)
    stats = session_stats(df)
    required_keys = {
        "hit_rate",
        "false_alarm_rate",
        "miss_rate",
        "correct_rejection_rate",
        "d_prime",
        "mean_hit_rt_ms",
    }
    assert required_keys == set(stats.keys())


def test_dprime_computed_correctly(tmp_path: Path) -> None:
    """d_prime > 4.0 for perfect performance (all hits, no false alarms)."""
    csv_path = _write_csv(tmp_path, _PERFECT_CSV)
    df = load_session(csv_path)
    stats = session_stats(df)
    # hit_rate=1.0 -> clamped 0.99, fa_rate=0.0 -> clamped 0.01
    # d' = probit(0.99) - probit(0.01) ~ 2.326 - (-2.326) ~ 4.652
    assert stats["d_prime"] > 4.0


def test_build_stats_chart_returns_figure(tmp_path: Path) -> None:
    """build_stats_chart returns a matplotlib Figure without displaying it."""
    csv_path = _write_csv(tmp_path, _MINIMAL_CSV)
    df = load_session(csv_path)
    fig = build_stats_chart(df)
    assert isinstance(fig, Figure)

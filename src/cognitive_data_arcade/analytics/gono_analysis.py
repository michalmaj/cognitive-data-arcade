from __future__ import annotations

import math
from pathlib import Path

import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def _probit(p: float) -> float:
    """Rational approximation of the probit (inverse-normal CDF) function."""
    c = (2.515517, 0.802853, 0.010328)
    d = (1.432788, 0.189269, 0.001308)
    t = math.sqrt(-2.0 * math.log(p if p <= 0.5 else 1.0 - p))
    num = c[0] + c[1] * t + c[2] * t * t
    den = 1.0 + d[0] * t + d[1] * t * t + d[2] * t * t * t
    z = t - num / den
    return -z if p <= 0.5 else z


def load_session(csv_path: Path) -> pd.DataFrame:
    """Load and normalise a Go/No-Go CSV."""
    df = pd.read_csv(csv_path)
    df["correct"] = df["correct"].astype(str).str.lower().isin(["true", "1"])
    df["reaction_time_ms"] = pd.to_numeric(
        df["reaction_time_ms"], errors="coerce"
    ).fillna(0.0)
    return df


def session_stats(df: pd.DataFrame) -> dict[str, float]:
    """Signal-detection theory stats for a Go/No-Go session.

    Returns hit_rate, false_alarm_rate, miss_rate, correct_rejection_rate,
    d_prime and mean_hit_rt_ms.
    """
    go_trials = df[df["trial_type"] == "go"]
    nogo_trials = df[df["trial_type"] == "nogo"]

    n_go = len(go_trials)
    n_nogo = len(nogo_trials)

    hits = int((go_trials["response"] == "hit").sum())
    misses = int((go_trials["response"] == "miss").sum())
    false_alarms = int((nogo_trials["response"] == "false_alarm").sum())
    correct_rejections = int((nogo_trials["response"] == "correct_rejection").sum())

    hit_rate = hits / n_go if n_go > 0 else 0.0
    miss_rate = misses / n_go if n_go > 0 else 0.0
    fa_rate = false_alarms / n_nogo if n_nogo > 0 else 0.0
    cr_rate = correct_rejections / n_nogo if n_nogo > 0 else 0.0

    # Clamp to (0.01, 0.99) to avoid ±inf in probit
    hit_rate_c = max(0.01, min(0.99, hit_rate))
    fa_rate_c = max(0.01, min(0.99, fa_rate))
    d_prime = _probit(hit_rate_c) - _probit(fa_rate_c)

    hit_rows = df[df["response"] == "hit"]["reaction_time_ms"]
    mean_hit_rt = float(hit_rows.mean()) if not hit_rows.empty else float("nan")

    return {
        "hit_rate": hit_rate,
        "false_alarm_rate": fa_rate,
        "miss_rate": miss_rate,
        "correct_rejection_rate": cr_rate,
        "d_prime": d_prime,
        "mean_hit_rt_ms": mean_hit_rt,
    }


def build_stats_chart(
    df: pd.DataFrame, figsize: tuple[float, float] = (7.0, 4.5)
) -> Figure:
    """Four-bar chart: Hit / Miss / False Alarm / Correct Rejection counts."""
    labels = ["Hit", "Miss", "False Alarm", "Correct Rejection"]
    counts = [
        int((df["response"] == "hit").sum()),
        int((df["response"] == "miss").sum()),
        int((df["response"] == "false_alarm").sum()),
        int((df["response"] == "correct_rejection").sum()),
    ]
    colors = ["#27ae60", "#e74c3c", "#e67e22", "#2980b9"]

    fig = Figure(figsize=figsize)
    FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)

    fig.patch.set_facecolor("#0d0d1e")
    ax.set_facecolor("#0d0d1e")

    bars = ax.bar(labels, counts, color=colors, width=0.5)
    ax.set_ylabel("Count", color="#a0a0c0")
    ax.set_title("Go/No-Go Response Counts", color="#f0f0f0")
    ax.tick_params(colors="#a0a0c0")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a2a50")
    for bar, val in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            val + 0.05,
            str(val),
            ha="center",
            color="#f0f0f0",
            fontsize=9,
        )

    fig.tight_layout()
    return fig

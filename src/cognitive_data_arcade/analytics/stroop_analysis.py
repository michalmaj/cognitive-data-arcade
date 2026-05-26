from __future__ import annotations

import matplotlib
matplotlib.use("Agg")

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


def load_session(csv_path: Path) -> pd.DataFrame:
    """Load and normalise a Stroop CSV."""
    df = pd.read_csv(csv_path)
    df["correct"] = df["correct"].astype(str).str.lower().isin(["true", "1"])
    df["reaction_time_ms"] = pd.to_numeric(
        df["reaction_time_ms"], errors="coerce"
    ).fillna(-1.0)
    return df


def session_stats(df: pd.DataFrame) -> dict:
    """Per-condition RT stats. Timeouts (reaction_time_ms == -1) excluded from means."""
    n_trials = len(df)
    n_correct = int(df["correct"].sum())
    accuracy = n_correct / n_trials if n_trials > 0 else 0.0

    def _avg_rt(cond: str) -> float:
        subset = df.loc[
            (df["condition"] == cond) & (df["reaction_time_ms"] > 0),
            "reaction_time_ms",
        ]
        return float(subset.mean()) if not subset.empty else 0.0

    cong   = _avg_rt("congruent")
    neut   = _avg_rt("neutral")
    incong = _avg_rt("incongruent")

    return {
        "avg_rt_congruent":   cong,
        "avg_rt_neutral":     neut,
        "avg_rt_incongruent": incong,
        "facilitation_ms":    neut - cong,
        "interference_ms":    incong - neut,
        "stroop_effect_ms":   incong - cong,
        "accuracy":           accuracy,
        "n_trials":           n_trials,
        "n_correct":          n_correct,
    }


def build_stroop_chart(
    df: pd.DataFrame, figsize: tuple[float, float] = (7.0, 4.5)
) -> Figure:
    """Horizontal bar chart with 3 conditions. Background #0d0d1e (matches game UI)."""
    stats = session_stats(df)
    labels = ["Incongruent", "Neutral", "Congruent"]
    values = [
        stats["avg_rt_incongruent"],
        stats["avg_rt_neutral"],
        stats["avg_rt_congruent"],
    ]
    colors = ["#e74c3c", "#5050c0", "#27ae60"]

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("#0d0d1e")
    ax.set_facecolor("#0d0d1e")

    bars = ax.barh(labels, values, color=colors, height=0.5)
    ax.set_xlabel("Average RT (ms)", color="#a0a0c0")
    ax.tick_params(colors="#a0a0c0")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a2a50")
    for bar, val in zip(bars, values):
        if val > 0:
            ax.text(
                val + 5,
                bar.get_y() + bar.get_height() / 2,
                f"{val:.0f} ms",
                va="center",
                color="#f0f0f0",
                fontsize=9,
            )
    fig.tight_layout()
    return fig

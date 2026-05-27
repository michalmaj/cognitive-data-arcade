from __future__ import annotations

from pathlib import Path

import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def load_session(csv_path: Path) -> pd.DataFrame:
    """Load and normalise a Flanker CSV."""
    df = pd.read_csv(csv_path)
    df["correct"] = df["correct"].astype(str).str.lower().isin(["true", "1"])
    df["reaction_time_ms"] = pd.to_numeric(
        df["reaction_time_ms"], errors="coerce"
    ).fillna(-1.0)
    return df


def session_stats(df: pd.DataFrame) -> dict[str, float]:
    """Per-condition RT stats and accuracy.

    Timeouts (reaction_time_ms == -1) are excluded from RT means but count
    as incorrect for accuracy.
    """
    n_trials = len(df)

    def _mean_rt(cond: str) -> float:
        subset = df.loc[
            (df["condition"] == cond) & (df["correct"]) & (df["reaction_time_ms"] > 0),
            "reaction_time_ms",
        ]
        return float(subset.mean()) if not subset.empty else float("nan")

    def _accuracy(cond: str) -> float:
        subset = df.loc[df["condition"] == cond]
        n = len(subset)
        return float(subset["correct"].sum()) / n if n > 0 else 0.0

    cong_rt = _mean_rt("congruent")
    incong_rt = _mean_rt("incongruent")

    return {
        "congruent_mean_rt": cong_rt,
        "incongruent_mean_rt": incong_rt,
        "flanker_effect_ms": incong_rt - cong_rt,
        "congruent_accuracy": _accuracy("congruent"),
        "incongruent_accuracy": _accuracy("incongruent"),
        "overall_accuracy": float(df["correct"].sum()) / n_trials
        if n_trials > 0
        else 0.0,
    }


def build_comparison_chart(
    df: pd.DataFrame, figsize: tuple[float, float] = (7.0, 4.5)
) -> Figure:
    """Two-bar chart: congruent vs incongruent mean RT for correct trials."""
    stats = session_stats(df)
    labels = ["Congruent", "Incongruent"]
    values = [stats["congruent_mean_rt"], stats["incongruent_mean_rt"]]
    colors = ["#27ae60", "#e74c3c"]

    fig = Figure(figsize=figsize)
    FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)

    fig.patch.set_facecolor("#0d0d1e")
    ax.set_facecolor("#0d0d1e")

    bars = ax.bar(labels, values, color=colors, width=0.5)
    ax.set_ylabel("Mean RT (ms)", color="#a0a0c0")
    ax.set_title("Flanker Effect", color="#f0f0f0")
    ax.tick_params(colors="#a0a0c0")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a2a50")
    for bar, val in zip(bars, values):
        if val > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                val + 5,
                f"{val:.0f} ms",
                ha="center",
                color="#f0f0f0",
                fontsize=9,
            )

    fig.tight_layout()
    return fig

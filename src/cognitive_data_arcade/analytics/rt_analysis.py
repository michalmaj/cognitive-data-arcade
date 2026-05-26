from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


def load_session(csv_path: Path) -> pd.DataFrame:
    """Load a single-session RT CSV. Normalises correct and reaction_time_ms columns."""
    df = pd.read_csv(csv_path)
    df["correct"] = df["correct"].astype(str).str.lower().isin(["true", "1"])
    df["reaction_time_ms"] = pd.to_numeric(
        df["reaction_time_ms"], errors="coerce"
    ).fillna(-1.0)
    return df


def session_stats(df: pd.DataFrame) -> dict:
    """Compute summary stats; timeouts (reaction_time_ms == -1) excluded from RT stats."""
    valid = df.loc[df["reaction_time_ms"] > 0, "reaction_time_ms"]
    n_trials = len(df)
    n_correct = int(df["correct"].sum())
    if valid.empty:
        return {
            "avg_rt": 0.0,
            "median_rt": 0.0,
            "min_rt": 0.0,
            "max_rt": 0.0,
            "accuracy": 0.0,
            "n_trials": n_trials,
            "n_correct": n_correct,
        }
    return {
        "avg_rt": float(valid.mean()),
        "median_rt": float(valid.median()),
        "min_rt": float(valid.min()),
        "max_rt": float(valid.max()),
        "accuracy": n_correct / n_trials if n_trials > 0 else 0.0,
        "n_trials": n_trials,
        "n_correct": n_correct,
    }


def build_histogram(
    df: pd.DataFrame,
    figsize: tuple[float, float] = (7.0, 4.5),
) -> Figure:
    """RT distribution histogram for correct trials. Dark theme matching game UI."""
    valid_rts = df.loc[df["reaction_time_ms"] > 0, "reaction_time_ms"]

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("#0d0d1e")
    ax.set_facecolor("#0d0d1e")

    if not valid_rts.empty:
        ax.hist(valid_rts, bins=10, color="#f3a020", edgecolor="#0d0d1e", alpha=0.85)
        ax.axvline(
            valid_rts.median(),
            color="white",
            linestyle="--",
            linewidth=1.5,
            alpha=0.7,
        )

    ax.set_xlabel("Reaction time (ms)", color="#a0a0c0")
    ax.set_ylabel("Count", color="#a0a0c0")
    ax.tick_params(colors="#a0a0c0")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a2a50")

    fig.tight_layout()
    return fig

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.ticker as mticker
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def _probit(p: float) -> float:
    c = (2.515517, 0.802853, 0.010328)
    d = (1.432788, 0.189269, 0.001308)
    t = math.sqrt(-2.0 * math.log(p if p <= 0.5 else 1.0 - p))
    num = c[0] + c[1] * t + c[2] * t * t
    den = 1.0 + d[0] * t + d[1] * t * t + d[2] * t * t * t
    z = t - num / den
    return -z if p <= 0.5 else z


def load_session(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    for col in (
        "pos_match", "let_match", "key_a_pressed", "key_l_pressed",
        "pos_correct", "let_correct",
    ):
        df[col] = df[col].astype(str).str.lower().isin(["true", "1"])
    for col in ("rt_a_ms", "rt_l_ms"):
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    df["n_level"] = pd.to_numeric(df["n_level"], errors="coerce").fillna(1).astype(int)
    return df


def session_stats(df: pd.DataFrame) -> dict[str, float]:
    n = len(df)
    pos_acc = float(df["pos_correct"].sum() / n) if n > 0 else 0.0
    let_acc = float(df["let_correct"].sum() / n) if n > 0 else 0.0

    pos_t = df[df["pos_match"]]
    pos_nt = df[~df["pos_match"]]
    let_t = df[df["let_match"]]
    let_nt = df[~df["let_match"]]

    def _safe_rate(subset: pd.DataFrame, col: str) -> float:
        return float(subset[col].sum() / len(subset)) if len(subset) > 0 else 0.5

    pos_hr = max(0.01, min(0.99, _safe_rate(pos_t, "key_a_pressed")))
    pos_far = max(0.01, min(0.99, _safe_rate(pos_nt, "key_a_pressed")))
    let_hr = max(0.01, min(0.99, _safe_rate(let_t, "key_l_pressed")))
    let_far = max(0.01, min(0.99, _safe_rate(let_nt, "key_l_pressed")))

    return {
        "pos_accuracy": pos_acc,
        "let_accuracy": let_acc,
        "pos_dprime": _probit(pos_hr) - _probit(pos_far),
        "let_dprime": _probit(let_hr) - _probit(let_far),
        "mean_n_level": float(df["n_level"].mean()) if n > 0 else 1.0,
        "final_n_level": float(df["n_level"].iloc[-1]) if n > 0 else 1.0,
        "total_trials": float(n),
    }


def build_chart(df: pd.DataFrame, figsize: tuple[float, float] = (7.0, 4.5)) -> Figure:
    stats = session_stats(df)
    n_by_block = df.groupby("block_id")["n_level"].first()
    n_varies = n_by_block.nunique() > 1

    fig = Figure(figsize=figsize)
    FigureCanvasAgg(fig)

    ax1 = fig.add_subplot(121 if n_varies else 111)
    fig.patch.set_facecolor("#0d0d1e")
    ax1.set_facecolor("#0d0d1e")

    labels = ["Pos Acc", "Let Acc", "Pos d'", "Let d'"]
    values = [
        stats["pos_accuracy"],
        stats["let_accuracy"],
        stats["pos_dprime"],
        stats["let_dprime"],
    ]
    colors = ["#27ae60", "#2980b9", "#e67e22", "#9b59b6"]
    bars = ax1.bar(labels, values, color=colors, width=0.5)
    ax1.set_title("N-Back Performance", color="#f0f0f0")
    ax1.tick_params(colors="#a0a0c0")
    for spine in ax1.spines.values():
        spine.set_edgecolor("#2a2a50")
    for bar, val in zip(bars, values):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            val + 0.02,
            f"{val:.2f}",
            ha="center",
            color="#f0f0f0",
            fontsize=8,
        )

    if n_varies:
        ax2 = fig.add_subplot(122)
        ax2.set_facecolor("#0d0d1e")
        ax2.plot(n_by_block.index.tolist(), n_by_block.values.tolist(),
                 color="#f39c12", marker="o")
        ax2.set_xlabel("Block", color="#a0a0c0")
        ax2.set_ylabel("N Level", color="#a0a0c0")
        ax2.set_title("N Progression", color="#f0f0f0")
        ax2.tick_params(colors="#a0a0c0")
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        for spine in ax2.spines.values():
            spine.set_edgecolor("#2a2a50")

    fig.tight_layout()
    return fig

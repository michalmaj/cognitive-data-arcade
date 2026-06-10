from __future__ import annotations

import random

import numpy as np

from cognitive_data_arcade.games.cognitive_dashboard.session import DashboardSession, TaskResult

MINI_TRIALS: int = 8
FIXATION_MS: int = 500
FEEDBACK_MS: int = 400
TIMEOUT_MS: int = 3000

# "gonogo"."nogo" only has "fa_rate" (a probability) — no RT distribution,
# because correct rejections are non-responses rather than timed keypresses.
SYNTHETIC_PARAMS: dict[str, dict[str, dict[str, float]]] = {
    "rt": {
        "simple": {"mean": 320.0, "sd": 60.0, "lo": 150.0, "hi": 800.0},
    },
    "stroop": {
        "congruent":   {"mean": 310.0, "sd": 40.0, "lo": 200.0, "hi": 700.0},
        "incongruent": {"mean": 378.0, "sd": 60.0, "lo": 200.0, "hi": 800.0},
    },
    "flanker": {
        "congruent":   {"mean": 322.0, "sd": 40.0, "lo": 200.0, "hi": 650.0},
        "incongruent": {"mean": 364.0, "sd": 55.0, "lo": 200.0, "hi": 700.0},
    },
    "gonogo": {
        "go":   {"mean": 330.0, "sd": 50.0, "lo": 180.0, "hi": 700.0},
        "nogo": {"fa_rate": 0.15},
    },
}


def _sample_rts(params: dict[str, float], n: int, rng: np.random.Generator) -> list[float]:
    raw = rng.normal(params["mean"], params["sd"], n)
    return [float(np.clip(x, params["lo"], params["hi"])) for x in raw]


def generate_synthetic(n_trials: int = MINI_TRIALS) -> DashboardSession:
    rng = np.random.default_rng()
    half = n_trials // 2

    # RT — all simple condition, all correct
    rt_rts = _sample_rts(SYNTHETIC_PARAMS["rt"]["simple"], n_trials, rng)
    rt_result = TaskResult(
        rt_ms=rt_rts,
        correct=[True] * n_trials,
        condition=["simple"] * n_trials,
    )

    # Stroop — 4 congruent + 4 incongruent, shuffled
    s_rts = (
        _sample_rts(SYNTHETIC_PARAMS["stroop"]["congruent"], half, rng)
        + _sample_rts(SYNTHETIC_PARAMS["stroop"]["incongruent"], half, rng)
    )
    s_conds = ["congruent"] * half + ["incongruent"] * half
    idx = list(range(n_trials))
    random.shuffle(idx)
    stroop_result = TaskResult(
        rt_ms=[s_rts[i] for i in idx],
        correct=[True] * n_trials,
        condition=[s_conds[i] for i in idx],
    )

    # Flanker — 4 congruent + 4 incongruent, shuffled
    f_rts = (
        _sample_rts(SYNTHETIC_PARAMS["flanker"]["congruent"], half, rng)
        + _sample_rts(SYNTHETIC_PARAMS["flanker"]["incongruent"], half, rng)
    )
    f_conds = ["congruent"] * half + ["incongruent"] * half
    idx2 = list(range(n_trials))
    random.shuffle(idx2)
    flanker_result = TaskResult(
        rt_ms=[f_rts[i] for i in idx2],
        correct=[True] * n_trials,
        condition=[f_conds[i] for i in idx2],
    )

    # Go/No-Go — (n_trials-2) go + 2 nogo
    n_go = n_trials - 2
    n_nogo = 2
    go_rts = _sample_rts(SYNTHETIC_PARAMS["gonogo"]["go"], n_go, rng)
    fa_rate = SYNTHETIC_PARAMS["gonogo"]["nogo"]["fa_rate"]
    nogo_correct = [bool(rng.random() >= fa_rate) for _ in range(n_nogo)]
    nogo_rts = [
        float(np.clip(rng.normal(250, 50), 100, 500)) if not c else -1.0
        for c in nogo_correct
    ]
    gng_rts = go_rts + nogo_rts
    gng_correct = [True] * n_go + nogo_correct
    gng_conds = ["go"] * n_go + ["nogo"] * n_nogo
    idx3 = list(range(n_trials))
    random.shuffle(idx3)
    gonogo_result = TaskResult(
        rt_ms=[gng_rts[i] for i in idx3],
        correct=[gng_correct[i] for i in idx3],
        condition=[gng_conds[i] for i in idx3],
    )

    return DashboardSession(
        rt=rt_result,
        stroop=stroop_result,
        flanker=flanker_result,
        gonogo=gonogo_result,
        synthetic=True,
    )

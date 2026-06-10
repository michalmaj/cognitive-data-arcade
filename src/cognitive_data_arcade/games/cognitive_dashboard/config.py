from __future__ import annotations

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

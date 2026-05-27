from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FlankerConfig:
    num_trials: int = 48
    trials_per_block: int = 24
    iti_min_ms: int = 800
    iti_max_ms: int = 1500
    fixation_duration_ms: int = 500
    stimulus_duration_ms: int = 2000
    feedback_duration_ms: int = 600
    ap_per_correct: int = 2
    sp_flanker_effect_bonus: int = 10
    fast_rt_threshold_ms: float = 400.0


QUICK = FlankerConfig(num_trials=24, trials_per_block=12)
STANDARD = FlankerConfig(num_trials=48, trials_per_block=24)
FULL = FlankerConfig(num_trials=96, trials_per_block=48)

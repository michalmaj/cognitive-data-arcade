from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GoNoGoConfig:
    num_trials: int = 80
    trials_per_block: int = 40
    go_ratio: float = 0.75
    iti_min_ms: int = 800
    iti_max_ms: int = 1500
    fixation_duration_ms: int = 500
    stimulus_duration_ms: int = 1000
    feedback_duration_ms: int = 600
    ap_per_hit: int = 3
    sp_dprime_bonus: int = 15
    dprime_threshold: float = 2.0


QUICK = GoNoGoConfig(num_trials=40, trials_per_block=20, go_ratio=0.75)
STANDARD = GoNoGoConfig(num_trials=80, trials_per_block=40, go_ratio=0.75)
FULL = GoNoGoConfig(num_trials=120, trials_per_block=60, go_ratio=0.75)

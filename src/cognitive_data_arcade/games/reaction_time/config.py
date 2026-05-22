from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReactionTimeConfig:
    num_trials: int = 24
    trials_per_block: int = 12
    iti_min_ms: int = 1500
    iti_max_ms: int = 4000
    fixation_duration_ms: int = 500
    feedback_duration_ms: int = 600
    distractor_count: int = 3
    ap_per_correct: int = 3
    ap_bonus_fast: int = 20
    ap_bonus_accurate: int = 10
    fast_rt_threshold_ms: float = 300.0
    accuracy_bonus_threshold: float = 0.90


DEFAULT_CONFIG = ReactionTimeConfig()

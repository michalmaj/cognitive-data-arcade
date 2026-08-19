from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProfileData:
    rt_median_ms: float
    stroop_effect_ms: float
    flanker_effect_ms: float
    gono_false_alarm_rate: float
    nback_max_level: int
    rt_percentile: int
    is_synthetic: bool = False


@dataclass
class GameState:
    profile: ProfileData | None = None
    current_card: int = 0

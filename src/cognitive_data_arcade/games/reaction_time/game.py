from __future__ import annotations

from cognitive_data_arcade.games.reaction_time.config import ReactionTimeConfig


def _compute_ap(config: ReactionTimeConfig, correct_trials: int, avg_rt: float) -> int:
    """Return Arcade Points earned from a session. Pure function — no side effects."""
    ap = correct_trials * config.ap_per_correct
    if avg_rt > 0 and avg_rt < config.fast_rt_threshold_ms:
        ap += config.ap_bonus_fast
    if (
        config.num_trials > 0
        and correct_trials / config.num_trials >= config.accuracy_bonus_threshold
    ):
        ap += config.ap_bonus_accurate
    return ap

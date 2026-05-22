from cognitive_data_arcade.games.reaction_time.config import ReactionTimeConfig
from cognitive_data_arcade.games.reaction_time.game import _compute_ap


def test_compute_ap_base_only() -> None:
    config = ReactionTimeConfig(
        num_trials=10,
        ap_per_correct=3,
        ap_bonus_fast=20,
        ap_bonus_accurate=10,
        fast_rt_threshold_ms=300.0,
        accuracy_bonus_threshold=0.90,
    )
    # 5/10 correct, slow RT — only base AP
    assert _compute_ap(config, correct_trials=5, avg_rt=500.0) == 15


def test_compute_ap_speed_bonus() -> None:
    config = ReactionTimeConfig(
        num_trials=10,
        ap_per_correct=3,
        ap_bonus_fast=20,
        ap_bonus_accurate=10,
        fast_rt_threshold_ms=300.0,
        accuracy_bonus_threshold=0.90,
    )
    # 5/10 correct (below accuracy threshold), fast RT
    assert _compute_ap(config, correct_trials=5, avg_rt=250.0) == 15 + 20


def test_compute_ap_all_bonuses() -> None:
    config = ReactionTimeConfig(
        num_trials=10,
        ap_per_correct=3,
        ap_bonus_fast=20,
        ap_bonus_accurate=10,
        fast_rt_threshold_ms=300.0,
        accuracy_bonus_threshold=0.90,
    )
    # 10/10 correct (100% >= 90%), fast RT (250 < 300)
    assert _compute_ap(config, correct_trials=10, avg_rt=250.0) == 30 + 20 + 10


def test_compute_ap_zero_avg_rt_no_speed_bonus() -> None:
    config = ReactionTimeConfig(
        num_trials=10,
        ap_per_correct=3,
        ap_bonus_fast=20,
        ap_bonus_accurate=10,
        fast_rt_threshold_ms=300.0,
        accuracy_bonus_threshold=0.90,
    )
    # avg_rt=0.0 means all trials timed out — no speed bonus
    assert _compute_ap(config, correct_trials=0, avg_rt=0.0) == 0

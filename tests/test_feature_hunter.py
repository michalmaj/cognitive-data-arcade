from __future__ import annotations


def test_difficulty_configs_card_counts():
    from cognitive_data_arcade.games.feature_hunter.config import EASY, MEDIUM, HARD
    assert EASY.card_count == 4
    assert MEDIUM.card_count == 6
    assert HARD.card_count == 8


def test_difficulty_configs_timers():
    from cognitive_data_arcade.games.feature_hunter.config import EASY, MEDIUM, HARD
    assert EASY.timer_s is None
    assert MEDIUM.timer_s == 45.0
    assert HARD.timer_s == 20.0


def test_difficulty_configs_hints():
    from cognitive_data_arcade.games.feature_hunter.config import EASY, MEDIUM, HARD
    assert EASY.hints == "full"
    assert MEDIUM.hints == "scatter_only"
    assert HARD.hints == "none"


def test_feature_bank_has_60_entries():
    from cognitive_data_arcade.games.feature_hunter.features import FEATURE_BANK
    assert len(FEATURE_BANK) >= 60


def test_feature_is_signal_threshold():
    from cognitive_data_arcade.games.feature_hunter.features import Feature
    strong = Feature("X", "x", "temporal", 0.75, 0.3, "X", "Y")
    noise = Feature("Y", "y", "noise", 0.05, 0.55, "X", "Y")
    assert strong.is_signal is True
    assert noise.is_signal is False


def test_feature_bank_has_all_categories():
    from cognitive_data_arcade.games.feature_hunter.features import FEATURE_BANK
    cats = {f.category for f in FEATURE_BANK}
    for expected in ("temporal", "demographic", "physiological", "environmental", "task_history", "noise"):
        assert expected in cats, f"Missing category: {expected}"


def test_easy_difficulty_can_draw_4_features():
    from cognitive_data_arcade.games.feature_hunter.features import draw_features
    from cognitive_data_arcade.games.feature_hunter.config import EASY
    features = draw_features(EASY, session_seed=0, round_idx=0)
    assert len(features) == 4


def test_hard_difficulty_can_draw_8_features():
    from cognitive_data_arcade.games.feature_hunter.features import draw_features
    from cognitive_data_arcade.games.feature_hunter.config import HARD
    features = draw_features(HARD, session_seed=7, round_idx=3)
    assert len(features) == 8


def test_draw_features_always_includes_noise():
    from cognitive_data_arcade.games.feature_hunter.features import draw_features
    from cognitive_data_arcade.games.feature_hunter.config import EASY
    for seed in range(10):
        features = draw_features(EASY, session_seed=seed, round_idx=0)
        noise_count = sum(1 for f in features if not f.is_signal)
        assert noise_count >= 1, f"seed={seed}: no noise feature in round"

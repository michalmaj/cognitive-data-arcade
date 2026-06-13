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

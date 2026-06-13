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


def test_simulate_scatter_shape():
    from cognitive_data_arcade.games.feature_hunter.features import FEATURE_BANK
    from cognitive_data_arcade.games.feature_hunter.simulator import simulate_scatter
    x, y = simulate_scatter(FEATURE_BANK[0], n_points=60, seed=1)
    assert len(x) == 60
    assert len(y) == 60


def test_simulate_scatter_normalised():
    from cognitive_data_arcade.games.feature_hunter.features import FEATURE_BANK
    from cognitive_data_arcade.games.feature_hunter.simulator import simulate_scatter
    import numpy as np
    x, y = simulate_scatter(FEATURE_BANK[0], n_points=60, seed=2)
    assert float(np.min(x)) >= 0.0 - 1e-6
    assert float(np.max(x)) <= 1.0 + 1e-6
    assert float(np.min(y)) >= 0.0 - 1e-6
    assert float(np.max(y)) <= 1.0 + 1e-6


def test_simulate_scatter_deterministic():
    from cognitive_data_arcade.games.feature_hunter.features import FEATURE_BANK
    from cognitive_data_arcade.games.feature_hunter.simulator import simulate_scatter
    import numpy as np
    x1, y1 = simulate_scatter(FEATURE_BANK[1], n_points=40, seed=99)
    x2, y2 = simulate_scatter(FEATURE_BANK[1], n_points=40, seed=99)
    np.testing.assert_array_equal(x1, x2)


def test_compute_accuracy_delta_signal_beats_noise():
    from cognitive_data_arcade.games.feature_hunter.features import FEATURE_BANK
    from cognitive_data_arcade.games.feature_hunter.simulator import compute_accuracy_delta
    signal_feat = next(f for f in FEATURE_BANK if abs(f.correlation) > 0.6)
    noise_feat = next(f for f in FEATURE_BANK if abs(f.correlation) < 0.05)
    acc_with_s, acc_without_s = compute_accuracy_delta(signal_feat, seed=0)
    acc_with_n, acc_without_n = compute_accuracy_delta(noise_feat, seed=0)
    assert acc_with_s > acc_without_s
    assert acc_with_n <= acc_without_n + 0.05  # noise barely helps


def test_render_card_returns_correct_size():
    import pygame
    pygame.init()
    pygame.display.set_mode((1, 1))
    from cognitive_data_arcade.games.feature_hunter.features import FEATURE_BANK
    from cognitive_data_arcade.games.feature_hunter.widgets import render_card
    surf = render_card(FEATURE_BANK[0], card_w=200, card_h=240, seed=0)
    assert isinstance(surf, pygame.Surface)
    assert surf.get_width() == 200
    assert surf.get_height() == 240
    pygame.quit()


def test_grid_layout_all_difficulties():
    from cognitive_data_arcade.games.feature_hunter.widgets import grid_layout
    assert grid_layout(4) == (2, 2)
    assert grid_layout(6) == (3, 2)
    assert grid_layout(8) == (4, 2)


def test_round_score_perfect_easy():
    from cognitive_data_arcade.games.feature_hunter.phase_b import compute_round_score
    from cognitive_data_arcade.games.feature_hunter.config import EASY
    score = compute_round_score(correct=4, total=4, timer_remaining=0.0, difficulty=EASY)
    assert score == 4 * 10 + 20  # 60


def test_round_score_hard_with_time_bonus():
    from cognitive_data_arcade.games.feature_hunter.phase_b import compute_round_score
    from cognitive_data_arcade.games.feature_hunter.config import HARD
    # 8 correct, 15s remaining → 80 + 20 + (15//5)*2 = 106
    score = compute_round_score(correct=8, total=8, timer_remaining=15.0, difficulty=HARD)
    assert score == 80 + 20 + 6  # 106


def test_round_score_partial():
    from cognitive_data_arcade.games.feature_hunter.phase_b import compute_round_score
    from cognitive_data_arcade.games.feature_hunter.config import MEDIUM
    # 4/6 correct, no time bonus (timer_remaining counts but no perfect bonus)
    score = compute_round_score(correct=4, total=6, timer_remaining=20.0, difficulty=MEDIUM)
    # 4*10 + 0 (no perfect) + (20//5)*1 = 40 + 4 = 44
    assert score == 44


def test_get_game_info_pl():
    import pygame
    pygame.init()
    pygame.display.set_mode((1, 1))
    from cognitive_data_arcade.engine.i18n import get_strings
    from cognitive_data_arcade.engine.pause import GameInfo
    from cognitive_data_arcade.games.feature_hunter.info import get_game_info
    strings = get_strings("pl")
    info = get_game_info(strings)
    assert isinstance(info, GameInfo)
    assert info.title == "Feature Hunter"
    assert len(info.description_lines) >= 2
    pygame.quit()


def test_lesson_17_content():
    from cognitive_data_arcade.lessons.lesson_17 import CONTENT
    for lang in ("pl", "en"):
        assert lang in CONTENT
        for key in ("theory", "notes", "tasks"):
            assert key in CONTENT[lang]
            assert len(CONTENT[lang][key]) >= 2


def test_lesson_17_in_menu():
    from cognitive_data_arcade.ui.menu import _LESSONS
    nums = [num for num, _ in _LESSONS]
    assert 17 in nums, "Lesson 17 must be in _LESSONS"


def test_lesson_17_name_in_menu():
    from cognitive_data_arcade.ui.menu import _LESSONS
    name = next((n for num, n in _LESSONS if num == 17), None)
    assert name == "Feature Hunter"


def test_game_factory_for_17_returns_callable(tmp_path):
    import pygame
    pygame.init()
    pygame.display.set_mode((1024, 720))
    from cognitive_data_arcade.engine.i18n import get_strings
    from cognitive_data_arcade.profile.manager import ProfileManager
    from cognitive_data_arcade.ui.menu import LessonMenuScene
    strings = get_strings("pl")
    pm = ProfileManager(tmp_path / "profile.json")
    scene = LessonMenuScene(pm, strings)
    factory = scene._game_factory_for(17)
    assert callable(factory), "_game_factory_for(17) must return a callable"
    pygame.quit()


def test_feature_hunter_scene_smoke(tmp_path):
    import pygame
    pygame.init()
    pygame.display.set_mode((1024, 720))
    from cognitive_data_arcade.games.feature_hunter.game import FeatHunterScene
    s = FeatHunterScene()
    surf = pygame.Surface((1024, 720))
    s.draw(surf)
    assert not s.is_done()
    pygame.quit()

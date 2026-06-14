from __future__ import annotations
import numpy as np


def test_scenarios_count():
    from cognitive_data_arcade.games.overfitting_monster.scenarios import SCENARIOS
    assert len(SCENARIOS) == 5


def test_generate_data_shape():
    from cognitive_data_arcade.games.overfitting_monster.scenarios import SCENARIOS, generate_data
    for s in SCENARIOS:
        X, y = generate_data(s, seed=42)
        assert X.shape == (s.n_points, 2), f"{s.name_pl}: shape mismatch"
        assert y.shape == (s.n_points,)


def test_generate_data_normalised():
    from cognitive_data_arcade.games.overfitting_monster.scenarios import SCENARIOS, generate_data
    for s in SCENARIOS:
        X, _ = generate_data(s, seed=0)
        assert float(X.min()) >= -1e-6
        assert float(X.max()) <= 1.0 + 1e-6


def test_generate_data_two_classes():
    from cognitive_data_arcade.games.overfitting_monster.scenarios import SCENARIOS, generate_data
    for s in SCENARIOS:
        _, y = generate_data(s, seed=7)
        assert 0 in y and 1 in y, f"{s.name_pl}: both classes must be present"


def test_generate_data_deterministic():
    from cognitive_data_arcade.games.overfitting_monster.scenarios import SCENARIOS, generate_data
    X1, y1 = generate_data(SCENARIOS[0], seed=99)
    X2, y2 = generate_data(SCENARIOS[0], seed=99)
    np.testing.assert_array_equal(X1, X2)


def test_split_data_sizes():
    from cognitive_data_arcade.games.overfitting_monster.classifier import split_data
    X = np.random.default_rng(0).random((80, 2))
    y = np.array([0] * 40 + [1] * 40, dtype=np.int32)
    X_tr, y_tr, X_te, y_te = split_data(X, y, split_pct=70, seed=1)
    assert len(X_tr) + len(X_te) == 80
    assert abs(len(X_tr) - 56) <= 1   # 70% of 80 = 56


def test_split_data_deterministic():
    from cognitive_data_arcade.games.overfitting_monster.classifier import split_data
    X = np.random.default_rng(0).random((60, 2))
    y = np.zeros(60, dtype=np.int32)
    r1 = split_data(X, y, split_pct=70, seed=5)
    r2 = split_data(X, y, split_pct=70, seed=5)
    np.testing.assert_array_equal(r1[0], r2[0])


def test_knn_accuracies_keys():
    from cognitive_data_arcade.games.overfitting_monster.classifier import knn_accuracies
    X_tr = np.array([[0.1, 0.1], [0.2, 0.2], [0.8, 0.8], [0.9, 0.9]])
    y_tr = np.array([0, 0, 1, 1], dtype=np.int32)
    X_te = np.array([[0.15, 0.15], [0.85, 0.85]])
    y_te = np.array([0, 1], dtype=np.int32)
    result = knn_accuracies(X_tr, y_tr, X_te, y_te, k=1)
    assert set(result.keys()) == {"train", "test"}
    assert 0.0 <= result["train"] <= 1.0
    assert 0.0 <= result["test"] <= 1.0


def test_knn_k1_train_perfect():
    from cognitive_data_arcade.games.overfitting_monster.classifier import knn_accuracies
    # k=1: each point is its own nearest neighbour -> always 100% train accuracy
    X_tr = np.array([[0.1, 0.1], [0.5, 0.5], [0.9, 0.9]])
    y_tr = np.array([0, 0, 1], dtype=np.int32)
    X_te = np.array([[0.2, 0.2]])
    y_te = np.array([0], dtype=np.int32)
    result = knn_accuracies(X_tr, y_tr, X_te, y_te, k=1)
    assert result["train"] == 1.0


def test_compute_gap_stars():
    from cognitive_data_arcade.games.overfitting_monster.classifier import compute_gap_stars
    assert compute_gap_stars(0.90, 0.88) == 3   # gap = 2 pp
    assert compute_gap_stars(0.90, 0.80) == 2   # gap = 10 pp
    assert compute_gap_stars(0.95, 0.70) == 1   # gap = 25 pp


def test_compute_round_score():
    from cognitive_data_arcade.games.overfitting_monster.classifier import compute_round_score
    assert compute_round_score(0.85, stars=3) == 85 + 20   # 105
    assert compute_round_score(0.85, stars=2) == 85 + 10   # 95
    assert compute_round_score(0.85, stars=1) == 85 + 0    # 85


def test_slider_initial_value():
    # SliderWidget must not import pygame at module level — import inside function
    import os; os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame; pygame.init()
    from cognitive_data_arcade.games.overfitting_monster.widgets import SliderWidget
    rect = pygame.Rect(100, 100, 200, 20)
    s = SliderWidget(rect, min_val=1, max_val=15, value=7)
    assert s.value == 7


def test_slider_clamping():
    import os; os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame; pygame.init()
    from cognitive_data_arcade.games.overfitting_monster.widgets import SliderWidget
    rect = pygame.Rect(0, 0, 300, 20)
    s = SliderWidget(rect, min_val=50, max_val=80, value=70)
    # Simulate click far to the right (should clamp to max)
    ev = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(500, 10))
    s.handle_event(ev)
    assert s.value == 80
    # Simulate click far to the left (should clamp to min)
    ev = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(-100, 10))
    s.handle_event(ev)
    assert s.value == 50


def test_overfitting_monster_scene_instantiates():
    import os; os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame; pygame.init()
    from cognitive_data_arcade.games.overfitting_monster.game import OverfittingMonsterScene
    scene = OverfittingMonsterScene()
    assert not scene.is_done()
    assert scene.next_scene() is None

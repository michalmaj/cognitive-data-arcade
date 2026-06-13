from __future__ import annotations


def test_scenarios_count():
    from cognitive_data_arcade.games.classifier_battle.scenarios import SCENARIOS
    assert len(SCENARIOS) == 5


def test_generate_data_shape():
    from cognitive_data_arcade.games.classifier_battle.scenarios import SCENARIOS, generate_data
    s = SCENARIOS[0]
    X, y = generate_data(s, seed=42)
    assert X.shape == (s.n_points, 2)
    assert y.shape == (s.n_points,)


def test_generate_data_normalised():
    from cognitive_data_arcade.games.classifier_battle.scenarios import SCENARIOS, generate_data
    import numpy as np
    for s in SCENARIOS:
        X, y = generate_data(s, seed=0)
        assert float(X.min()) >= -1e-6
        assert float(X.max()) <= 1.0 + 1e-6


def test_generate_data_deterministic():
    from cognitive_data_arcade.games.classifier_battle.scenarios import SCENARIOS, generate_data
    import numpy as np
    X1, y1 = generate_data(SCENARIOS[2], seed=99)
    X2, y2 = generate_data(SCENARIOS[2], seed=99)
    np.testing.assert_array_equal(X1, X2)


def test_generate_data_two_classes():
    from cognitive_data_arcade.games.classifier_battle.scenarios import SCENARIOS, generate_data
    import numpy as np
    for s in SCENARIOS:
        _, y = generate_data(s, seed=7)
        assert 0 in y and 1 in y, f"{s.name_pl}: both classes must be present"


def test_player_accuracy_range():
    from cognitive_data_arcade.games.classifier_battle.scenarios import SCENARIOS, generate_data
    from cognitive_data_arcade.games.classifier_battle.classifier import player_accuracy
    X, y = generate_data(SCENARIOS[0], seed=1)
    # vertical line at x=0.5 in normalised space, spanning full height
    polyline = [(0.5, 0.0), (0.5, 1.0)]
    acc = player_accuracy(polyline, X, y)
    assert 0.0 <= acc <= 1.0


def test_player_accuracy_perfect_blobs():
    from cognitive_data_arcade.games.classifier_battle.scenarios import SCENARIOS, generate_data
    from cognitive_data_arcade.games.classifier_battle.classifier import player_accuracy
    import numpy as np
    # blobs: class 0 centred at (0.25, 0.5), class 1 at (0.75, 0.5)
    # a vertical line at x=0.5 should separate them well
    X, y = generate_data(SCENARIOS[0], seed=42)
    polyline = [(0.5, 0.0), (0.5, 1.0)]
    acc = player_accuracy(polyline, X, y)
    assert acc >= 0.80, f"Expected >= 0.80 for clean blobs, got {acc:.2f}"


def test_classifier_accuracies_keys():
    from cognitive_data_arcade.games.classifier_battle.scenarios import SCENARIOS, generate_data
    from cognitive_data_arcade.games.classifier_battle.classifier import classifier_accuracies
    X, y = generate_data(SCENARIOS[0], seed=0)
    accs = classifier_accuracies(X, y, seed=0)
    assert set(accs.keys()) == {"liniowy", "knn", "drzewo"}


def test_classifier_accuracies_range():
    from cognitive_data_arcade.games.classifier_battle.scenarios import SCENARIOS, generate_data
    from cognitive_data_arcade.games.classifier_battle.classifier import classifier_accuracies
    X, y = generate_data(SCENARIOS[0], seed=0)
    accs = classifier_accuracies(X, y, seed=0)
    for name, acc in accs.items():
        assert 0.0 <= acc <= 1.0, f"{name}: {acc}"


def test_compute_round_score_no_bonus():
    from cognitive_data_arcade.games.classifier_battle.classifier import compute_round_score
    # player at 60%, classifiers all at 80% -> no bonus
    accs = {"liniowy": 0.80, "knn": 0.80, "drzewo": 0.80}
    score = compute_round_score(0.60, accs)
    assert score == 60


def test_compute_round_score_beat_linear():
    from cognitive_data_arcade.games.classifier_battle.classifier import compute_round_score
    # player at 85%, linear at 75%, knn at 90%
    accs = {"liniowy": 0.75, "knn": 0.90, "drzewo": 0.80}
    score = compute_round_score(0.85, accs)
    assert score == 85 + 15  # beat linear only


def test_compute_round_score_beat_knn():
    from cognitive_data_arcade.games.classifier_battle.classifier import compute_round_score
    # player at 95%, all classifiers at 80%
    accs = {"liniowy": 0.80, "knn": 0.80, "drzewo": 0.80}
    score = compute_round_score(0.95, accs)
    assert score == 95 + 15 + 20  # beat both


def test_draw_canvas_smoke():
    import pygame
    pygame.init()
    pygame.display.set_mode((1, 1))
    from cognitive_data_arcade.games.classifier_battle.widgets import DrawCanvas
    from cognitive_data_arcade.games.classifier_battle.scenarios import SCENARIOS, generate_data
    canvas = DrawCanvas(pygame.Rect(0, 0, 750, 600))
    X, y = generate_data(SCENARIOS[0], seed=0)
    canvas.load_data(X, y)
    surf = pygame.Surface((750, 600))
    canvas.draw(surf)
    assert not canvas.is_valid()   # no polyline yet
    pygame.quit()

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

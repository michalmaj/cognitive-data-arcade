def test_config_defaults() -> None:
    from cognitive_data_arcade.games.gono.config import GoNoGoConfig

    c = GoNoGoConfig()
    assert c.num_trials == 80
    assert c.go_ratio == 0.75


def test_presets_ordering() -> None:
    from cognitive_data_arcade.games.gono.config import FULL, QUICK, STANDARD

    assert QUICK.num_trials < STANDARD.num_trials < FULL.num_trials


def test_generate_trials_count() -> None:
    from cognitive_data_arcade.games.gono.config import STANDARD
    from cognitive_data_arcade.games.gono.game import _generate_trials

    trials = _generate_trials(STANDARD)
    assert len(trials) == STANDARD.num_trials


def test_generate_trials_go_ratio() -> None:
    from cognitive_data_arcade.games.gono.config import STANDARD
    from cognitive_data_arcade.games.gono.game import _generate_trials

    trials = _generate_trials(STANDARD)
    go_count = sum(1 for t in trials if t["trial_type"] == "go")
    expected = round(STANDARD.go_ratio * STANDARD.num_trials)
    assert go_count == expected

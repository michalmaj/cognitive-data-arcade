from __future__ import annotations

from pathlib import Path


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
    num_blocks = STANDARD.num_trials // STANDARD.trials_per_block
    expected = round(STANDARD.go_ratio * STANDARD.trials_per_block) * num_blocks
    assert go_count == expected


def test_initial_phase_is_iti(tmp_path: Path) -> None:
    import pygame

    pygame.init()
    from cognitive_data_arcade.engine.i18n import PL
    from cognitive_data_arcade.games.gono.config import QUICK
    from cognitive_data_arcade.games.gono.game import GoNoGoGame, _Phase
    from cognitive_data_arcade.profile.manager import ProfileManager

    pm = ProfileManager(tmp_path / "profile.json")
    csv_path = tmp_path / "gono.csv"
    game = GoNoGoGame(QUICK, pm, PL, "pid", "sid", csv_path)
    assert game._phase == _Phase.ITI
    assert not game.is_done()


def test_draw_without_crash(tmp_path: Path) -> None:
    import pygame

    pygame.init()
    from cognitive_data_arcade.engine.i18n import PL
    from cognitive_data_arcade.games.gono.config import QUICK
    from cognitive_data_arcade.games.gono.game import GoNoGoGame
    from cognitive_data_arcade.profile.manager import ProfileManager

    pm = ProfileManager(tmp_path / "profile.json")
    csv_path = tmp_path / "gono.csv"
    game = GoNoGoGame(QUICK, pm, PL, "pid", "sid", csv_path)
    surface = pygame.Surface((1024, 768))
    game.draw(surface)  # must not raise


def test_space_on_go_trial_is_hit(tmp_path: Path) -> None:
    import pygame

    pygame.init()
    from cognitive_data_arcade.engine.i18n import PL
    from cognitive_data_arcade.games.gono.config import QUICK
    from cognitive_data_arcade.games.gono.game import GoNoGoGame, _Phase
    from cognitive_data_arcade.profile.manager import ProfileManager

    pm = ProfileManager(tmp_path / "profile.json")
    csv_path = tmp_path / "gono.csv"
    game = GoNoGoGame(QUICK, pm, PL, "pid", "sid", csv_path)
    # Force first trial to be GO and move to STIMULUS phase
    game._trials[0] = {"trial_type": "go"}
    game._phase = _Phase.STIMULUS
    game._phase_timer = 250.0
    game.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" ")
    )
    assert game._records[-1].response == "hit"
    assert game._records[-1].correct is True


def test_space_on_nogo_trial_is_false_alarm(tmp_path: Path) -> None:
    import pygame

    pygame.init()
    from cognitive_data_arcade.engine.i18n import PL
    from cognitive_data_arcade.games.gono.config import QUICK
    from cognitive_data_arcade.games.gono.game import GoNoGoGame, _Phase
    from cognitive_data_arcade.profile.manager import ProfileManager

    pm = ProfileManager(tmp_path / "profile.json")
    csv_path = tmp_path / "gono.csv"
    game = GoNoGoGame(QUICK, pm, PL, "pid", "sid", csv_path)
    game._trials[0] = {"trial_type": "nogo"}
    game._phase = _Phase.STIMULUS
    game._phase_timer = 250.0
    game.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" ")
    )
    assert game._records[-1].response == "false_alarm"
    assert game._records[-1].correct is False


def test_timeout_on_go_trial_is_miss(tmp_path: Path) -> None:
    import pygame

    pygame.init()
    from cognitive_data_arcade.engine.i18n import PL
    from cognitive_data_arcade.games.gono.config import QUICK
    from cognitive_data_arcade.games.gono.game import GoNoGoGame, _Phase
    from cognitive_data_arcade.profile.manager import ProfileManager

    pm = ProfileManager(tmp_path / "profile.json")
    csv_path = tmp_path / "gono.csv"
    game = GoNoGoGame(QUICK, pm, PL, "pid", "sid", csv_path)
    game._trials[0] = {"trial_type": "go"}
    game._phase = _Phase.STIMULUS
    game._phase_timer = 0.0
    game.update(game._config.stimulus_duration_ms + 1)
    assert game._records[-1].response == "miss"
    assert game._records[-1].correct is False


def test_silence_on_nogo_is_correct_rejection(tmp_path: Path) -> None:
    import pygame

    pygame.init()
    from cognitive_data_arcade.engine.i18n import PL
    from cognitive_data_arcade.games.gono.config import QUICK
    from cognitive_data_arcade.games.gono.game import GoNoGoGame, _Phase
    from cognitive_data_arcade.profile.manager import ProfileManager

    pm = ProfileManager(tmp_path / "profile.json")
    csv_path = tmp_path / "gono.csv"
    game = GoNoGoGame(QUICK, pm, PL, "pid", "sid", csv_path)
    game._trials[0] = {"trial_type": "nogo"}
    game._phase = _Phase.STIMULUS
    game._phase_timer = 0.0
    game.update(game._config.stimulus_duration_ms + 1)
    assert game._records[-1].response == "correct_rejection"
    assert game._records[-1].correct is True


def test_next_scene_is_session_summary_after_all_trials(tmp_path: Path) -> None:
    import pygame

    pygame.init()
    from cognitive_data_arcade.engine.i18n import PL
    from cognitive_data_arcade.games.gono.config import QUICK
    from cognitive_data_arcade.games.gono.game import GoNoGoGame, _Phase
    from cognitive_data_arcade.profile.manager import ProfileManager
    from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

    pm = ProfileManager(tmp_path / "profile.json")
    csv_path = tmp_path / "gono.csv"
    game = GoNoGoGame(QUICK, pm, PL, "pid", "sid", csv_path)
    # Simulate all trials by calling _complete_trial for each
    for i in range(QUICK.num_trials):
        game._trial_idx = i
        game._phase = _Phase.STIMULUS
        t = game._trials[i]
        if t["trial_type"] == "go":
            game._complete_trial("hit", True, 250.0)
        else:
            game._complete_trial("correct_rejection", True, 0.0)
        # Fast-forward feedback
        game.update(game._config.feedback_duration_ms + 1)
    assert isinstance(game.next_scene(), SessionSummaryScene)

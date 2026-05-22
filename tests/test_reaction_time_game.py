from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.games.reaction_time.config import ReactionTimeConfig
from cognitive_data_arcade.games.reaction_time.game import ReactionTimeGame, _compute_ap
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.session_summary import SessionSummaryScene


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


# Small config keeps tests fast: 4 trials, short timers, no between-blocks break
_FAST_CONFIG = ReactionTimeConfig(
    num_trials=4,
    trials_per_block=10,  # 4 trials never reaches 10 → no between-blocks break
    iti_min_ms=100,
    iti_max_ms=200,
    feedback_duration_ms=100,
)

_SPACE = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" ")


def _make_game(tmp_path: Path) -> ReactionTimeGame:
    pm = ProfileManager(tmp_path / "profile.json")
    pm.load()  # create default profile
    return ReactionTimeGame(
        config=_FAST_CONFIG,
        profile_manager=pm,
        strings=PL,
        participant_id="tester",
        session_id="test-session",
        csv_path=tmp_path / "rt.csv",
    )


def test_game_starts_in_instructions_phase(tmp_path: Path) -> None:
    from cognitive_data_arcade.games.reaction_time.game import _Phase

    game = _make_game(tmp_path)
    assert game._phase == _Phase.INSTRUCTIONS
    assert not game.is_done()


def test_space_advances_from_instructions(tmp_path: Path) -> None:
    from cognitive_data_arcade.games.reaction_time.game import _Phase

    game = _make_game(tmp_path)
    game.handle_event(_SPACE)
    assert game._phase == _Phase.COUNTDOWN


def test_early_press_does_not_advance_trial(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    game.handle_event(_SPACE)  # INSTRUCTIONS → COUNTDOWN
    game.update(3100.0)  # COUNTDOWN → ITI
    trial_before = game._trial_index
    game.handle_event(_SPACE)  # early press during ITI
    assert game._trial_index == trial_before


def test_correct_trial_increments_count(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    game.handle_event(_SPACE)  # → COUNTDOWN
    game.update(3100.0)  # → ITI
    game.update(250.0)  # ITI → STIMULUS (iti_max=200 ms, so 250 clears it)
    game.handle_event(_SPACE)  # respond → FEEDBACK
    assert game._trial_index == 1
    assert game._records[0].correct is True
    assert game._records[0].reaction_time_ms > 0


def test_timeout_records_incorrect_trial(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    game.handle_event(_SPACE)  # → COUNTDOWN
    game.update(3100.0)  # → ITI
    game.update(250.0)  # → STIMULUS
    game.update(11000.0)  # 10 s timeout → FEEDBACK (incorrect)
    assert game._trial_index == 1
    assert game._records[0].correct is False
    assert game._records[0].reaction_time_ms == -1.0


def test_game_done_after_all_trials(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    game.handle_event(_SPACE)  # → COUNTDOWN
    game.update(3100.0)  # → ITI
    for _ in range(_FAST_CONFIG.num_trials):
        game.update(250.0)  # ITI → STIMULUS
        game.handle_event(_SPACE)  # respond
        game.update(150.0)  # FEEDBACK → next ITI (or DONE on last)
    assert game.is_done()


def test_csv_written_per_trial(tmp_path: Path) -> None:
    import csv as csv_mod

    game = _make_game(tmp_path)
    game.handle_event(_SPACE)
    game.update(3100.0)
    game.update(250.0)  # → STIMULUS
    game.handle_event(_SPACE)  # respond
    game.update(150.0)  # → ITI

    with (tmp_path / "rt.csv").open() as f:
        rows = list(csv_mod.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["task_name"] == "reaction_time"
    assert rows[0]["distractor_count"] == "3"


def test_next_scene_is_session_summary(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    game.handle_event(_SPACE)
    game.update(3100.0)
    for _ in range(_FAST_CONFIG.num_trials):
        game.update(250.0)
        game.handle_event(_SPACE)
        game.update(150.0)
    assert game.is_done()
    assert isinstance(game.next_scene(), SessionSummaryScene)


def test_ap_applied_to_profile_after_completion(tmp_path: Path) -> None:
    pm = ProfileManager(tmp_path / "profile.json")
    pm.load()
    game = ReactionTimeGame(
        config=_FAST_CONFIG,
        profile_manager=pm,
        strings=PL,
        participant_id="tester",
        session_id="test-session",
        csv_path=tmp_path / "rt.csv",
    )
    game.handle_event(_SPACE)
    game.update(3100.0)
    for _ in range(_FAST_CONFIG.num_trials):
        game.update(250.0)
        game.handle_event(_SPACE)
        game.update(150.0)
    game.next_scene()  # triggers profile update
    assert pm.load().arcade_points > 0


def test_game_draw_does_not_crash(tmp_path: Path) -> None:
    pygame.init()
    surface = pygame.Surface((1024, 768))
    game = _make_game(tmp_path)
    game.draw(surface)  # INSTRUCTIONS phase
    game.handle_event(_SPACE)
    game.draw(surface)  # COUNTDOWN phase
    game.update(3100.0)
    game.draw(surface)  # ITI phase
    game.update(250.0)
    game.draw(surface)  # STIMULUS phase
    game.handle_event(_SPACE)
    game.draw(surface)  # FEEDBACK phase

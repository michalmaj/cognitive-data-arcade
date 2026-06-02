from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.games.stroop.config import StroopConfig
from cognitive_data_arcade.games.stroop.game import StroopGame
from cognitive_data_arcade.profile.manager import ProfileManager

_FAST_CONFIG = StroopConfig(
    num_trials=12,
    trials_per_block=12,
    num_colors=4,
    iti_min_ms=10,
    iti_max_ms=20,
    feedback_duration_ms=10,
    timeout_ms=500,
    ap_per_correct=2,
)

_SPACE = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" ")
_ENTER = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
_UP = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=0, unicode="")
_DOWN = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode="")


def _make_game(tmp_path: Path) -> StroopGame:
    pm = ProfileManager(tmp_path / "profile.json")
    pm.load()
    game = StroopGame(
        config=_FAST_CONFIG,
        profile_manager=pm,
        strings=PL,
        participant_id="tester",
        session_id="test-session",
        csv_path=tmp_path / "stroop.csv",
    )
    # Override presets to use _FAST_CONFIG as the default (at index 1)
    game._presets = [_FAST_CONFIG, _FAST_CONFIG, _FAST_CONFIG]
    return game


def _advance_to_stimulus(game: StroopGame) -> None:
    """Bring game from PRESET_SELECT all the way to STIMULUS."""
    game.handle_event(_ENTER)  # PRESET_SELECT → INSTRUCTIONS
    game.handle_event(_SPACE)  # INSTRUCTIONS → COUNTDOWN
    game.update(3100.0)  # COUNTDOWN → ITI
    game.update(25.0)  # ITI → STIMULUS (max iti=20 ms)


def test_preset_select_phase_is_initial(tmp_path: Path) -> None:
    from cognitive_data_arcade.games.stroop.game import _Phase

    game = _make_game(tmp_path)
    assert game._phase == _Phase.PRESET_SELECT
    assert not game.is_done()


def test_arrow_keys_change_preset(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    assert game._preset_idx == 1  # MEDIUM default
    game.handle_event(_UP)
    assert game._preset_idx == 0  # EASY
    game.handle_event(_DOWN)
    assert game._preset_idx == 1  # MEDIUM
    game.handle_event(_DOWN)
    assert game._preset_idx == 2  # HARD
    game.handle_event(_DOWN)
    assert game._preset_idx == 2  # clamps at max


def test_space_advances_to_instructions(tmp_path: Path) -> None:
    from cognitive_data_arcade.games.stroop.game import _Phase

    game = _make_game(tmp_path)
    game.handle_event(_SPACE)
    assert game._phase == _Phase.INSTRUCTIONS


def test_correct_trial_increments_count(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    _advance_to_stimulus(game)
    expected_key = game._current_stimulus.expected_key
    event = pygame.event.Event(pygame.KEYDOWN, key=expected_key, mod=0, unicode="")
    game.handle_event(event)
    assert game._trial_index == 1
    assert game._records[0].correct is True
    assert game._records[0].reaction_time_ms > 0


def test_wrong_key_records_incorrect(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    _advance_to_stimulus(game)
    expected_key = game._current_stimulus.expected_key
    color_keys = [pygame.K_r, pygame.K_g, pygame.K_b, pygame.K_y]
    wrong_key = next(k for k in color_keys if k != expected_key)
    event = pygame.event.Event(pygame.KEYDOWN, key=wrong_key, mod=0, unicode="")
    game.handle_event(event)
    assert game._records[0].correct is False
    assert game._records[0].reaction_time_ms > 0


def test_timeout_records_minus_one(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    _advance_to_stimulus(game)
    game.update(600.0)  # 500 ms timeout + 100 ms buffer
    assert game._records[0].reaction_time_ms == -1.0
    assert game._records[0].correct is False
    assert game._records[0].actual_response == "none"


def test_game_done_after_num_trials(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    _advance_to_stimulus(game)
    for _ in range(_FAST_CONFIG.num_trials):
        event = pygame.event.Event(
            pygame.KEYDOWN, key=game._current_stimulus.expected_key, mod=0, unicode=""
        )
        game.handle_event(event)
        game.update(_FAST_CONFIG.feedback_duration_ms + 1)
        if not game.is_done():
            game.update(_FAST_CONFIG.iti_max_ms + 1)
    assert game.is_done()


def test_csv_written(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    _advance_to_stimulus(game)
    event = pygame.event.Event(
        pygame.KEYDOWN, key=game._current_stimulus.expected_key, mod=0, unicode=""
    )
    game.handle_event(event)
    assert (tmp_path / "stroop.csv").exists()


def test_next_scene_is_session_summary(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

    game = _make_game(tmp_path)
    _advance_to_stimulus(game)
    for _ in range(_FAST_CONFIG.num_trials):
        event = pygame.event.Event(
            pygame.KEYDOWN, key=game._current_stimulus.expected_key, mod=0, unicode=""
        )
        game.handle_event(event)
        game.update(_FAST_CONFIG.feedback_duration_ms + 1)
        if not game.is_done():
            game.update(_FAST_CONFIG.iti_max_ms + 1)
    assert game.is_done()
    assert isinstance(game.next_scene(), SessionSummaryScene)


def test_word_color_semantics_across_conditions(tmp_path: Path) -> None:
    """Verify word_color is set correctly per condition in the trial record."""
    game = _make_game(tmp_path)
    _advance_to_stimulus(game)

    # Play enough trials to cover all three conditions
    # Run a full 12-trial block (one complete cycle)
    for _ in range(12):
        if game.is_done():
            break
        event = pygame.event.Event(
            pygame.KEYDOWN, key=game._current_stimulus.expected_key, mod=0, unicode=""
        )
        game.handle_event(event)
        game.update(_FAST_CONFIG.feedback_duration_ms + 1)
        if not game.is_done():
            game.update(_FAST_CONFIG.iti_max_ms + 1)

    for record in game._records:
        if record.condition == "neutral":
            assert record.word_color == "none", (
                f"Neutral trial should have word_color='none', got '{record.word_color}'"
            )
        elif record.condition == "congruent":
            assert record.word_color == record.ink_color, (
                f"Congruent trial: word_color '{record.word_color}' != ink_color '{record.ink_color}'"
            )
        elif record.condition == "incongruent":
            assert record.word_color != record.ink_color, (
                f"Incongruent trial: word_color '{record.word_color}' should differ from ink_color '{record.ink_color}'"
            )
            assert record.word_color != "none", (
                "Incongruent word_color should not be 'none'"
            )

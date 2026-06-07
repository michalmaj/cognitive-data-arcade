from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.i18n import EN, PL
from cognitive_data_arcade.games.event_log_detective.game import EventLogDetectiveGame, _State
from cognitive_data_arcade.games.event_log_detective.scenarios import SCENARIOS


class _FakePM:
    class _Profile:
        device_uuid = "test-uuid"

    def load(self):
        return self._Profile()


def _make_game(difficulty="medium", scenario_idx=0, lang="en"):
    pygame.init()
    strings = EN if lang == "en" else PL
    return EventLogDetectiveGame(SCENARIOS[scenario_idx], difficulty, strings, _FakePM())


# ── Initial state ──────────────────────────────────────────────────────────────

def test_initial_state_is_intro():
    assert _make_game()._state == _State.INTRO


def test_not_done_initially():
    game = _make_game()
    assert not game.is_done()
    assert game.next_scene() is None


# ── INTRO → CONFIG_MAP ─────────────────────────────────────────────────────────

def test_enter_on_intro_advances():
    game = _make_game()
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert game._state == _State.CONFIG_MAP


def test_space_on_intro_advances():
    game = _make_game()
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=""))
    assert game._state == _State.CONFIG_MAP


def test_other_key_on_intro_does_nothing():
    game = _make_game()
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode=""))
    assert game._state == _State.INTRO


# ── CONFIG_MAP navigation ──────────────────────────────────────────────────────

def test_enter_on_config_map_opens_decision():
    game = _make_game()
    game._state = _State.CONFIG_MAP
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert game._state == _State.DECISION


def test_down_increments_node():
    game = _make_game()
    game._state = _State.CONFIG_MAP
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode=""))
    assert game._node_idx == 1


def test_up_decrements_node():
    game = _make_game()
    game._state = _State.CONFIG_MAP
    game._node_idx = 2
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=0, unicode=""))
    assert game._node_idx == 1


def test_node_clamps_at_zero():
    game = _make_game()
    game._state = _State.CONFIG_MAP
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=0, unicode=""))
    assert game._node_idx == 0


def test_node_clamps_at_max():
    game = _make_game()
    game._state = _State.CONFIG_MAP
    n = len(SCENARIOS[0].decisions)
    for _ in range(n + 5):
        game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode=""))
    assert game._node_idx == n - 1


def test_enter_when_all_decided_goes_to_report():
    game = _make_game()
    game._state = _State.CONFIG_MAP
    for i in range(len(SCENARIOS[0].decisions)):
        game._choices[i] = 0
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert game._state == _State.REPORT


# ── DECISION navigation ────────────────────────────────────────────────────────

def test_backspace_in_decision_returns_to_config_map():
    game = _make_game()
    game._state = _State.DECISION
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, mod=0, unicode=""))
    assert game._state == _State.CONFIG_MAP


def test_left_in_decision_is_noop():
    game = _make_game()
    game._state = _State.DECISION
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=0, unicode=""))
    assert game._state == _State.DECISION


def test_down_increments_option():
    game = _make_game()
    game._state = _State.DECISION
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode=""))
    assert game._option_idx == 1


def test_up_clamps_option_at_zero():
    game = _make_game()
    game._state = _State.DECISION
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=0, unicode=""))
    assert game._option_idx == 0


def test_number_key_sets_option():
    game = _make_game()
    game._state = _State.DECISION
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_2, mod=0, unicode="2"))
    assert game._option_idx == 1


def test_confirm_decision_saves_and_returns_to_map():
    game = _make_game()
    game._state = _State.DECISION
    game._node_idx = 0
    game._option_idx = 0
    game._confirm_decision()
    assert game._choices[0] == 0
    assert game._state == _State.CONFIG_MAP


# ── Easy difficulty popup ──────────────────────────────────────────────────────

def test_easy_popup_shown_for_wrong_answer():
    game = _make_game(difficulty="easy")
    game._state = _State.DECISION
    game._node_idx = 0
    wrong_idx = next(j for j, o in enumerate(game._shuffled_options[0]) if not o.is_correct)
    game._option_idx = wrong_idx
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert game._popup_visible


def test_easy_popup_shown_for_correct_answer():
    # On Easy, correct choices also show a popup explaining WHY the choice was good.
    game = _make_game(difficulty="easy")
    game._state = _State.DECISION
    game._node_idx = 0
    correct_idx = next(j for j, o in enumerate(game._shuffled_options[0]) if o.is_correct)
    game._option_idx = correct_idx
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert game._popup_visible
    assert game._popup_is_correct


def test_medium_no_popup_for_wrong_answer():
    game = _make_game(difficulty="medium")
    game._state = _State.DECISION
    game._node_idx = 0
    wrong_idx = next(j for j, o in enumerate(game._shuffled_options[0]) if not o.is_correct)
    game._option_idx = wrong_idx
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert not game._popup_visible
    assert game._choices[0] == wrong_idx


def test_popup_enter_confirms_and_closes():
    game = _make_game(difficulty="easy")
    game._state = _State.DECISION
    game._popup_visible = True
    game._node_idx = 0
    game._option_idx = 1
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert not game._popup_visible
    assert game._choices[0] == 1
    assert game._state == _State.CONFIG_MAP


def test_popup_backspace_closes_without_saving():
    game = _make_game(difficulty="easy")
    game._state = _State.DECISION
    game._popup_visible = True
    game._node_idx = 0
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, mod=0, unicode=""))
    assert not game._popup_visible
    assert game._choices[0] is None


# ── Score calculation ──────────────────────────────────────────────────────────

def test_all_decided_false_initially():
    assert not _make_game()._all_decided()


def test_all_decided_true_when_all_set():
    game = _make_game()
    for i in range(len(SCENARIOS[0].decisions)):
        game._choices[i] = 0
    assert game._all_decided()


def test_score_all_correct_hard():
    game = _make_game(difficulty="hard")
    for i in range(len(game._scenario.decisions)):
        correct_idx = next(j for j, o in enumerate(game._shuffled_options[i]) if o.is_correct)
        game._choices[i] = correct_idx
    correct, total, score = game._score()
    assert correct == total == len(game._scenario.decisions)
    assert score == total * 3


def test_score_multiplier_easy():
    game = _make_game(difficulty="easy")
    for i in range(len(game._scenario.decisions)):
        correct_idx = next(j for j, o in enumerate(game._shuffled_options[i]) if o.is_correct)
        game._choices[i] = correct_idx
    correct, total, score = game._score()
    assert score == correct * 1


def test_score_zero_when_all_wrong():
    game = _make_game(difficulty="medium")
    for i in range(len(game._scenario.decisions)):
        wrong_idx = next((j for j, o in enumerate(game._shuffled_options[i]) if not o.is_correct), None)
        if wrong_idx is None:
            wrong_idx = 0
        game._choices[i] = wrong_idx
    correct, total, score = game._score()
    assert correct == 0
    assert score == 0


# ── REPORT navigation ──────────────────────────────────────────────────────────

def test_report_backspace_navigates_to_level_scene():
    from cognitive_data_arcade.ui.event_log_level_scene import EventLogLevelScene
    game = _make_game()
    game._state = _State.REPORT
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, mod=0, unicode=""))
    assert game.is_done()
    assert isinstance(game.next_scene(), EventLogLevelScene)


def test_report_enter_replays_same_scenario():
    game = _make_game()
    game._state = _State.REPORT
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert game.is_done()
    assert isinstance(game.next_scene(), EventLogDetectiveGame)


# ── Draw smoke tests ──────────────────────────────────────────────────────────

def test_draw_intro_does_not_crash():
    pygame.display.set_mode((800, 600), pygame.NOFRAME)
    game = _make_game()
    game.draw(pygame.display.get_surface())


def test_draw_config_map_does_not_crash():
    pygame.display.set_mode((800, 600), pygame.NOFRAME)
    game = _make_game()
    game._state = _State.CONFIG_MAP
    game.draw(pygame.display.get_surface())


def test_draw_decision_does_not_crash():
    pygame.display.set_mode((800, 600), pygame.NOFRAME)
    game = _make_game()
    game._state = _State.DECISION
    game.draw(pygame.display.get_surface())


def test_draw_report_does_not_crash():
    pygame.display.set_mode((800, 600), pygame.NOFRAME)
    game = _make_game()
    game._state = _State.REPORT
    for i in range(len(SCENARIOS[0].decisions)):
        game._choices[i] = 0
    game.draw(pygame.display.get_surface())


# ── Option shuffle ─────────────────────────────────────────────────────────────

def test_options_are_shuffled_differently_across_games():
    """Two game instances must not always produce the same option order."""
    import random
    orders = set()
    for seed in range(20):
        random.seed(seed)
        game = _make_game(scenario_idx=0)
        order = tuple(opt.label_en for opt in game._shuffled_options[0])
        orders.add(order)
    assert len(orders) > 1


def test_shuffled_options_same_length_as_original():
    game = _make_game()
    for i, dec in enumerate(game._scenario.decisions):
        assert len(game._shuffled_options[i]) == len(dec.options)
        assert set(game._shuffled_options[i]) == set(dec.options)

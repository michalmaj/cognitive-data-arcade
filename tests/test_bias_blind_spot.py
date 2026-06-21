"""Tests for L30 Bias Blind Spot."""

from __future__ import annotations
import pygame


def test_game_state_defaults():
    from cognitive_data_arcade.games.bias_blind_spot.game_state import GameState

    s = GameState()
    assert s.act1_choice == ""
    assert s.act1_correct is False
    assert s.bias_rounds == []
    assert s.accuracy_rounds == []
    assert s.regulator_choice == ""
    assert s.score_engineer == 0


def test_act1_correct_answer():
    from cognitive_data_arcade.games.bias_blind_spot.game_state import ACT1_CORRECT

    assert ACT1_CORRECT == "zipcode"


def test_engineer_bias_decreases_when_zip_removed():
    from cognitive_data_arcade.games.bias_blind_spot.game_state import compute_round_result

    bias_before = 33.0
    bias_after, _ = compute_round_result(frozenset({"zip_code"}))
    assert bias_after < bias_before


def test_engineer_accuracy_drops_when_too_many_removed():
    from cognitive_data_arcade.games.bias_blind_spot.game_state import (
        compute_round_result,
        STARTING_ACC,
    )

    _, acc = compute_round_result(frozenset({"zip_code", "debt_ratio", "income"}))
    assert acc < STARTING_ACC - 0.10


def test_score_engineer_formula():
    from cognitive_data_arcade.games.bias_blind_spot.game_state import compute_score_engineer

    assert compute_score_engineer(24.0, 0.79) == 100
    assert compute_score_engineer(0.0, 0.0) == 0
    score = compute_score_engineer(24.0, 0.79)
    assert 0 <= score <= 100


def test_regulator_consequence_table():
    from cognitive_data_arcade.games.bias_blind_spot.game_state import CONSEQUENCE_TABLE

    for choice in ("parity", "opportunity", "calibration"):
        row = CONSEQUENCE_TABLE[choice]
        ok_count = sum(1 for k in ("parity", "opportunity", "calibration") if row[k])
        assert ok_count == 1
        assert row[choice] is True
        assert 0.0 < row["accuracy"] <= 1.0


def test_stars_formula():
    from cognitive_data_arcade.games.bias_blind_spot.game_state import stars_from_score

    assert stars_from_score(70) == 3
    assert stars_from_score(100) == 3
    assert stars_from_score(69) == 2
    assert stars_from_score(45) == 2
    assert stars_from_score(44) == 1
    assert stars_from_score(0) == 1


# ---------------------------------------------------------------------------
# Task 2 — PhaseIntroScene render smoke
# ---------------------------------------------------------------------------


def test_phase_intro_renders():
    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.bias_blind_spot.game_state import GameState
    from cognitive_data_arcade.games.bias_blind_spot.phase_intro import PhaseIntroScene

    scene = PhaseIntroScene(GameState())
    scene.update(0)
    scene.draw(surface)  # must not raise
    assert not scene.is_done()
    pygame.quit()


# ---------------------------------------------------------------------------
# Task 3 — PhaseApplicantScene render smoke
# ---------------------------------------------------------------------------


def test_phase_applicant_renders():
    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.bias_blind_spot.game_state import GameState
    from cognitive_data_arcade.games.bias_blind_spot.phase_applicant import PhaseApplicantScene

    scene = PhaseApplicantScene(GameState())
    scene.update(0)
    scene.draw(surface)  # must not raise
    assert not scene.is_done()
    pygame.quit()


# ---------------------------------------------------------------------------
# Task 5 — PhaseEngineerScene render smoke
# ---------------------------------------------------------------------------


def test_phase_engineer_renders():
    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.bias_blind_spot.game_state import GameState
    from cognitive_data_arcade.games.bias_blind_spot.phase_engineer import PhaseEngineerScene

    scene = PhaseEngineerScene(GameState())
    scene.update(0)
    scene.draw(surface)  # must not raise
    assert not scene.is_done()
    pygame.quit()


# ---------------------------------------------------------------------------
# Task 6 — PhaseRegulatorScene render smoke
# ---------------------------------------------------------------------------


def test_phase_regulator_renders():
    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.bias_blind_spot.game_state import GameState
    from cognitive_data_arcade.games.bias_blind_spot.phase_regulator import PhaseRegulatorScene

    scene = PhaseRegulatorScene(GameState())
    scene.update(0)
    scene.draw(surface)  # must not raise
    assert not scene.is_done()
    pygame.quit()


# ---------------------------------------------------------------------------
# Task 7 — PhaseResultScene render smoke
# ---------------------------------------------------------------------------


def test_phase_result_renders():
    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.bias_blind_spot.game_state import GameState
    from cognitive_data_arcade.games.bias_blind_spot.phase_result import PhaseResultScene

    state = GameState()
    state.act1_correct = True
    state.bias_rounds = [21.0, 14.0, 9.0]
    state.accuracy_rounds = [0.76, 0.71, 0.58]
    state.score_engineer = 72
    state.regulator_choice = "parity"
    scene = PhaseResultScene(state)
    scene.update(0)
    scene.draw(surface)  # must not raise
    pygame.quit()


# ---------------------------------------------------------------------------
# Task 8 — BiasBlindSpotScene coordinator smoke
# ---------------------------------------------------------------------------


def test_game_renders_3_frames():
    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.bias_blind_spot.game import BiasBlindSpotScene

    scene = BiasBlindSpotScene()
    for _ in range(3):
        scene.update(16)
        scene.draw(surface)
    assert not scene.is_done()
    pygame.quit()


# ---------------------------------------------------------------------------
# Task 9 — Lesson 30 structure
# ---------------------------------------------------------------------------


def test_lesson_30_structure():
    from cognitive_data_arcade.lessons.lesson_30 import CONTENT

    for lang in ("pl", "en"):
        assert len(CONTENT[lang]["theory"]) == 4
        assert len(CONTENT[lang]["notes"]) == 2
        assert len(CONTENT[lang]["tasks"]) == 3


# ---------------------------------------------------------------------------
# Task 10 — Menu wiring
# ---------------------------------------------------------------------------


def test_menu_has_lesson_30():
    from cognitive_data_arcade.ui.menu import _LESSONS

    nums = [n for n, _ in _LESSONS]
    assert 30 in nums

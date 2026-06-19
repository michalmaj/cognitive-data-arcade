"""Tests for L30 Bias Blind Spot."""
from __future__ import annotations
import pygame
import pytest


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
        compute_round_result, STARTING_ACC,
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

# tests/test_phase_b.py
from __future__ import annotations
import pytest
import numpy as np
import pygame

@pytest.fixture(autouse=True)
def pg():
    pygame.init()
    pygame.display.set_mode((1024, 720))
    yield
    pygame.quit()


def test_match_score_100_when_equal():
    from cognitive_data_arcade.games.distribution_playground.simulator import (
        match_score, simulate,
    )
    r = simulate("normal", {"mu": 400, "sigma": 80, "N": 50}, rng_seed=1)
    score = match_score(r.dist_type, r.params, r.dist_type, r.params)
    assert score == 100.0


def test_match_score_less_when_different():
    from cognitive_data_arcade.games.distribution_playground.simulator import match_score
    score = match_score("normal", {"mu": 600, "sigma": 80, "N": 50},
                        "normal", {"mu": 400, "sigma": 80, "N": 50})
    assert score < 100.0


def test_phase_b_initialises_without_crash():
    from cognitive_data_arcade.games.distribution_playground.phase_b import PhaseBScene
    scene = PhaseBScene()
    assert scene is not None


def test_phase_b_hint_increments():
    from cognitive_data_arcade.games.distribution_playground.phase_b import PhaseBScene
    scene = PhaseBScene()
    initial_hints = scene.hints_used()
    scene.use_hint()
    assert scene.hints_used() == initial_hints + 1


def test_phase_b_max_3_hints():
    from cognitive_data_arcade.games.distribution_playground.phase_b import PhaseBScene
    scene = PhaseBScene()
    for _ in range(5):
        scene.use_hint()
    assert scene.hints_used() <= 3


def test_phase_b_give_up_reveals_target():
    from cognitive_data_arcade.games.distribution_playground.phase_b import PhaseBScene
    scene = PhaseBScene()
    assert not scene.target_revealed()
    scene.give_up()
    assert scene.target_revealed()


def test_phase_b_new_target_resets_state():
    from cognitive_data_arcade.games.distribution_playground.phase_b import PhaseBScene
    scene = PhaseBScene()
    scene.give_up()
    scene.new_target()
    assert not scene.target_revealed()
    assert scene.hints_used() == 0

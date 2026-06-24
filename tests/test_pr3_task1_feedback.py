"""Tests for PR3 Task 1: per-decision visual feedback."""

from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame


def test_submit_enters_feedback_scene() -> None:
    """After submit, next scene is PhaseFeedbackScene."""
    pygame.init()
    from cognitive_data_arcade.games.semantic_space.phase_feedback import PhaseFeedbackScene
    from cognitive_data_arcade.games.semantic_space.phase_mission import PhaseMissionScene
    from cognitive_data_arcade.games.semantic_space.missions import build_session

    missions = build_session()
    scene = PhaseMissionScene(missions, round_idx=0, session_score=0, round_results=[])
    m = missions[0]
    # inject a valid answer selection
    if hasattr(m, "answers") and m.answers:
        scene._selected = {m.answers[0]}
    else:
        scene._selected = set()
    scene._submit()
    nxt = scene.next_scene()
    assert isinstance(nxt, PhaseFeedbackScene)


def test_feedback_advances_after_delay() -> None:
    """PhaseFeedbackScene.is_done() becomes True after 1500 ms."""
    pygame.init()
    from cognitive_data_arcade.games.semantic_space.phase_feedback import PhaseFeedbackScene

    fb = PhaseFeedbackScene(
        is_correct=True,
        score=30,
        answers=["model"],
        mission_type="analogy",
        next_scene_factory=lambda: None,
    )
    assert not fb.is_done()
    fb.update(1501)
    assert fb.is_done()

"""Failing tests for Task 5: Module 5 NLP games."""

from pathlib import Path
import pygame
import pytest

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.session_summary import SessionSummaryScene


def _pm(tmp_path: Path) -> ProfileManager:
    pm = ProfileManager(tmp_path / "profile.json")
    pm.load()
    return pm


def test_text_tokenizer_q_routes_to_session_summary(tmp_path: Path) -> None:
    pygame.init()
    from cognitive_data_arcade.games.text_tokenizer.scene import TextTokenizerLabScene

    pm = _pm(tmp_path)
    game = TextTokenizerLabScene(pm, PL)
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q, mod=0, unicode="q"))
    assert game.is_done()
    assert isinstance(game.next_scene(), SessionSummaryScene)
    assert pm.load().arcade_points > 0


def test_human_vs_model_esc_routes_to_summary(tmp_path: Path) -> None:
    pygame.init()
    from cognitive_data_arcade.games.human_vs_model.phase_result import PhaseResultScene

    pm = _pm(tmp_path)
    scene = PhaseResultScene(session_score=120, beat_ai_count=4, pm=pm, strings=PL)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), SessionSummaryScene)
    assert pm.load().arcade_points > 0

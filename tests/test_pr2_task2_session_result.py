"""Failing tests for Task 2: Visual Search Lab, Cognitive Dashboard."""

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


def test_visual_search_done_routes_to_session_summary(tmp_path: Path) -> None:
    """After all trials, VisualSearchGame.next_scene() must be SessionSummaryScene."""
    pygame.init()
    from cognitive_data_arcade.games.visual_search.game import VisualSearchGame
    from cognitive_data_arcade.games.visual_search.config import VSConfig

    pm = _pm(tmp_path)
    cfg = VSConfig(mode="letters", difficulty="easy")  # minimal config
    csv_path = tmp_path / "vs.csv"
    game = VisualSearchGame(cfg, pm, PL, "p1", "s1", csv_path)
    # Force DONE phase
    from cognitive_data_arcade.games.visual_search.game import _Phase

    game._phase = _Phase.DONE
    scene = game.next_scene()
    assert isinstance(scene, SessionSummaryScene)


def test_cognitive_dashboard_q_routes_to_session_summary(tmp_path: Path) -> None:
    """When session complete, pressing Q must produce SessionSummaryScene."""
    pygame.init()
    from cognitive_data_arcade.games.cognitive_dashboard.dashboard_scene import (
        CognitiveDashboardScene,
    )
    from cognitive_data_arcade.games.cognitive_dashboard.config import generate_synthetic

    pm = _pm(tmp_path)
    session = generate_synthetic()
    game = CognitiveDashboardScene(session, PL, pm)
    assert session.is_complete()
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q, mod=0, unicode="q"))
    assert game.is_done()
    assert isinstance(game.next_scene(), SessionSummaryScene)

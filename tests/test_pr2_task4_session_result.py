"""Failing tests for Task 4: Module 4 games."""

from pathlib import Path
import pygame
import pytest
from unittest.mock import MagicMock

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.session_summary import SessionSummaryScene


def _pm(tmp_path: Path) -> ProfileManager:
    pm = ProfileManager(tmp_path / "profile.json")
    pm.load()
    return pm


def test_feature_hunter_done_routes_to_session_summary(tmp_path: Path) -> None:
    """When all phases complete, FeatHunterScene.next_scene() must be SessionSummaryScene."""
    pygame.init()
    from cognitive_data_arcade.games.feature_hunter.game import FeatHunterScene

    pm = _pm(tmp_path)
    game = FeatHunterScene(pm, PL)
    # Force done state: stub current scene as done with no next
    game._phases_completed = 3
    stub = MagicMock()
    stub.is_done.return_value = True
    stub.next_scene.return_value = None
    game._current = stub
    game.update(0.0)
    assert game.is_done()
    assert isinstance(game.next_scene(), SessionSummaryScene)
    assert pm.load().arcade_points > 0


def test_anomaly_alert_esc_routes_to_session_summary(tmp_path: Path) -> None:
    """PhaseSessionResultScene in AnomalyAlert must route to SessionSummaryScene via ESC."""
    pygame.init()
    from cognitive_data_arcade.games.anomaly_alert.phase_session_result import (
        PhaseSessionResultScene,
    )

    pm = _pm(tmp_path)
    results = [
        {
            "round_idx": 0,
            "score": 30,
            "chart_type": "bar",
            "found": 2,
            "total_anomalies": 3,
            "false_alarms": 1,
            "time_bonus": 5,
        }
    ]
    scene = PhaseSessionResultScene(results, pm, PL)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), SessionSummaryScene)
    assert pm.load().arcade_points > 0

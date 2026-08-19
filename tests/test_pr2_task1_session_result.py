"""Tests for Task 1 SessionResult wiring: L01, L03, L06."""

from __future__ import annotations

from pathlib import Path

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.session_summary import SessionSummaryScene


@pytest.fixture(autouse=True)
def pg():
    pygame.init()
    yield
    pygame.quit()


def _pm(tmp_path: Path) -> ProfileManager:
    pm = ProfileManager(tmp_path / "profile.json")
    pm.load()
    return pm


def test_big_data_map_q_routes_to_session_summary(tmp_path):
    from cognitive_data_arcade.games.big_data_map.game import BigDataMapGame

    pm = _pm(tmp_path)
    game = BigDataMapGame(PL, pm)
    # Q shows the summary overlay first (PR3)
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q, mod=0, unicode="q"))
    assert game._show_summary is True
    assert not game.is_done()  # not done yet - summary is showing
    # Dismiss the summary with a click - now done
    game.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(512, 400)))
    assert game.is_done()
    assert isinstance(game.next_scene(), SessionSummaryScene)


def test_eld_report_enter_routes_to_session_summary(tmp_path):
    from cognitive_data_arcade.games.event_log_detective.game import EventLogDetectiveGame, _State
    from cognitive_data_arcade.games.event_log_detective.scenarios import SCENARIOS

    pm = _pm(tmp_path)
    game = EventLogDetectiveGame(SCENARIOS[0], "medium", PL, pm)
    # Set all choices to make the game ready for report
    for i in range(len(SCENARIOS[0].decisions)):
        game._choices[i] = 0
    game._state = _State.REPORT
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert game.is_done()
    assert isinstance(game.next_scene(), SessionSummaryScene)


def test_eld_double_enter_does_not_double_award(tmp_path):
    """Two ENTER presses in REPORT must award AP only once."""
    from cognitive_data_arcade.games.event_log_detective.game import EventLogDetectiveGame, _State
    from cognitive_data_arcade.games.event_log_detective.scenarios import SCENARIOS

    pm = _pm(tmp_path)
    game = EventLogDetectiveGame(SCENARIOS[0], "medium", PL, pm)
    # Set all choices so the game is ready for the report screen
    for i in range(len(SCENARIOS[0].decisions)):
        game._choices[i] = 0
    game._state = _State.REPORT

    enter = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="")
    game.handle_event(enter)
    assert game.is_done()
    ap_after_first = pm.load().arcade_points

    # Second ENTER must not call _build_next_scene() again (no double add_ap)
    game.handle_event(enter)
    ap_after_second = pm.load().arcade_points

    assert ap_after_first == ap_after_second, (
        f"AP was awarded twice: {ap_after_first} -> {ap_after_second}"
    )


def test_eda_sandbox_q_routes_to_session_summary(tmp_path):
    from cognitive_data_arcade.games.eda.scene import EDAScene

    pm = _pm(tmp_path)
    game = EDAScene(pm, PL)
    # Q shows the summary overlay first (PR3)
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q, mod=0, unicode="q"))
    assert game._show_summary is True
    assert not game.is_done()  # not done yet - summary is showing
    # Dismiss the summary with a click - now done
    game.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(512, 400)))
    assert game.is_done()
    assert isinstance(game.next_scene(), SessionSummaryScene)

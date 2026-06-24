"""Failing tests for Task 6: Module 6 network/ethics games."""

from pathlib import Path
import pygame

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.session_summary import SessionSummaryScene


def _pm(tmp_path: Path) -> ProfileManager:
    pm = ProfileManager(tmp_path / "profile.json")
    pm.load()
    return pm


def test_social_network_q_routes_to_session_summary(tmp_path: Path) -> None:
    pygame.init()
    from cognitive_data_arcade.games.social_network.game import SocialNetworkScene

    pm = _pm(tmp_path)
    game = SocialNetworkScene(pm, PL)
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q, mod=0, unicode="q"))
    assert game.is_done()
    assert isinstance(game.next_scene(), SessionSummaryScene)
    assert pm.load().arcade_points > 0


def test_architects_trial_ends_with_session_summary(tmp_path: Path) -> None:
    pygame.init()
    from cognitive_data_arcade.games.architects_trial.game import ArchitectsTrialScene

    pm = _pm(tmp_path)
    game = ArchitectsTrialScene(pm, PL)
    game._state.fairness_score = 80
    game._state.compliance_score = 70
    game._state.effectiveness_score = 60
    game._done = True
    game._next = game._build_next_scene()
    assert isinstance(game.next_scene(), SessionSummaryScene)
    assert pm.load().arcade_points > 0

"""Failing tests for Task 3: Module 3 sandboxes."""

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


@pytest.mark.parametrize(
    "lesson_cls,module_path",
    [
        (
            "DistributionPlaygroundScene",
            "cognitive_data_arcade.games.distribution_playground.scene",
        ),
        ("CorrelationTrapScene", "cognitive_data_arcade.games.correlation_trap.scene"),
        ("HypothesisArenaScene", "cognitive_data_arcade.games.hypothesis_arena.scene"),
        ("PredictionSliderScene", "cognitive_data_arcade.games.prediction_slider.scene"),
    ],
)
def test_sandbox_q_routes_to_session_summary(lesson_cls, module_path, tmp_path: Path) -> None:
    """Pressing Q on any Module 3 sandbox must produce SessionSummaryScene."""
    pygame.init()
    import importlib

    mod = importlib.import_module(module_path)
    cls = getattr(mod, lesson_cls)
    pm = _pm(tmp_path)
    game = cls(pm, PL)
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q, mod=0, unicode="q"))
    # Games with summary overlay require timer to expire before is_done() is True
    if getattr(game, "_show_summary", False):
        game._summary_timer = 10_001
        game.update(0)
    assert game.is_done()
    assert isinstance(game.next_scene(), SessionSummaryScene)
    assert pm.load().arcade_points > 0

# tests/test_distribution_scene.py
from __future__ import annotations
import pytest
import pygame
from pathlib import Path
from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager


@pytest.fixture(autouse=True)
def pg():
    pygame.init()
    pygame.display.set_mode((1024, 720))
    yield
    pygame.quit()


@pytest.fixture()
def pm(tmp_path: Path) -> ProfileManager:
    p = ProfileManager(tmp_path / "profile.json")
    p.load()
    return p


def test_scene_init_no_crash(pm):
    from cognitive_data_arcade.games.distribution_playground.scene import (
        DistributionPlaygroundScene,
    )

    scene = DistributionPlaygroundScene(pm, PL)
    assert scene is not None


def test_scene_is_not_done_initially(pm):
    from cognitive_data_arcade.games.distribution_playground.scene import (
        DistributionPlaygroundScene,
    )

    scene = DistributionPlaygroundScene(pm, PL)
    assert not scene.is_done()


def test_right_arrow_advances_phase(pm):
    from cognitive_data_arcade.games.distribution_playground.scene import (
        DistributionPlaygroundScene,
    )

    scene = DistributionPlaygroundScene(pm, PL)
    assert scene.current_phase() == 1
    ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT, "mod": 0, "unicode": ""})
    scene.handle_event(ev)
    assert scene.current_phase() == 2


def test_left_arrow_wraps_to_phase_3(pm):
    from cognitive_data_arcade.games.distribution_playground.scene import (
        DistributionPlaygroundScene,
    )

    scene = DistributionPlaygroundScene(pm, PL)
    ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT, "mod": 0, "unicode": ""})
    scene.handle_event(ev)
    assert scene.current_phase() == 3


def test_draw_no_crash_all_phases(pm):
    from cognitive_data_arcade.games.distribution_playground.scene import (
        DistributionPlaygroundScene,
    )

    surf = pygame.display.get_surface()
    assert surf is not None
    scene = DistributionPlaygroundScene(pm, PL)
    for _ in range(3):
        scene.draw(surf)
        ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT, "mod": 0, "unicode": ""})
        scene.handle_event(ev)

# tests/test_distribution_scene.py
from __future__ import annotations
import pytest
import pygame


@pytest.fixture(autouse=True)
def pg():
    pygame.init()
    pygame.display.set_mode((1024, 720))
    yield
    pygame.quit()


def test_scene_init_no_crash():
    from cognitive_data_arcade.games.distribution_playground.scene import (
        DistributionPlaygroundScene,
    )
    scene = DistributionPlaygroundScene()
    assert scene is not None


def test_scene_is_not_done_initially():
    from cognitive_data_arcade.games.distribution_playground.scene import (
        DistributionPlaygroundScene,
    )
    scene = DistributionPlaygroundScene()
    assert not scene.is_done()


def test_right_arrow_advances_phase():
    from cognitive_data_arcade.games.distribution_playground.scene import (
        DistributionPlaygroundScene,
    )
    scene = DistributionPlaygroundScene()
    assert scene.current_phase() == 1
    ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT, "mod": 0, "unicode": ""})
    scene.handle_event(ev)
    assert scene.current_phase() == 2


def test_left_arrow_wraps_to_phase_3():
    from cognitive_data_arcade.games.distribution_playground.scene import (
        DistributionPlaygroundScene,
    )
    scene = DistributionPlaygroundScene()
    ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT, "mod": 0, "unicode": ""})
    scene.handle_event(ev)
    assert scene.current_phase() == 3


def test_draw_no_crash_all_phases():
    from cognitive_data_arcade.games.distribution_playground.scene import (
        DistributionPlaygroundScene,
    )
    surf = pygame.display.get_surface()
    assert surf is not None
    scene = DistributionPlaygroundScene()
    for _ in range(3):
        scene.draw(surf)
        ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT, "mod": 0, "unicode": ""})
        scene.handle_event(ev)

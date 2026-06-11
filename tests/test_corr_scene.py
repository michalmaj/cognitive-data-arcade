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
    from cognitive_data_arcade.games.correlation_trap.scene import CorrelationTrapScene
    scene = CorrelationTrapScene()
    assert scene is not None


def test_scene_is_not_done_initially():
    from cognitive_data_arcade.games.correlation_trap.scene import CorrelationTrapScene
    scene = CorrelationTrapScene()
    assert not scene.is_done()


def test_right_arrow_advances_phase():
    from cognitive_data_arcade.games.correlation_trap.scene import CorrelationTrapScene
    scene = CorrelationTrapScene()
    assert scene.current_phase() == 1
    ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT, "mod": 0, "unicode": ""})
    scene.handle_event(ev)
    assert scene.current_phase() == 2


def test_left_arrow_wraps_to_phase_3():
    from cognitive_data_arcade.games.correlation_trap.scene import CorrelationTrapScene
    scene = CorrelationTrapScene()
    ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT, "mod": 0, "unicode": ""})
    scene.handle_event(ev)
    assert scene.current_phase() == 3


def test_draw_no_crash_all_phases():
    from cognitive_data_arcade.games.correlation_trap.scene import CorrelationTrapScene
    surf = pygame.display.get_surface()
    scene = CorrelationTrapScene()
    for _ in range(3):
        scene.draw(surf)
        ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT, "mod": 0, "unicode": ""})
        scene.handle_event(ev)


def test_right_arrow_wraps_from_phase_3_to_1():
    from cognitive_data_arcade.games.correlation_trap.scene import CorrelationTrapScene
    scene = CorrelationTrapScene()
    # advance to phase 3
    ev_right = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT, "mod": 0, "unicode": ""})
    scene.handle_event(ev_right)  # 1 → 2
    scene.handle_event(ev_right)  # 2 → 3
    assert scene.current_phase() == 3
    scene.handle_event(ev_right)  # 3 → 1 (wrap)
    assert scene.current_phase() == 1


def test_mouse_event_offset():
    from cognitive_data_arcade.games.correlation_trap.scene import _offset_mouse_event
    ev = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (100, 200), "button": 1})
    adjusted = _offset_mouse_event(ev, dy=-48)
    assert adjusted.pos == (100, 152)   # y reduced by 48

# tests/test_hyp_scene.py
from __future__ import annotations
import pytest
import pygame


@pytest.fixture(autouse=True)
def pg():
    pygame.init()
    pygame.display.set_mode((1024, 720))
    yield
    pygame.quit()


def _right_arrow():
    return pygame.event.Event(pygame.KEYDOWN, {
        "key": pygame.K_RIGHT, "mod": 0, "unicode": "", "scancode": 0
    })


def _left_arrow():
    return pygame.event.Event(pygame.KEYDOWN, {
        "key": pygame.K_LEFT, "mod": 0, "unicode": "", "scancode": 0
    })


def test_scene_init_no_crash():
    from cognitive_data_arcade.games.hypothesis_arena.scene import HypothesisArenaScene
    s = HypothesisArenaScene()
    assert s is not None


def test_scene_not_done_initially():
    from cognitive_data_arcade.games.hypothesis_arena.scene import HypothesisArenaScene
    s = HypothesisArenaScene()
    assert not s.is_done()


def test_right_arrow_advances_phase():
    from cognitive_data_arcade.games.hypothesis_arena.scene import HypothesisArenaScene
    s = HypothesisArenaScene()
    assert s._phase_idx == 0
    s.handle_event(_right_arrow())
    assert s._phase_idx == 1


def test_left_arrow_wraps_to_phase_3():
    from cognitive_data_arcade.games.hypothesis_arena.scene import HypothesisArenaScene
    s = HypothesisArenaScene()
    s.handle_event(_left_arrow())
    assert s._phase_idx == 2


def test_right_arrow_wraps_from_3_to_1():
    from cognitive_data_arcade.games.hypothesis_arena.scene import HypothesisArenaScene
    s = HypothesisArenaScene()
    s._phase_idx = 2
    s.handle_event(_right_arrow())
    assert s._phase_idx == 0


def test_draw_all_phases_no_crash():
    from cognitive_data_arcade.games.hypothesis_arena.scene import HypothesisArenaScene
    s = HypothesisArenaScene()
    surf = pygame.Surface((1024, 720))
    for _ in range(3):
        s.draw(surf)
        s.handle_event(_right_arrow())


def test_mouse_event_offset():
    from cognitive_data_arcade.games.hypothesis_arena.scene import HypothesisArenaScene
    s = HypothesisArenaScene()
    ev = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
        "button": 1, "pos": (100, 200), "touch": False
    })
    offset = s._offset_mouse_event(ev, dy=-48)
    assert offset.pos == (100, 200 - 48)

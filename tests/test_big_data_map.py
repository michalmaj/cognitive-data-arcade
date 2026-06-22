from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager


@pytest.fixture
def game(tmp_path):
    pygame.init()
    pm = ProfileManager(tmp_path / "profile.json")
    from cognitive_data_arcade.games.big_data_map.game import BigDataMapGame

    return BigDataMapGame(PL, pm)


@pytest.fixture
def game_with_factory(tmp_path):
    pygame.init()
    pm = ProfileManager(tmp_path / "profile.json")
    from cognitive_data_arcade.games.big_data_map.game import BigDataMapGame
    from cognitive_data_arcade.engine.scene import Scene

    navigated_to: list[int] = []

    class _FakeScene(Scene):
        def handle_event(self, event): pass
        def update(self, dt): pass
        def draw(self, surface): pass
        def is_done(self): return False
        def next_scene(self): return None

    def factory(lesson_num: int) -> Scene:
        navigated_to.append(lesson_num)
        return _FakeScene()

    g = BigDataMapGame(PL, pm, lesson_reader_factory=factory)
    return g, navigated_to


# --- concept_data tests ---

def test_concept_nodes_count() -> None:
    from cognitive_data_arcade.games.big_data_map.concept_data import CONCEPT_NODES
    assert len(CONCEPT_NODES) == 31


def test_all_modules_present() -> None:
    from cognitive_data_arcade.games.big_data_map.concept_data import CONCEPT_NODES
    modules = {n.module for n in CONCEPT_NODES}
    assert modules == {1, 2, 3, 4, 5, 6}


def test_lesson_nums_unique() -> None:
    from cognitive_data_arcade.games.big_data_map.concept_data import CONCEPT_NODES
    nums = [n.lesson_num for n in CONCEPT_NODES]
    assert len(nums) == len(set(nums))


def test_concept_edges_reference_valid_nodes() -> None:
    from cognitive_data_arcade.games.big_data_map.concept_data import CONCEPT_NODES, CONCEPT_EDGES
    valid = {n.lesson_num for n in CONCEPT_NODES}
    for a, b in CONCEPT_EDGES:
        assert a in valid, f"Edge ({a},{b}): {a} not in CONCEPT_NODES"
        assert b in valid, f"Edge ({a},{b}): {b} not in CONCEPT_NODES"


# --- BigDataMapGame state tests ---

def test_initial_selected_is_first_node(game) -> None:
    from cognitive_data_arcade.games.big_data_map.concept_data import CONCEPT_NODES
    assert game._selected == CONCEPT_NODES[0].lesson_num


def test_initial_nav_idx_is_zero(game) -> None:
    assert game._nav_idx == 0


def test_game_not_done_initially(game) -> None:
    assert game.is_done() is False


def test_next_scene_none_without_factory(game) -> None:
    assert game.next_scene() is None


def test_arrow_down_advances_selection(game) -> None:
    initial_idx = game._nav_idx
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode=""))
    assert game._nav_idx == (initial_idx + 1) % len(game._nav_order)
    assert game._selected == game._nav_order[game._nav_idx]


def test_arrow_up_retreats_selection(game) -> None:
    game._nav_idx = 5
    game._selected = game._nav_order[5]
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=0, unicode=""))
    assert game._nav_idx == 4
    assert game._selected == game._nav_order[4]


def test_arrow_wraps_around(game) -> None:
    n = len(game._nav_order)
    game._nav_idx = 0
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=0, unicode=""))
    assert game._nav_idx == n - 1


# --- Navigation with factory ---

def test_enter_without_factory_does_not_navigate(game) -> None:
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert game.is_done() is False
    assert game.next_scene() is None


def test_enter_with_factory_navigates(game_with_factory) -> None:
    game, navigated_to = game_with_factory
    selected = game._selected
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert game.is_done() is True
    assert game.next_scene() is not None
    assert navigated_to == [selected]


def test_second_click_on_selected_node_navigates(game_with_factory) -> None:
    game, navigated_to = game_with_factory
    # Select first node
    first_node = game._nav_order[0]
    game._selected = first_node
    # Get position of that node
    x, y = game._positions[first_node]
    # First click: already selected -> should navigate
    game.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(x, y)))
    assert navigated_to == [first_node]
    assert game.is_done() is True


def test_first_click_on_unselected_node_selects_it(game_with_factory) -> None:
    game, navigated_to = game_with_factory
    # Select a different node from the second one
    second_num = game._nav_order[1]
    first_num = game._nav_order[0]
    game._selected = first_num
    x, y = game._positions[second_num]
    game.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(x, y)))
    assert game._selected == second_num
    assert navigated_to == []  # no navigation, just selection


# --- Positions ---

def test_positions_cover_all_nodes() -> None:
    from cognitive_data_arcade.games.big_data_map.concept_data import CONCEPT_NODES
    from cognitive_data_arcade.games.big_data_map.game import _compute_positions
    positions = _compute_positions()
    for node in CONCEPT_NODES:
        assert node.lesson_num in positions


# --- Draw tests ---

def test_draw_without_crash(game) -> None:
    surface = pygame.Surface((1024, 768))
    game.draw(surface)


def test_draw_with_hovered_node(game) -> None:
    surface = pygame.Surface((1024, 768))
    game._hovered = game._nav_order[2]
    game.draw(surface)


def test_draw_with_selected_node(game) -> None:
    surface = pygame.Surface((1024, 768))
    game._selected = game._nav_order[5]
    game.draw(surface)

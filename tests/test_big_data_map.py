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
        def handle_event(self, event):
            pass

        def update(self, dt):
            pass

        def draw(self, surface):
            pass

        def is_done(self):
            return False

        def next_scene(self):
            return None

    def factory(lesson_num: int) -> Scene:
        navigated_to.append(lesson_num)
        return _FakeScene()

    g = BigDataMapGame(PL, pm, concept_detail_factory=factory)
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


def test_double_click_on_node_navigates(game_with_factory) -> None:
    game, navigated_to = game_with_factory
    first_node = game._nav_order[0]
    x, y = game._positions[first_node]
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(x, y))
    # First click selects; second click (within window) is the double-click
    game.handle_event(event)
    game.handle_event(event)
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


# --- DISPLAY_NUM tests ---


def test_display_num_covers_all_nodes() -> None:
    from cognitive_data_arcade.games.big_data_map.concept_data import CONCEPT_NODES, DISPLAY_NUM

    for node in CONCEPT_NODES:
        assert node.lesson_num in DISPLAY_NUM


def test_display_num_sequential_1_to_31() -> None:
    from cognitive_data_arcade.games.big_data_map.concept_data import DISPLAY_NUM

    values = sorted(DISPLAY_NUM.values())
    assert values == list(range(1, 32))


# --- get_connected tests ---


def test_get_connected_returns_at_most_5() -> None:
    from cognitive_data_arcade.games.big_data_map.concept_data import CONCEPT_NODES, get_connected

    for node in CONCEPT_NODES:
        result = get_connected(node.lesson_num)
        assert len(result) <= 5


def test_get_connected_cross_module_first() -> None:
    from cognitive_data_arcade.games.big_data_map.concept_data import get_connected, _node_map

    # Lesson 2 (RT Lab, module 1) has both intra- and cross-module connections
    result = get_connected(2, max_count=5)
    assert len(result) > 0
    src_module = _node_map[2].module
    # If any cross-module connection exists, it must come before all intra-module ones
    modules = [n.module for n, _, _ in result]
    cross_indices = [i for i, m in enumerate(modules) if m != src_module]
    intra_indices = [i for i, m in enumerate(modules) if m == src_module]
    if cross_indices and intra_indices:
        assert max(cross_indices) < min(intra_indices)


def test_get_connected_unknown_node_returns_empty() -> None:
    from cognitive_data_arcade.games.big_data_map.concept_data import get_connected

    assert get_connected(9999) == []


def test_get_connected_returns_tuples_of_three() -> None:
    from cognitive_data_arcade.games.big_data_map.concept_data import get_connected, LessonNode

    result = get_connected(1)
    for item in result:
        node, reason_pl, reason_en = item
        assert isinstance(node, LessonNode)
        assert isinstance(reason_pl, str) and len(reason_pl) > 0
        assert isinstance(reason_en, str) and len(reason_en) > 0


# --- ConceptDetailScene tests ---


def test_detail_scene_is_done_on_backspace() -> None:
    pygame.init()
    from cognitive_data_arcade.games.big_data_map.detail import ConceptDetailScene
    from cognitive_data_arcade.engine.i18n import get_strings

    scene = ConceptDetailScene(1, get_strings("en"), back_scene=None)
    assert not scene.is_done()
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, mod=0, unicode="")
    )
    assert scene.is_done()


def test_detail_scene_esc_not_handled_by_scene() -> None:
    """ESC is handled by the wrapping PausableGame, not by ConceptDetailScene itself."""
    pygame.init()
    from cognitive_data_arcade.games.big_data_map.detail import ConceptDetailScene
    from cognitive_data_arcade.engine.i18n import get_strings

    scene = ConceptDetailScene(1, get_strings("en"), back_scene=None)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert not scene.is_done()  # ESC passes through to PausableGame


def test_detail_scene_next_scene_returns_back() -> None:
    pygame.init()
    from cognitive_data_arcade.games.big_data_map.detail import ConceptDetailScene
    from cognitive_data_arcade.engine.i18n import get_strings
    from unittest.mock import MagicMock

    back = MagicMock()
    scene = ConceptDetailScene(1, get_strings("en"), back_scene=back)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, mod=0, unicode="")
    )
    assert scene.next_scene() is back


def test_detail_scene_click_closes() -> None:
    pygame.init()
    from cognitive_data_arcade.games.big_data_map.detail import ConceptDetailScene
    from cognitive_data_arcade.engine.i18n import get_strings

    scene = ConceptDetailScene(1, get_strings("en"), back_scene=None)
    scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(512, 400), button=1))
    assert scene.is_done()


def test_detail_scene_draw_without_crash() -> None:
    pygame.init()
    from cognitive_data_arcade.games.big_data_map.detail import ConceptDetailScene
    from cognitive_data_arcade.engine.i18n import get_strings

    scene = ConceptDetailScene(1, get_strings("en"), back_scene=None)
    surface = pygame.Surface((1024, 768))
    scene.draw(surface)


def test_detail_scene_shows_connections() -> None:
    pygame.init()
    from cognitive_data_arcade.games.big_data_map.detail import ConceptDetailScene
    from cognitive_data_arcade.engine.i18n import get_strings

    scene = ConceptDetailScene(2, get_strings("en"), back_scene=None)  # RT Lab has many connections
    assert len(scene._connections) > 0
    assert len(scene._connections) <= 5


# --- Session summary overlay tests ---


def test_q_key_triggers_summary(tmp_path) -> None:
    """Q key should show summary overlay, not immediately set done."""
    pygame.init()
    from cognitive_data_arcade.games.big_data_map.game import BigDataMapGame

    pm = ProfileManager(tmp_path / "profile.json")
    game = BigDataMapGame(PL, pm)
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q, mod=0, unicode="q"))
    assert game._show_summary is True
    assert not game.is_done()  # not done yet - summary is showing


def test_summary_auto_exit(tmp_path) -> None:
    """Summary becomes done after 10s timeout."""
    pygame.init()
    from cognitive_data_arcade.games.big_data_map.game import BigDataMapGame

    pm = ProfileManager(tmp_path / "profile.json")
    game = BigDataMapGame(PL, pm)
    game._show_summary = True
    game._summary_timer = 0.0
    game.update(10001)
    assert game.is_done()


def test_summary_click_fast_forwards(tmp_path) -> None:
    """Click during summary fast-forwards to done."""
    pygame.init()
    from cognitive_data_arcade.games.big_data_map.game import BigDataMapGame

    pm = ProfileManager(tmp_path / "profile.json")
    game = BigDataMapGame(PL, pm)
    game._show_summary = True
    game._summary_timer = 0.0
    game.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(512, 400)))
    assert game.is_done()


def test_summary_draw_does_not_crash(tmp_path) -> None:
    """Drawing the summary overlay should not raise."""
    pygame.init()
    from cognitive_data_arcade.games.big_data_map.game import BigDataMapGame

    pm = ProfileManager(tmp_path / "profile.json")
    game = BigDataMapGame(PL, pm)
    game._show_summary = True
    surface = pygame.Surface((1024, 768))
    game.draw(surface)

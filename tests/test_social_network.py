from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


def test_generate_random_node_count():
    from cognitive_data_arcade.games.social_network.graph import generate_random

    g = generate_random(15, 0.3, 0, 512)
    assert len(g.nodes) == 15


def test_generate_scale_free_node_count():
    from cognitive_data_arcade.games.social_network.graph import generate_scale_free

    g = generate_scale_free(15, 2, 512, 512)
    assert len(g.nodes) == 15


def test_generate_scale_free_min_edges():
    from cognitive_data_arcade.games.social_network.graph import generate_scale_free

    n, m = 10, 2
    g = generate_scale_free(n, m, 512, 512)
    assert len(g.edges) >= (n - m) * m


def test_sir_step_infection_spreads():
    from cognitive_data_arcade.games.social_network.graph import Node, Graph, sir_step

    nodes = [Node(x=0, y=0, state="I"), Node(x=1, y=0, state="S")]
    g = Graph(nodes=nodes, edges=[(0, 1)])
    g2 = sir_step(g, p_infect=1.0, p_recover=0.0)
    assert g2.nodes[1].state == "I"


def test_sir_step_recovery():
    from cognitive_data_arcade.games.social_network.graph import Node, Graph, sir_step

    nodes = [Node(x=0, y=0, state="I")]
    g = Graph(nodes=nodes, edges=[])
    g2 = sir_step(g, p_infect=0.0, p_recover=1.0)
    assert g2.nodes[0].state == "R"


def test_sir_step_pure():
    from cognitive_data_arcade.games.social_network.graph import Node, Graph, sir_step

    nodes = [Node(x=0, y=0, state="I"), Node(x=1, y=0, state="S")]
    g = Graph(nodes=nodes, edges=[(0, 1)])
    original_states = [n.state for n in g.nodes]
    _ = sir_step(g, p_infect=1.0, p_recover=0.0)
    assert [n.state for n in g.nodes] == original_states


def test_hub_node_max_degree():
    from cognitive_data_arcade.games.social_network.graph import Node, Graph, hub_node_index

    nodes = [Node(x=0, y=0, degree=1), Node(x=1, y=0, degree=4), Node(x=2, y=0, degree=2)]
    g = Graph(nodes=nodes, edges=[])
    assert hub_node_index(g) == 1


def test_game_scene_instantiates():
    from cognitive_data_arcade.games.social_network.game import SocialNetworkScene

    scene = SocialNetworkScene()
    assert scene is not None


def test_game_renders():
    import pygame
    from cognitive_data_arcade.games.social_network.game import SocialNetworkScene

    pygame.display.init()
    surface = pygame.Surface((1024, 720))
    scene = SocialNetworkScene()
    scene.draw(surface)  # must not raise


def test_add_node_limit():
    import pygame
    from cognitive_data_arcade.games.social_network.game import SocialNetworkScene

    scene = SocialNetworkScene()
    # default mode is "add_node"; fire 35 clicks inside left panel area
    for i in range(35):
        x = 50 + (i % 10) * 30
        y = 100 + (i // 10) * 30
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (x, y)})
        scene.handle_event(event)
    assert len(scene._left.nodes) <= 30


def test_add_edge_no_duplicate():
    import pygame
    from cognitive_data_arcade.games.social_network.game import SocialNetworkScene

    scene = SocialNetworkScene()
    # Add 2 nodes at known positions
    e1 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 150)})
    e2 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (200, 150)})
    scene.handle_event(e1)
    scene.handle_event(e2)
    assert len(scene._left.nodes) == 2
    # Switch to add_edge mode directly (white-box)
    scene._mode = "add_edge"
    # Try to create the same edge twice
    for _ in range(2):
        scene.handle_event(e1)  # select node 0
        scene.handle_event(e2)  # select node 1 -> create/attempt edge
    assert len(scene._left.edges) == 1


def test_menu_has_lesson_27():
    from cognitive_data_arcade.ui.menu import _LESSONS

    lesson_nums = [num for num, _ in _LESSONS]
    assert 27 in lesson_nums

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

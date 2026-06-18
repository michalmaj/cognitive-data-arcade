import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest


def test_network_configs_count():
    from cognitive_data_arcade.games.misinformation.networks import ROUNDS
    assert len(ROUNDS) == 3


def test_network_node_counts():
    from cognitive_data_arcade.games.misinformation.networks import ROUNDS
    for cfg in ROUNDS:
        assert cfg.n > 0


def test_generate_network_random():
    from cognitive_data_arcade.games.misinformation.networks import ROUNDS, build_graph
    g = build_graph(ROUNDS[0])
    assert len(g.nodes) == 15


def test_generate_network_scale_free():
    from cognitive_data_arcade.games.misinformation.networks import ROUNDS, build_graph
    g = build_graph(ROUNDS[1])
    assert len(g.nodes) == 20


def test_network_reproducible():
    from cognitive_data_arcade.games.misinformation.networks import ROUNDS, build_graph
    g1 = build_graph(ROUNDS[0])
    g2 = build_graph(ROUNDS[0])
    assert g1.edges == g2.edges


def test_game_scene_instantiates():
    import pygame
    pygame.init()
    from cognitive_data_arcade.games.misinformation.game import MisinformationScene
    scene = MisinformationScene()
    assert scene is not None
    pygame.quit()


def test_game_renders():
    import pygame
    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.misinformation.game import MisinformationScene
    scene = MisinformationScene()
    scene.draw(surface)  # must not raise
    pygame.quit()

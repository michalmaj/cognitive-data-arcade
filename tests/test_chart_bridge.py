import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface


def _make_fig() -> "matplotlib.figure.Figure":
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot([1, 2, 3], [1, 4, 9])
    return fig


def test_figure_to_surface_returns_surface() -> None:
    pygame.init()
    fig = _make_fig()
    surface = figure_to_surface(fig, (400, 300))
    assert isinstance(surface, pygame.Surface)


def test_figure_to_surface_correct_size() -> None:
    pygame.init()
    fig = _make_fig()
    surface = figure_to_surface(fig, (640, 480))
    assert surface.get_size() == (640, 480)

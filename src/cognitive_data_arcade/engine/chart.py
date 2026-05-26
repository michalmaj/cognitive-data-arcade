from __future__ import annotations

import matplotlib.pyplot as plt
import pygame
from matplotlib.figure import Figure


def figure_to_surface(fig: Figure, size: tuple[int, int]) -> pygame.Surface:
    """Render a matplotlib Figure to a pygame Surface of exactly `size` pixels.

    Closes the figure after conversion to free matplotlib memory.
    """
    dpi = fig.dpi
    fig.set_size_inches(size[0] / dpi, size[1] / dpi)
    fig.canvas.draw()
    actual_size = fig.canvas.get_width_height()
    buf = fig.canvas.buffer_rgba()
    surface = pygame.image.frombuffer(buf, actual_size, "RGBA").copy()
    plt.close(fig)
    return surface

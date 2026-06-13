from __future__ import annotations

from dataclasses import dataclass, field

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.games.feature_hunter.features import Feature
from cognitive_data_arcade.games.feature_hunter.simulator import simulate_scatter

_FIG_BG = "#0d1b2a"
_AX_BG  = "#060f1a"
_BLUE   = "#3498db"
_DIM    = (120, 120, 160)
_ORANGE = (243, 156, 18)
_WHITE  = (240, 240, 240)
_CARD_BG = (13, 27, 42)


@dataclass
class FeatureCard:
    feature: Feature
    surface: pygame.Surface
    home_rect: pygame.Rect       # original grid position (for snap-back)
    rect: pygame.Rect            # current position (moves during drag)
    assigned: str | None = None  # None | "useful" | "noise"
    dragging: bool = False
    drag_offset: tuple[int, int] = field(default_factory=lambda: (0, 0))


def grid_layout(n: int) -> tuple[int, int]:
    """Return (cols, rows) for n cards. Supports n in {4, 6, 8}."""
    mapping = {4: (2, 2), 6: (3, 2), 8: (4, 2)}
    return mapping.get(n, (n, 1))


def render_card(feature: Feature, card_w: int, card_h: int, seed: int) -> pygame.Surface:
    """Render a FeatureCard surface: label (top 24px) + scatter plot (remaining)."""
    label_h = 24
    plot_h = card_h - label_h
    dpi = 100
    fig_w_in = card_w / dpi
    fig_h_in = plot_h / dpi

    x, y = simulate_scatter(feature, n_points=60, seed=seed)

    fig, ax = plt.subplots(figsize=(fig_w_in, fig_h_in), dpi=dpi, facecolor=_FIG_BG)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.10, top=0.96)
    ax.set_facecolor(_AX_BG)
    ax.scatter(x, y, s=10, alpha=0.70, color=_BLUE)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_xlabel(feature.x_label_pl, color="#506070", fontsize=6)
    ax.set_ylabel(feature.y_label_pl, color="#506070", fontsize=6)
    ax.tick_params(colors="#506070", labelsize=5)
    for spine in ax.spines.values():
        spine.set_edgecolor("#1a2a3a")

    plot_surf = figure_to_surface(fig, (card_w, plot_h))

    # Compose: label bar on top, scatter below
    card_surf = pygame.Surface((card_w, card_h))
    card_surf.fill(_CARD_BG)
    card_surf.blit(plot_surf, (0, label_h))

    font = get_font(12)
    lbl = font.render(feature.name_pl, True, _WHITE)
    card_surf.blit(lbl, ((card_w - lbl.get_width()) // 2, (label_h - lbl.get_height()) // 2))

    return card_surf

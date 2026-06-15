# src/cognitive_data_arcade/games/word_weight_factory/step_idf.py
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.word_weight_factory.corpus import CorpusState
from cognitive_data_arcade.games.word_weight_factory.engine import WeightMatrix

_BG     = (15, 15, 35)
_DIM    = (120, 120, 160)
_AMBER  = (243, 156, 18)
_PURPLE = (155, 89, 182)
_FIG_BG = "#0f0f23"
_AX_BG  = "#1a1a3e"

_STEP_H  = 672
_W       = 804
_CHART_W = _W
_CHART_H = _STEP_H - 80   # leave room for title + insight
_DPI     = 96


def _idf_color(val: float, max_val: float) -> str:
    if max_val == 0:
        return "#7f8c8d"
    ratio = val / max_val
    if ratio > 0.6:
        return "#2ecc71"   # green = unique (high IDF)
    if ratio > 0.3:
        return "#f39c12"   # amber = mid
    return "#7f8c8d"       # grey = common (low IDF)


class StepIdfScene(Scene):
    def __init__(self, state: CorpusState) -> None:
        self._state = state
        self._done = False
        self._chart_surf: pygame.Surface | None = None
        self._cached_key: tuple | None = None
        self._selected_tok: str | None = None

    def _chart_key(self, matrix: WeightMatrix) -> tuple:
        return (tuple(matrix.vocab), tuple(matrix.idf))

    def handle_event(self, event: pygame.event.Event) -> None:
        pass  # bar clicks: not implemented (chart is image)

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return None

    def draw(self, surface: pygame.Surface, matrix: WeightMatrix | None = None) -> None:
        surface.fill(_BG)
        if matrix is None or not matrix.vocab:
            msg = get_font(12).render("Brak tokenow.", True, _DIM)
            surface.blit(msg, (8, 8))
            return

        t = get_font(12).render("IDF — rzadkosc tokenow w korpusie", True, _AMBER)
        surface.blit(t, (8, 6))

        key = self._chart_key(matrix)
        if key != self._cached_key:
            self._chart_surf = _render_idf_chart(matrix)
            self._cached_key = key

        if self._chart_surf:
            surface.blit(self._chart_surf, (0, 28))

        # Insight
        if matrix.idf:
            min_idf_j = matrix.idf.index(min(matrix.idf))
            min_tok   = matrix.vocab[min_idf_j]
            insight = (f"IDF karze za popularnosc -- '{min_tok}' jest pospolite"
                       f" (IDF={matrix.idf[min_idf_j]:.2f}). Slowa unikalne maja wysoki IDF.")
        else:
            insight = "IDF karze za popularnosc -- slowa wspolne dla wielu dok maja niski IDF."
        iy = _STEP_H - 40
        pygame.draw.rect(surface, (20, 15, 35), (0, iy - 6, _W, 46))
        pygame.draw.line(surface, _PURPLE, (0, iy - 6), (0, iy + 40), 3)
        ins = get_font(11).render(insight[:115], True, (200, 180, 220))
        surface.blit(ins, (8, iy + 4))


def _render_idf_chart(matrix: WeightMatrix) -> pygame.Surface:
    pairs = sorted(zip(matrix.idf, matrix.vocab), reverse=True)
    idf_vals = [v for v, _ in pairs]
    tokens   = [t for _, t in pairs]
    max_val  = max(idf_vals, default=1) or 1
    colors   = [_idf_color(v, max_val) for v in idf_vals]

    fig, ax = plt.subplots(
        facecolor=_FIG_BG,
        figsize=(_CHART_W / _DPI, _CHART_H / _DPI),
        dpi=_DPI,
    )
    ax.set_facecolor(_AX_BG)
    y_pos = range(len(tokens))
    ax.barh(list(y_pos), idf_vals, color=colors, edgecolor="none")
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(tokens, color="#c8c8d8", fontsize=8)
    ax.set_xlabel("IDF = log((N+1)/(df+1))", color="#787890", fontsize=8)
    ax.tick_params(colors="#787890", labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#2a2a50")
    ax.invert_yaxis()
    ax.set_title("Zielony = unikalne  |  Szary = pospolite", color="#787890", fontsize=8, pad=3)
    fig.tight_layout(pad=0.5)
    surf = figure_to_surface(fig, (_CHART_W, _CHART_H))
    # Note: figure_to_surface already closes the figure internally
    return surf

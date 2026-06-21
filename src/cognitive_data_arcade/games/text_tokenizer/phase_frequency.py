# src/cognitive_data_arcade/games/text_tokenizer/phase_frequency.py
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerState
from cognitive_data_arcade.games.text_tokenizer.stop_words import STOP_WORDS_EN, STOP_WORDS_PL
from cognitive_data_arcade.games.text_tokenizer.widgets import SharedState

_BG = (15, 15, 35)
_FIG_BG = "#0f0f23"
_AX_BG = "#1a1a3e"
_PANEL = (18, 18, 42)
_WHITE = (240, 240, 240)
_DIM = (120, 120, 160)
_AMBER = (243, 156, 18)
_GREEN = (46, 204, 113)
_PURPLE = (155, 89, 182)
_LEFT_W = 220
_PHASE_H = 636
_CHART_W = 1024 - _LEFT_W - 8
_CHART_H = _PHASE_H - 60
_DPI = 96


class PhaseFrequencyScene(Scene):
    def __init__(self, state: SharedState) -> None:
        self._state = state
        self._done = False
        self._chart_surf: pygame.Surface | None = None
        self._cached_key: tuple | None = None

        self._slider_rect = pygame.Rect(8, 60, _LEFT_W - 16, 20)
        self._dragging_slider = False
        self._checkbox_rect = pygame.Rect(8, 110, 16, 16)

    def _chart_key(self, result: TokenizerState) -> tuple:
        return (
            tuple(result.freq.items()),
            self._state.topn,
            self._state.show_stops_in_chart,
            self._state.lang,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._checkbox_rect.collidepoint(event.pos):
                self._state.show_stops_in_chart = not self._state.show_stops_in_chart
                return
            if self._slider_rect.collidepoint(event.pos):
                self._dragging_slider = True
                self._update_slider(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self._dragging_slider = False
        elif event.type == pygame.MOUSEMOTION and self._dragging_slider:
            self._update_slider(event.pos[0])

    def _update_slider(self, px: int) -> None:
        ratio = (px - self._slider_rect.x) / max(1, self._slider_rect.w)
        ratio = max(0.0, min(1.0, ratio))
        self._state.topn = 5 + round(ratio * 15)

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return None

    def draw(self, surface: pygame.Surface, result: TokenizerState | None = None) -> None:  # type: ignore[override]
        if result is None:
            return
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _LEFT_W, _PHASE_H))

        hdr = get_font(12).render("KONTROLKI", True, _PURPLE)
        surface.blit(hdr, (8, 12))

        # Top-N slider
        topn_lbl = get_font(12).render(f"Top N: {self._state.topn}", True, _WHITE)
        surface.blit(topn_lbl, (8, 38))
        pygame.draw.rect(surface, (42, 42, 80), self._slider_rect, border_radius=2)
        ratio = (self._state.topn - 5) / 15.0
        filled_w = int(ratio * self._slider_rect.w)
        if filled_w > 0:
            pygame.draw.rect(
                surface,
                _AMBER,
                (self._slider_rect.x, self._slider_rect.y, filled_w, self._slider_rect.h),
                border_radius=2,
            )
        thumb_x = self._slider_rect.x + filled_w
        pygame.draw.circle(surface, _AMBER, (thumb_x, self._slider_rect.centery), 7)

        # Show stop words checkbox
        pygame.draw.rect(surface, (30, 30, 55), self._checkbox_rect, border_radius=2)
        pygame.draw.rect(surface, _AMBER, self._checkbox_rect, 1, border_radius=2)
        if self._state.show_stops_in_chart:
            pygame.draw.line(
                surface,
                _AMBER,
                (self._checkbox_rect.x + 2, self._checkbox_rect.centery),
                (self._checkbox_rect.centerx, self._checkbox_rect.bottom - 2),
                2,
            )
            pygame.draw.line(
                surface,
                _AMBER,
                (self._checkbox_rect.centerx, self._checkbox_rect.bottom - 2),
                (self._checkbox_rect.right - 2, self._checkbox_rect.y + 2),
                2,
            )
        chk_lbl = get_font(11).render("Pokaz stop words", True, _DIM)
        surface.blit(chk_lbl, (self._checkbox_rect.right + 6, self._checkbox_rect.y))

        # Stats
        y = 145
        pygame.draw.line(surface, (40, 40, 70), (8, y), (_LEFT_W - 8, y))
        y += 10
        if result.freq:
            top_tok = next(iter(result.freq))
            top_cnt = result.freq[top_tok]
            hapax = sum(1 for v in result.freq.values() if v == 1)
            for label, val, col in [
                ("Najczestszy:", f'"{top_tok}" ({top_cnt}x)', _AMBER),
                ("Unikalnych:", str(len(result.freq)), _WHITE),
                ("Hapax legomena:", str(hapax), _DIM),
            ]:
                lbl_s = get_font(11).render(label, True, _DIM)
                val_s = get_font(11).render(val, True, col)
                surface.blit(lbl_s, (8, y))
                y += 18
                surface.blit(val_s, (8, y))
                y += 22
        hapax_hint = get_font(10).render("Hapax = token jednorazowy", True, (70, 70, 100))
        surface.blit(hapax_hint, (8, y))

        # Chart (right panel) — cached
        key = self._chart_key(result)
        if key != self._cached_key:
            self._chart_surf = _render_chart(result, self._state)
            self._cached_key = key
        if self._chart_surf:
            surface.blit(self._chart_surf, (_LEFT_W + 4, 10))

        # Insight banner
        insight = self._make_insight(result)
        iy = _PHASE_H - 40
        pygame.draw.rect(surface, (20, 15, 35), (0, iy - 6, 1024, 46))
        pygame.draw.line(surface, _PURPLE, (0, iy - 6), (0, iy + 40), 3)
        ins_s = get_font(11).render(insight[:115], True, (200, 180, 220))
        surface.blit(ins_s, (8, iy + 4))

    def _make_insight(self, result: TokenizerState) -> str:
        vals = list(result.freq.values())
        if len(vals) >= 2 and vals[0] >= 2 * vals[1]:
            return (
                "Prawo Zipfa: najczestszy token pojawia sie ~2x czesciej "
                "niz drugi — nawet w krotkich tekstach."
            )
        return (
            "Prawo Zipfa: czestotliwosc tokenow spada bardzo szybko. "
            "Kilka tokenow dominuje, reszta to hapax legomena."
        )


def _render_chart(result: TokenizerState, state: SharedState) -> pygame.Surface:
    stops = STOP_WORDS_PL if state.lang == "pl" else STOP_WORDS_EN

    items = list(result.freq.items())
    if not state.show_stops_in_chart:
        items = [(t, c) for t, c in items if t.lower() not in stops]
    items = items[: state.topn]

    if not items:
        items = [("(brak tokenow)", 0)]

    tokens = [t for t, _ in items]
    counts = [c for _, c in items]
    colors = ["#7f8c8d" if t.lower() in stops else "#2ecc71" for t in tokens]

    fig, ax = plt.subplots(
        facecolor=_FIG_BG,
        figsize=(_CHART_W / _DPI, _CHART_H / _DPI),
        dpi=_DPI,
    )
    ax.set_facecolor(_AX_BG)
    y_pos = range(len(tokens))
    ax.barh(list(y_pos), counts, color=colors, edgecolor="none")
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(tokens, color="#c8c8d8", fontsize=8)
    ax.set_xlabel("Czestotliwosc", color="#787890", fontsize=8)
    ax.tick_params(colors="#787890", labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#2a2a50")
    if max(counts, default=0) > 0:
        ax.axvline(x=1, color="#3a3a6a", linestyle="--", linewidth=0.8)
    ax.invert_yaxis()
    ax.set_title(f"Top {state.topn} tokenow", color="#787890", fontsize=9, pad=4)
    fig.tight_layout(pad=0.5)
    surf = figure_to_surface(fig, (_CHART_W, _CHART_H))
    plt.close(fig)
    return surf

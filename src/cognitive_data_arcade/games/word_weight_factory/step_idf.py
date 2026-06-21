# src/cognitive_data_arcade/games/word_weight_factory/step_idf.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.engine.scrollbar import ScrollBar
from cognitive_data_arcade.games.word_weight_factory.corpus import CorpusState
from cognitive_data_arcade.games.word_weight_factory.engine import WeightMatrix

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
    GREEN as _GREEN,
    PURPLE as _PURPLE,
)

_PANEL = (18, 18, 42)
_AMBER = (243, 156, 18)
_GREY = (90, 90, 120)

_STEP_H = 672
_W = 804
_TITLE_H = 28
_INSIGHT_H = 46
_CHART_Y = _TITLE_H
_CHART_H = _STEP_H - _TITLE_H - _INSIGHT_H  # 598 px visible

_BAR_ROW = 24  # px per token row
_LABEL_W = 165  # token label column
_BAR_MAX = 560  # max bar pixel width
_VAL_X = _LABEL_W + _BAR_MAX + 6  # IDF value text x
_SB_W = 8
_SB_X = _W - _SB_W - 4
_SB_MARGIN = 4  # gap between bar area and scrollbar

_TOOLTIP_W = 300
_TOOLTIP_PAD = 8
_TOOLTIP_LINE = 18


def _bar_color(ratio: float) -> tuple[int, int, int]:
    if ratio > 0.6:
        return _GREEN
    if ratio > 0.3:
        return _AMBER
    return _GREY


class StepIdfScene(Scene):
    def __init__(self, state: CorpusState) -> None:
        self._state = state
        self._done = False
        self._sb = ScrollBar(
            total=0,
            visible=_CHART_H,
            x=_SB_X,
            y=_CHART_Y,
            h=_CHART_H,
            width=_SB_W,
        )
        self._pairs: list[tuple[float, str, int]] = []  # (idf, tok, df_count)
        self._n_docs: int = 0
        self._max_idf: float = 1.0
        self._cached_key: tuple | None = None
        self._tooltip: list[str] | None = None
        self._tooltip_pos: tuple[int, int] = (0, 0)

    # ------------------------------------------------------------------
    def _rebuild(self, matrix: WeightMatrix) -> None:
        key = (tuple(matrix.vocab), tuple(matrix.idf))
        if key == self._cached_key:
            return
        self._cached_key = key
        N = len(matrix.doc_titles)
        V = len(matrix.vocab)
        df = [sum(1 for i in range(N) if matrix.bow[i][j] > 0) for j in range(V)]
        pairs = sorted(
            zip(matrix.idf, matrix.vocab, df),
            key=lambda x: x[0],
            reverse=True,
        )
        self._pairs = list(pairs)
        self._n_docs = N
        self._max_idf = max((v for v, _, _ in self._pairs), default=1.0) or 1.0
        self._sb.set_total(len(self._pairs) * _BAR_ROW)
        self._tooltip = None

    # ------------------------------------------------------------------
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEWHEEL:
            self._sb.handle_wheel(-event.y * 3)
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self._sb.handle_mousedown(event.pos):
                    return
                self._tooltip = None
            if event.button == 3:
                self._open_tooltip(event.pos)
        if event.type == pygame.MOUSEMOTION:
            self._sb.handle_mousemotion(event.pos, pygame.mouse.get_pressed())
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._tooltip = None

    def _open_tooltip(self, pos: tuple[int, int]) -> None:
        px, py = pos
        if px < 0 or px >= _W:
            return
        # Is click inside chart area?
        if not (_CHART_Y <= py < _CHART_Y + _CHART_H):
            return
        rel_y = py - _CHART_Y + self._sb.scroll
        row = rel_y // _BAR_ROW
        if not (0 <= row < len(self._pairs)):
            # Right-click on empty space below bars → formula tooltip
            self._tooltip = [
                "IDF — Inverse Document Frequency",
                "",
                "Wzor: IDF(t) = log((N+1) / (df(t)+1))",
                "",
                "N   = liczba dokumentow w korpusie",
                "df  = ile dok zawiera ten token",
                "",
                "Wysoki IDF → token rzadki → wazny",
                "Niski IDF  → token pospolity → mniej wazny",
            ]
            self._tooltip_pos = pos
            return
        idf_val, tok, df_val = self._pairs[row]
        N = self._n_docs
        if df_val == N:
            uniqueness = "we wszystkich dok — pospolity"
        elif df_val == 1:
            uniqueness = "tylko w 1 dok — bardzo unikalne"
        else:
            uniqueness = f"w {df_val} z {N} dok"
        self._tooltip = [
            f'Token: "{tok}"',
            "",
            f"IDF  = {idf_val:.4f}",
            f"df   = {df_val} ({uniqueness})",
            "",
            f"IDF = log(({N}+1) / ({df_val}+1))",
            "",
            "Zielony = rzadki (wysoki IDF)",
            "Szary   = pospolity (niski IDF)",
        ]
        self._tooltip_pos = pos

    # ------------------------------------------------------------------
    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return None

    # ------------------------------------------------------------------
    def draw(self, surface: pygame.Surface, matrix: WeightMatrix | None = None) -> None:
        surface.fill(_BG)
        if matrix is None or not matrix.vocab:
            msg = get_font(12).render("Brak tokenow.", True, _DIM)
            surface.blit(msg, (8, 8))
            return

        self._rebuild(matrix)

        # ── Title ──────────────────────────────────────────────────────
        font12 = get_font(12)
        t = font12.render("IDF — rzadkosc tokenow w korpusie", True, _AMBER)
        surface.blit(t, (8, 6))
        hint = get_font(10).render("PPM = opis   |   kolko = scroll", True, _DIM)
        surface.blit(hint, (_W - hint.get_width() - _SB_W - 10, 8))

        # ── Chart clip region ──────────────────────────────────────────
        clip = pygame.Rect(0, _CHART_Y, _W, _CHART_H)
        surface.set_clip(clip)

        scroll = self._sb.scroll
        font9 = get_font(9)

        for idx, (idf_val, tok, _df) in enumerate(self._pairs):
            row_y = _CHART_Y + idx * _BAR_ROW - scroll
            if row_y + _BAR_ROW < _CHART_Y:
                continue
            if row_y >= _CHART_Y + _CHART_H:
                break

            ratio = idf_val / self._max_idf
            bar_px = max(2, round(ratio * _BAR_MAX))
            color = _bar_color(ratio)

            # Row background (alternating)
            row_bg = (17, 17, 38) if idx % 2 == 0 else _BG
            pygame.draw.rect(surface, row_bg, (0, row_y, _SB_X - _SB_MARGIN, _BAR_ROW))

            # Token label (right-aligned in label column)
            label_text = tok if len(tok) <= 18 else tok[:17] + "…"
            lbl = font9.render(label_text, True, _WHITE)
            surface.blit(
                lbl, (_LABEL_W - lbl.get_width() - 4, row_y + (_BAR_ROW - lbl.get_height()) // 2)
            )

            # Bar
            bar_rect = pygame.Rect(_LABEL_W, row_y + 4, bar_px, _BAR_ROW - 8)
            pygame.draw.rect(surface, color, bar_rect, border_radius=2)

            # IDF value text
            val_lbl = font9.render(f"{idf_val:.3f}", True, _DIM)
            surface.blit(
                val_lbl, (_LABEL_W + bar_px + 4, row_y + (_BAR_ROW - val_lbl.get_height()) // 2)
            )

            # Row separator
            pygame.draw.line(
                surface,
                (30, 30, 55),
                (0, row_y + _BAR_ROW - 1),
                (_SB_X - _SB_MARGIN, row_y + _BAR_ROW - 1),
            )

        # x-axis grid lines (faint verticals at 25% intervals)
        for frac in (0.25, 0.5, 0.75, 1.0):
            gx = _LABEL_W + round(frac * _BAR_MAX)
            pygame.draw.line(surface, (30, 30, 58), (gx, _CHART_Y), (gx, _CHART_Y + _CHART_H))

        surface.set_clip(None)

        # ── Scrollbar ─────────────────────────────────────────────────
        self._sb.draw(surface)

        # ── Insight banner ────────────────────────────────────────────
        if self._pairs:
            min_tok = self._pairs[-1][1]
            min_idf = self._pairs[-1][0]
            max_tok = self._pairs[0][1]
            max_idf = self._pairs[0][0]
            insight = (
                f"'{max_tok}' jest unikalne (IDF={max_idf:.2f})."
                f"  '{min_tok}' jest pospolite (IDF={min_idf:.2f})."
                f"  PPM na pasku = szczegoly."
            )
        else:
            insight = "IDF karze za popularnosc — slowa wspolne maja niski IDF."
        iy = _STEP_H - 40
        pygame.draw.rect(surface, (20, 15, 35), (0, iy - 6, _W, 46))
        pygame.draw.line(surface, _PURPLE, (0, iy - 6), (0, iy + 40), 3)
        ins = get_font(11).render(insight[:115], True, (200, 180, 220))
        surface.blit(ins, (8, iy + 4))

        # ── Tooltip ───────────────────────────────────────────────────
        if self._tooltip:
            self._draw_tooltip(surface)

    def _draw_tooltip(self, surface: pygame.Surface) -> None:
        lines = self._tooltip
        if not lines:
            return
        font10 = get_font(10)
        n_lines = len(lines)
        box_h = n_lines * _TOOLTIP_LINE + _TOOLTIP_PAD * 2
        tx, ty = self._tooltip_pos
        # Keep tooltip inside the surface
        if tx + _TOOLTIP_W > _W:
            tx = _W - _TOOLTIP_W - 4
        if ty + box_h > _STEP_H - _INSIGHT_H:
            ty = max(0, _STEP_H - _INSIGHT_H - box_h - 4)

        bg_rect = pygame.Rect(tx, ty, _TOOLTIP_W, box_h)
        pygame.draw.rect(surface, (12, 12, 30), bg_rect, border_radius=4)
        pygame.draw.rect(surface, _PURPLE, bg_rect, 1, border_radius=4)

        for i, line in enumerate(lines):
            if line == "":
                continue
            col = _AMBER if i == 0 else (_DIM if line.startswith("Wzor") or "=" in line else _WHITE)
            s = font10.render(line, True, col)
            surface.blit(s, (tx + _TOOLTIP_PAD, ty + _TOOLTIP_PAD + i * _TOOLTIP_LINE))

# src/cognitive_data_arcade/games/word_weight_factory/step_bow.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.word_weight_factory.corpus import CorpusState
from cognitive_data_arcade.games.word_weight_factory.engine import WeightMatrix

_BG     = (15, 15, 35)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_AMBER  = (243, 156, 18)
_GREEN  = (46, 204, 113)
_PURPLE = (155, 89, 182)

_STEP_H  = 672
_W       = 804
_LABEL_W = 100
_COL_W   = 36
_ROW_H   = 30
_HDR_H   = 28
_MAX_COLS = 19


def _green_cell(value: float, max_val: float) -> tuple[int, int, int]:
    if max_val == 0:
        return (20, 20, 38)
    ratio = min(1.0, value / max_val)
    r = int(20 + ratio * (46 - 20))
    g = int(20 + ratio * (204 - 20))
    b = int(38 + ratio * (30 - 38))
    return (r, g, b)


class StepBowScene(Scene):
    def __init__(self, state: CorpusState) -> None:
        self._state = state
        self._done = False
        self._selected_col: int | None = None
        self._selected_cell: tuple[int, int] | None = None  # (row, col)
        self._col_offset = 0  # horizontal scroll

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEWHEEL:
            self._col_offset = max(0, self._col_offset - event.x - event.y)
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        pos = event.pos
        # Column header click
        hdr_y = 28
        for ci in range(_MAX_COLS):
            x0 = _LABEL_W + ci * _COL_W
            rect = pygame.Rect(x0, hdr_y, _COL_W, _HDR_H)
            if rect.collidepoint(pos):
                col_idx = self._col_offset + ci
                self._selected_col = col_idx if self._selected_col != col_idx else None
                self._selected_cell = None
                return
        # Cell click
        for ri in range(20):
            for ci in range(_MAX_COLS):
                x0 = _LABEL_W + ci * _COL_W
                y0 = 28 + _HDR_H + ri * _ROW_H
                rect = pygame.Rect(x0, y0, _COL_W, _ROW_H)
                if rect.collidepoint(pos):
                    self._selected_cell = (ri, self._col_offset + ci)
                    self._selected_col = None
                    return

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return None

    def draw(self, surface: pygame.Surface, matrix: WeightMatrix | None = None) -> None:
        surface.fill(_BG)
        if matrix is None or not matrix.vocab:
            msg = get_font(12).render("Brak tokenow — zmien ustawienia.", True, _DIM)
            surface.blit(msg, (8, 8))
            return

        V = len(matrix.vocab)
        N = len(matrix.doc_titles)
        max_val = max((matrix.bow[i][j] for i in range(N) for j in range(V)), default=1) or 1

        # Title
        t = get_font(12).render("BoW — surowe zliczenia tokenow", True, _AMBER)
        surface.blit(t, (8, 6))

        visible_start = self._col_offset
        visible_end = min(V, visible_start + _MAX_COLS)
        visible_cols = list(range(visible_start, visible_end))

        font9  = get_font(9)
        font11 = get_font(11)

        # Column headers
        hdr_y = 28
        for ci, j in enumerate(visible_cols):
            x0 = _LABEL_W + ci * _COL_W
            label = matrix.vocab[j][:6]
            active_col = j == self._selected_col
            bg = (40, 30, 10) if active_col else (20, 20, 38)
            pygame.draw.rect(surface, bg, (x0, hdr_y, _COL_W, _HDR_H))
            pygame.draw.line(surface, (40, 40, 70), (x0, hdr_y), (x0, hdr_y + _HDR_H))
            ls = font9.render(label, True, _AMBER if active_col else _DIM)
            surface.blit(ls, (x0 + (_COL_W - ls.get_width()) // 2,
                               hdr_y + (_HDR_H - ls.get_height()) // 2))

        # Rows
        for ri in range(N):
            y0 = 28 + _HDR_H + ri * _ROW_H
            active_row = ri == self._state.selected_idx
            row_bg = (25, 22, 10) if active_row else _BG
            pygame.draw.rect(surface, row_bg, (0, y0, _W, _ROW_H))
            # Row label
            rl = font9.render(matrix.doc_titles[ri][:13], True, _AMBER if active_row else _DIM)
            surface.blit(rl, (4, y0 + (_ROW_H - rl.get_height()) // 2))
            # Cells
            for ci, j in enumerate(visible_cols):
                x0 = _LABEL_W + ci * _COL_W
                val = matrix.bow[ri][j]
                active_cell = self._selected_cell == (ri, j)
                active_col_h = j == self._selected_col
                cell_bg = (50, 40, 5) if active_cell else \
                          (35, 28, 5) if active_col_h else \
                          _green_cell(val, max_val)
                pygame.draw.rect(surface, cell_bg, (x0 + 1, y0 + 1, _COL_W - 2, _ROW_H - 2))
                pygame.draw.line(surface, (30, 30, 55), (x0, y0), (x0, y0 + _ROW_H))
                pygame.draw.line(surface, (30, 30, 55), (x0, y0), (_LABEL_W + len(visible_cols) * _COL_W, y0))
                vs = font9.render(str(val), True, _WHITE if val > 0 else _DIM)
                surface.blit(vs, (x0 + (_COL_W - vs.get_width()) // 2,
                                   y0 + (_ROW_H - vs.get_height()) // 2))
            pygame.draw.line(surface, (30, 30, 55), (0, y0 + _ROW_H),
                             (_LABEL_W + len(visible_cols) * _COL_W, y0 + _ROW_H))

        # Scroll hint
        if V > _MAX_COLS:
            sh = font9.render(f"Kolumny {visible_start+1}-{visible_end}/{V}  (scroll)", True, _DIM)
            surface.blit(sh, (_W - sh.get_width() - 8, 8))

        # Selected cell detail
        detail_y = 28 + _HDR_H + N * _ROW_H + 8
        if self._selected_cell is not None:
            ri, j = self._selected_cell
            if ri < N and j < V:
                tok = matrix.vocab[j]
                cnt = matrix.bow[ri][j]
                dtitle = matrix.doc_titles[ri]
                detail = f'"{tok}" w "{dtitle}": {cnt}x'
                ds = font11.render(detail, True, _AMBER)
                surface.blit(ds, (8, detail_y))
        elif self._selected_col is not None and self._selected_col < V:
            tok = matrix.vocab[self._selected_col]
            detail = f'Token "{tok}" — zaznaczony w calej macierzy'
            ds = font11.render(detail, True, _AMBER)
            surface.blit(ds, (8, detail_y))

        # Insight banner
        insight = ("BoW = surowe zliczenia. Dlugi dokument dostaje duze liczby"
                   " -- dlatego potrzebujemy normalizacji.")
        iy = _STEP_H - 40
        pygame.draw.rect(surface, (20, 15, 35), (0, iy - 6, _W, 46))
        pygame.draw.line(surface, _PURPLE, (0, iy - 6), (0, iy + 40), 3)
        ins = get_font(11).render(insight, True, (200, 180, 220))
        surface.blit(ins, (8, iy + 4))

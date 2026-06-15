# src/cognitive_data_arcade/games/word_weight_factory/step_tf.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.word_weight_factory.corpus import CorpusState
from cognitive_data_arcade.games.word_weight_factory.engine import WeightMatrix
from cognitive_data_arcade.games.word_weight_factory.step_bow import (
    _BG, _WHITE, _DIM, _AMBER, _GREEN, _PURPLE,
    _STEP_H, _W, _LABEL_W, _COL_W, _ROW_H, _HDR_H, _MAX_COLS,
    _green_cell,
)


class StepTfScene(Scene):
    def __init__(self, state: CorpusState) -> None:
        self._state = state
        self._done = False
        self._selected_cell: tuple[int, int] | None = None
        self._col_offset = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEWHEEL:
            self._col_offset = max(0, self._col_offset - event.x - event.y)
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        pos = event.pos
        for ri in range(20):
            for ci in range(_MAX_COLS):
                x0 = _LABEL_W + ci * _COL_W
                y0 = 52 + _HDR_H + ri * _ROW_H
                if pygame.Rect(x0, y0, _COL_W, _ROW_H).collidepoint(pos):
                    self._selected_cell = (ri, self._col_offset + ci)
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
            msg = get_font(12).render("Brak tokenow.", True, _DIM)
            surface.blit(msg, (8, 8))
            return

        V = len(matrix.vocab)
        N = len(matrix.doc_titles)
        max_tf = max((matrix.tf[i][j] for i in range(N) for j in range(V)), default=1) or 1

        # Title + formula
        t = get_font(12).render("TF — czestotliwosc terminu (znormalizowana)", True, _AMBER)
        surface.blit(t, (8, 6))
        formula = get_font(11).render("TF(t, d) = count(t, d) / |d|", True, _DIM)
        surface.blit(formula, (8, 26))

        visible_start = self._col_offset
        visible_end   = min(V, visible_start + _MAX_COLS)
        visible_cols  = list(range(visible_start, visible_end))

        font9 = get_font(9)
        HDR_TOP = 52  # shifted down because of formula line

        # Column headers
        for ci, j in enumerate(visible_cols):
            x0 = _LABEL_W + ci * _COL_W
            label = matrix.vocab[j][:6]
            pygame.draw.rect(surface, (20, 20, 38), (x0, HDR_TOP, _COL_W, _HDR_H))
            pygame.draw.line(surface, (40, 40, 70), (x0, HDR_TOP), (x0, HDR_TOP + _HDR_H))
            ls = font9.render(label, True, _DIM)
            surface.blit(ls, (x0 + (_COL_W - ls.get_width()) // 2,
                               HDR_TOP + (_HDR_H - ls.get_height()) // 2))

        # Rows
        for ri in range(N):
            y0 = HDR_TOP + _HDR_H + ri * _ROW_H
            active_row = ri == self._state.selected_idx
            pygame.draw.rect(surface, (25, 22, 10) if active_row else _BG, (0, y0, _W, _ROW_H))
            rl = font9.render(matrix.doc_titles[ri][:13], True, _AMBER if active_row else _DIM)
            surface.blit(rl, (4, y0 + (_ROW_H - rl.get_height()) // 2))
            for ci, j in enumerate(visible_cols):
                x0 = _LABEL_W + ci * _COL_W
                val = matrix.tf[ri][j]
                active_cell = self._selected_cell == (ri, j)
                cell_bg = (50, 40, 5) if active_cell else _green_cell(val, max_tf)
                pygame.draw.rect(surface, cell_bg, (x0 + 1, y0 + 1, _COL_W - 2, _ROW_H - 2))
                pygame.draw.line(surface, (30, 30, 55), (x0, y0), (x0, y0 + _ROW_H))
                vs = font9.render(f"{val:.2f}", True, _WHITE if val > 0 else _DIM)
                surface.blit(vs, (x0 + (_COL_W - vs.get_width()) // 2,
                                   y0 + (_ROW_H - vs.get_height()) // 2))
            pygame.draw.line(surface, (30, 30, 55), (0, y0 + _ROW_H),
                             (_LABEL_W + len(visible_cols) * _COL_W, y0 + _ROW_H))

        if V > _MAX_COLS:
            sh = font9.render(f"Kolumny {visible_start+1}-{visible_end}/{V}  (scroll)", True, _DIM)
            surface.blit(sh, (_W - sh.get_width() - 8, 8))

        # Selected cell detail
        detail_y = HDR_TOP + _HDR_H + N * _ROW_H + 8
        if self._selected_cell is not None:
            ri, j = self._selected_cell
            if ri < N and j < V:
                tok = matrix.vocab[j]
                cnt = matrix.bow[ri][j]
                doc_len = max(1, sum(matrix.bow[ri]))
                tf_val  = matrix.tf[ri][j]
                dtitle  = matrix.doc_titles[ri]
                detail  = f'"{tok}" w "{dtitle}": TF = {cnt}/{doc_len} = {tf_val:.3f}'
                ds = get_font(11).render(detail, True, _AMBER)
                surface.blit(ds, (8, detail_y))

        insight = "TF normalizuje przez dlugosc dokumentu. Dlugie i krotkie teksty sa teraz porownywalnie."
        iy = _STEP_H - 40
        pygame.draw.rect(surface, (20, 15, 35), (0, iy - 6, _W, 46))
        pygame.draw.line(surface, _PURPLE, (0, iy - 6), (0, iy + 40), 3)
        ins = get_font(11).render(insight, True, (200, 180, 220))
        surface.blit(ins, (8, iy + 4))

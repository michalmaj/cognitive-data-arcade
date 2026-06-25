# src/cognitive_data_arcade/games/word_weight_factory/step_bow.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.word_weight_factory.corpus import CorpusState
from cognitive_data_arcade.games.word_weight_factory.engine import WeightMatrix

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
    PURPLE as _PURPLE,
)

_AMBER = (243, 156, 18)

_STEP_H = 672
_W = 804
_LABEL_W = 100
_COL_W = 36
_ROW_H = 30
_HDR_H = 28
_MAX_COLS = 19

_TOOLTIP_W = 300
_TOOLTIP_PAD = 8
_TOOLTIP_LINE = 18


def _draw_tooltip_box(surface: pygame.Surface, lines: list[str], pos: tuple[int, int]) -> None:
    bh = len(lines) * _TOOLTIP_LINE + _TOOLTIP_PAD * 2
    sw, sh = surface.get_size()
    tx = max(4, min(pos[0], sw - _TOOLTIP_W - 4))
    ty = max(4, min(pos[1], sh - bh - 4))
    r = pygame.Rect(tx, ty, _TOOLTIP_W, bh)
    pygame.draw.rect(surface, (12, 12, 30), r, border_radius=4)
    pygame.draw.rect(surface, _PURPLE, r, 1, border_radius=4)
    font10 = get_font(10)
    for i, line in enumerate(lines):
        if not line:
            continue
        col = _AMBER if i == 0 else _WHITE
        s = font10.render(line, True, col)
        surface.blit(s, (tx + _TOOLTIP_PAD, ty + _TOOLTIP_PAD + i * _TOOLTIP_LINE))


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
        self._tooltip: list[str] | None = None
        self._tooltip_pos: tuple[int, int] = (0, 0)
        self._last_matrix: WeightMatrix | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEWHEEL:
            self._col_offset = max(0, self._col_offset - event.x - event.y)
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        pos = event.pos
        if event.button == 3:
            self._open_tooltip(pos)
            return
        if event.button != 1:
            return
        self._tooltip = None
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

    def _open_tooltip(self, pos: tuple[int, int]) -> None:
        px, py = pos
        if px < 0 or px >= _W:
            return
        m = self._last_matrix
        hdr_y = 28
        iy = _STEP_H - 40
        # Insight banner
        if py >= iy - 6:
            self._tooltip = [
                "Bag of Words — spostrzezenie",
                "",
                "BoW ignoruje kolejnosc slow.",
                "Dlugie dokumenty maja wyzsze",
                "wartosci — stad potrzeba TF.",
            ]
            self._tooltip_pos = pos
            return
        # Column header zone
        if hdr_y <= py < hdr_y + _HDR_H and m is not None:
            for ci in range(_MAX_COLS):
                x0 = _LABEL_W + ci * _COL_W
                if x0 <= px < x0 + _COL_W:
                    j = self._col_offset + ci
                    if j < len(m.vocab):
                        tok = m.vocab[j]
                        N = len(m.doc_titles)
                        V = len(m.vocab)
                        total = sum(m.bow[i][j] for i in range(N))
                        df = sum(1 for i in range(N) if m.bow[i][j] > 0)
                        self._tooltip = [
                            f'Token: "{tok}"',
                            "",
                            f"Suma w korpusie: {total}",
                            f"Wystepuje w {df} z {N} dok.",
                            "",
                            "LPM = zaznacz kolumne",
                        ]
                        self._tooltip_pos = pos
                        return
        # Row label zone
        if py >= hdr_y + _HDR_H and px < _LABEL_W and m is not None:
            N = len(m.doc_titles)
            V = len(m.vocab)
            ri = (py - (hdr_y + _HDR_H)) // _ROW_H
            if 0 <= ri < N:
                doc_len = sum(m.bow[ri])
                self._tooltip = [
                    f'Dokument: "{m.doc_titles[ri]}"',
                    "",
                    f"Dlugosc: {doc_len} tokenow",
                    f"Rozne tokeny: {sum(1 for j in range(V) if m.bow[ri][j] > 0)}",
                ]
                self._tooltip_pos = pos
                return
        # Cell zone
        if py >= hdr_y + _HDR_H and m is not None:
            N = len(m.doc_titles)
            V = len(m.vocab)
            ri = (py - (hdr_y + _HDR_H)) // _ROW_H
            if 0 <= ri < N:
                for ci in range(_MAX_COLS):
                    x0 = _LABEL_W + ci * _COL_W
                    if x0 <= px < x0 + _COL_W:
                        j = self._col_offset + ci
                        if j < V:
                            tok = m.vocab[j]
                            cnt = m.bow[ri][j]
                            dtitle = m.doc_titles[ri]
                            self._tooltip = [
                                f'Token "{tok}" w "{dtitle}"',
                                "",
                                f"BoW = {cnt}",
                                "",
                                "BoW = surowe zliczenia.",
                                "Nie uwzglednia dlugosci dok.",
                                "LPM = zaznacz komorke",
                            ]
                            self._tooltip_pos = pos
                            return
        # Fallback — formula
        self._tooltip = [
            "Bag of Words (BoW)",
            "",
            "Zlicza ile razy kazdy token",
            "pojawia się w dokumencie.",
            "",
            "Ignoruje kolejnosc slow.",
        ]
        self._tooltip_pos = pos

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return None

    def draw(self, surface: pygame.Surface, matrix: WeightMatrix | None = None) -> None:
        if matrix is not None:
            self._last_matrix = matrix
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

        font9 = get_font(9)
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
            surface.blit(
                ls, (x0 + (_COL_W - ls.get_width()) // 2, hdr_y + (_HDR_H - ls.get_height()) // 2)
            )

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
                cell_bg = (
                    (50, 40, 5)
                    if active_cell
                    else (35, 28, 5)
                    if active_col_h
                    else _green_cell(val, max_val)
                )
                pygame.draw.rect(surface, cell_bg, (x0 + 1, y0 + 1, _COL_W - 2, _ROW_H - 2))
                pygame.draw.line(surface, (30, 30, 55), (x0, y0), (x0, y0 + _ROW_H))
                pygame.draw.line(
                    surface, (30, 30, 55), (x0, y0), (_LABEL_W + len(visible_cols) * _COL_W, y0)
                )
                vs = font9.render(str(val), True, _WHITE if val > 0 else _DIM)
                surface.blit(
                    vs, (x0 + (_COL_W - vs.get_width()) // 2, y0 + (_ROW_H - vs.get_height()) // 2)
                )
            pygame.draw.line(
                surface,
                (30, 30, 55),
                (0, y0 + _ROW_H),
                (_LABEL_W + len(visible_cols) * _COL_W, y0 + _ROW_H),
            )

        # Scroll hint
        if V > _MAX_COLS:
            sh = font9.render(
                f"Kolumny {visible_start + 1}-{visible_end}/{V}  (scroll)", True, _DIM
            )
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
        insight = (
            "BoW = surowe zliczenia. Dlugi dokument dostaje duze liczby"
            " -- dlatego potrzebujemy normalizacji."
        )
        iy = _STEP_H - 40
        pygame.draw.rect(surface, (20, 15, 35), (0, iy - 6, _W, 46))
        pygame.draw.line(surface, _PURPLE, (0, iy - 6), (0, iy + 40), 3)
        ins = get_font(11).render(insight, True, (200, 180, 220))
        surface.blit(ins, (8, iy + 4))

        if self._tooltip:
            _draw_tooltip_box(surface, self._tooltip, self._tooltip_pos)

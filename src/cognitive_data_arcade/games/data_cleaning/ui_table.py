# src/cognitive_data_arcade/games/data_cleaning/ui_table.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.games.data_cleaning.generator import DataRow

_ORANGE = (243, 156, 18)
_GREEN = (39, 174, 96)
_WHITE = (240, 240, 240)
_DIM = (120, 120, 160)

VISIBLE_ROWS = 15
ROW_H = 28


class TableWidget:
    """Scrollable data table with flag-row support."""

    def __init__(self, rows: list[DataRow]) -> None:
        self._rows = rows
        self._cursor = 0
        self._scroll = 0
        self._flagged: set[int] = set()
        self._font = get_font(22)

    def handle_keydown(self, key: int) -> str | None:
        """
        Handle a key press.
        Returns 'flagged', 'unflagged', or None (navigation).
        """
        n = len(self._rows)
        if key == pygame.K_UP:
            if self._cursor > 0:
                self._cursor -= 1
                if self._cursor < self._scroll:
                    self._scroll = self._cursor
        elif key == pygame.K_DOWN:
            if self._cursor < n - 1:
                self._cursor += 1
                if self._cursor >= self._scroll + VISIBLE_ROWS:
                    self._scroll = self._cursor - VISIBLE_ROWS + 1
        elif key in (pygame.K_SPACE, pygame.K_RETURN):
            idx = self._cursor
            if idx in self._flagged:
                self._flagged.discard(idx)
                return "unflagged"
            else:
                self._flagged.add(idx)
                return "flagged"
        return None

    def draw(
        self,
        surface: pygame.Surface,
        flagged_override: set[int] | None = None,
        x0: int = 40,
        y0: int = 100,
        hints_visible: bool = True,
    ) -> None:
        flagged = flagged_override if flagged_override is not None else self._flagged
        rows = self._rows

        # Column header
        hdr_y = y0 - 32
        cols = [(x0, "ID"), (x0 + 50, "Ses"), (x0 + 100, "Trial"),
                (x0 + 160, "RT (ms)"), (x0 + 270, "Accuracy"), (x0 + 370, "")]
        for cx, label in cols:
            s = self._font.render(label, True, _DIM)
            surface.blit(s, (cx, hdr_y))
        pygame.draw.line(
            surface, _DIM,
            (x0, hdr_y + 24), (surface.get_width() - x0, hdr_y + 24), 1
        )

        for vi in range(VISIBLE_ROWS):
            ri = self._scroll + vi
            if ri >= len(rows):
                break
            row = rows[ri]
            y = y0 + vi * ROW_H
            active = ri == self._cursor
            is_flagged = ri in flagged

            if active:
                color = _ORANGE
            elif is_flagged and hints_visible:
                color = _GREEN
            else:
                color = _WHITE
            prefix = "[!]" if is_flagged else "   "

            rt_str = f"{row.rt_ms:.1f}" if row.rt_ms is not None else "None"
            acc_str = f"{row.accuracy:.2f}" if row.accuracy is not None else "None"

            def _r(text: str, c: tuple = color) -> pygame.Surface:
                return self._font.render(text, True, c)

            surface.blit(_r(str(row.participant_id)), (x0, y))
            surface.blit(_r(str(row.session)), (x0 + 50, y))
            surface.blit(_r(str(row.trial)), (x0 + 100, y))
            surface.blit(_r(rt_str), (x0 + 160, y))
            surface.blit(_r(acc_str), (x0 + 270, y))
            surface.blit(_r(prefix), (x0 + 370, y))

    @property
    def cursor(self) -> int:
        return self._cursor

    @property
    def flagged(self) -> set[int]:
        return set(self._flagged)

    @property
    def scroll(self) -> int:
        return self._scroll

    def set_cursor(self, idx: int) -> None:
        """Move cursor to idx, adjusting scroll to keep the row visible."""
        n = len(self._rows)
        if not (0 <= idx < n):
            return
        self._cursor = idx
        if self._cursor < self._scroll:
            self._scroll = self._cursor
        elif self._cursor >= self._scroll + VISIBLE_ROWS:
            self._scroll = self._cursor - VISIBLE_ROWS + 1

    def flag_toggle(self, idx: int) -> str:
        """Toggle flag on row idx. Returns 'flagged' or 'unflagged'."""
        if idx in self._flagged:
            self._flagged.discard(idx)
            return "unflagged"
        self._flagged.add(idx)
        return "flagged"

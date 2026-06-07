# src/cognitive_data_arcade/games/data_cleaning/ui_table.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scrollbar import ScrollBar
from cognitive_data_arcade.games.data_cleaning.generator import DataRow

_ORANGE = (243, 156, 18)
_GREEN = (39, 174, 96)
_WHITE = (240, 240, 240)
_DIM = (120, 120, 160)

VISIBLE_ROWS = 15
ROW_H = 28
_TABLE_W = 420        # visual width of table content (used to position scrollbar)
_SCROLLBAR_GAP = 8    # pixels between table content and scrollbar


class TableWidget:
    """Scrollable data table with flag-row support."""

    def __init__(self, rows: list[DataRow], x0: int = 40, y0: int = 100) -> None:
        self._rows = rows
        self._cursor = 0
        self._flagged: set[int] = set()
        self._font = get_font(22)
        self._scrollbar = ScrollBar(
            total=len(rows),
            visible=VISIBLE_ROWS,
            x=x0 + _TABLE_W + _SCROLLBAR_GAP,
            y=y0,
            h=VISIBLE_ROWS * ROW_H,
        )

    @property
    def scroll(self) -> int:
        return self._scrollbar.scroll

    @property
    def cursor(self) -> int:
        return self._cursor

    @property
    def flagged(self) -> set[int]:
        return set(self._flagged)

    def handle_keydown(self, key: int) -> str | None:
        """
        Handle a key press.
        Returns 'flagged', 'unflagged', or None (navigation).
        """
        n = len(self._rows)
        if key == pygame.K_UP:
            if self._cursor > 0:
                self._cursor -= 1
                self._sync_scroll()
        elif key == pygame.K_DOWN:
            if self._cursor < n - 1:
                self._cursor += 1
                self._sync_scroll()
        elif key in (pygame.K_SPACE, pygame.K_RETURN):
            idx = self._cursor
            if idx in self._flagged:
                self._flagged.discard(idx)
                return "unflagged"
            else:
                self._flagged.add(idx)
                return "flagged"
        return None

    def set_cursor(self, idx: int) -> None:
        """Move cursor to idx, adjusting scroll to keep the row visible."""
        n = len(self._rows)
        if not (0 <= idx < n):
            return
        self._cursor = idx
        self._sync_scroll()

    def flag_toggle(self, idx: int) -> str:
        """Toggle flag on row idx. Returns 'flagged' or 'unflagged'."""
        if idx in self._flagged:
            self._flagged.discard(idx)
            return "unflagged"
        self._flagged.add(idx)
        return "flagged"

    def handle_wheel(self, dy: int) -> bool:
        """Scroll by dy rows (positive = down). Returns True if scroll changed."""
        return self._scrollbar.handle_wheel(dy)

    def handle_mousedown(self, pos: tuple[int, int]) -> bool:
        """Forward mousedown to scrollbar. Returns True if consumed."""
        return self._scrollbar.handle_mousedown(pos)

    def handle_mousemotion(self, pos: tuple[int, int], buttons: tuple) -> bool:
        """Forward mousemotion to scrollbar (drag). Returns True if scroll changed."""
        return self._scrollbar.handle_mousemotion(pos, buttons)

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
        scroll = self._scrollbar.scroll

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
            ri = scroll + vi
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

        self._scrollbar.draw(surface)

    def _sync_scroll(self) -> None:
        scroll = self._scrollbar.scroll
        if self._cursor < scroll:
            self._scrollbar.scroll_to(self._cursor)
        elif self._cursor >= scroll + VISIBLE_ROWS:
            self._scrollbar.scroll_to(self._cursor - VISIBLE_ROWS + 1)

# src/cognitive_data_arcade/games/data_cleaning/ui_popup.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.games.data_cleaning.generator import DataRow

_BG = (18, 18, 40)
_WHITE = (240, 240, 240)
_ORANGE = (243, 156, 18)
_DIM = (120, 120, 160)
_BORDER = (60, 60, 100)


class DecisionPopup:
    """
    Modal popup showing one flagged row and asking the student what to do.
    has_format_fix=True replaces 'median' with 'fix_format' in the choice list.
    """

    def __init__(self, row: DataRow, *, has_format_fix: bool) -> None:
        self._row = row
        if has_format_fix:
            self._choices = ["delete", "fix_format", "keep"]
        else:
            self._choices = ["delete", "median", "keep"]
        self._cursor = 0
        self._font_body = get_font(28)
        self._font_hint = get_font(22)

    def handle_keydown(self, key: int) -> str | None:
        """
        Process a key press.
        Returns the chosen fix string when ENTER is pressed, otherwise None.
        """
        n = len(self._choices)
        if key == pygame.K_UP:
            if self._cursor > 0:
                self._cursor -= 1
        elif key == pygame.K_DOWN:
            if self._cursor < n - 1:
                self._cursor += 1
        elif key in (pygame.K_1, pygame.K_2, pygame.K_3):
            idx = key - pygame.K_1
            if idx < n:
                self._cursor = idx
        elif key == pygame.K_RETURN:
            return self._choices[self._cursor]
        return None

    def draw(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        box_w, box_h = 520, 240
        box_x = w // 2 - box_w // 2
        box_y = h // 2 - box_h // 2

        # Semi-transparent overlay
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, _BG, (box_x, box_y, box_w, box_h), border_radius=8)
        pygame.draw.rect(surface, _BORDER, (box_x, box_y, box_w, box_h), 2, border_radius=8)

        # Row values
        row = self._row
        rt_str = f"{row.rt_ms:.1f}" if row.rt_ms is not None else "None"
        acc_str = f"{row.accuracy:.2f}" if row.accuracy is not None else "None"
        info = (
            f"Participant {row.participant_id}  Session {row.session}  "
            f"Trial {row.trial}  |  RT: {rt_str}  Accuracy: {acc_str}"
        )
        info_surf = self._font_hint.render(info, True, _WHITE)
        surface.blit(info_surf, (box_x + 20, box_y + 18))

        # Choice labels
        labels = {
            "delete": "Delete row",
            "median": "Replace with column median",
            "fix_format": "Fix format (divide by 100)",
            "keep": "Keep as-is (it's fine)",
        }
        y = box_y + 60
        for j, choice in enumerate(self._choices):
            active = j == self._cursor
            color = _ORANGE if active else _WHITE
            text = f"[{j + 1}]  {labels[choice]}"
            surf = self._font_body.render(text, True, color)
            surface.blit(surf, (box_x + 20, y))
            y += 44

        hint_surf = self._font_hint.render(
            "ENTER — confirm   UP/DN or 1/2/3 — select", True, _DIM
        )
        surface.blit(
            hint_surf,
            (box_x + box_w // 2 - hint_surf.get_width() // 2, box_y + box_h - 28),
        )

    @property
    def cursor(self) -> int:
        return self._cursor

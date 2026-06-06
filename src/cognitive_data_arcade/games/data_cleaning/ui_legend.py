# src/cognitive_data_arcade/games/data_cleaning/ui_legend.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings

_PANEL_W = 680
_PANEL_H = 260
_BG_PANEL = (18, 18, 42)
_BORDER = (42, 42, 80)
_COL_NAME = (139, 233, 253)   # #8be9fd
_COL_DESC = (170, 170, 170)   # #aaaaaa
_TITLE_COLOR = (240, 240, 240)
_DIM = (100, 100, 140)


def draw_legend_overlay(
    surface: pygame.Surface,
    font: pygame.font.Font,
    strings: Strings,
) -> None:
    """Draw a centred semi-transparent legend overlay."""
    w, h = surface.get_size()

    # Dim the background
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    px = (w - _PANEL_W) // 2
    py = (h - _PANEL_H) // 2

    pygame.draw.rect(surface, _BG_PANEL, (px, py, _PANEL_W, _PANEL_H), border_radius=8)
    pygame.draw.rect(surface, _BORDER,   (px, py, _PANEL_W, _PANEL_H), 1, border_radius=8)

    # Title
    title_font = get_font(30)
    ts = title_font.render(strings.legend_title, True, _TITLE_COLOR)
    surface.blit(ts, (px + _PANEL_W // 2 - ts.get_width() // 2, py + 14))

    # Five column rows
    cols = [
        strings.legend_col_participant_id,
        strings.legend_col_session,
        strings.legend_col_trial,
        strings.legend_col_rt_ms,
        strings.legend_col_accuracy,
    ]
    y = py + 58
    for entry in cols:
        # Split "name — description" on em-dash
        if " — " in entry:
            name_part, desc_part = entry.split(" — ", 1)
        else:
            name_part, desc_part = entry, ""
        ns = font.render(name_part + " —", True, _COL_NAME)
        ds = font.render(desc_part, True, _COL_DESC)
        surface.blit(ns, (px + 24, y))
        surface.blit(ds, (px + 24 + ns.get_width() + 4, y))
        y += 32

    # Footer
    close_font = get_font(20)
    cs = close_font.render("[L] " + ("zamknij" if strings.language == "pl" else "close"),
                           True, _DIM)
    surface.blit(cs, (px + _PANEL_W // 2 - cs.get_width() // 2, py + _PANEL_H - 28))

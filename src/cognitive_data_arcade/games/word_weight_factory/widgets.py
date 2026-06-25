# src/cognitive_data_arcade/games/word_weight_factory/widgets.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.games.word_weight_factory.corpus import CorpusState, _PRESETS

from cognitive_data_arcade.engine.colors import (
    WHITE as _WHITE,
    DIM as _DIM,
    BLUE as _BLUE,
    PURPLE as _PURPLE,
)

_PANEL_W = 220
_PANEL = (18, 18, 42)
_AMBER = (243, 156, 18)

_MAX_CUSTOM_LEN = 160
_DOC_ROW_H = 28
_DOCS_TOP = 44  # y inside the panel surface
_CHK_SIZE = 14

_TOOLTIP_W = 240
_TOOLTIP_PAD = 8
_TOOLTIP_LINE = 18


class CorpusPanel:
    def __init__(self, state: CorpusState) -> None:
        self._state = state
        self._custom_active = False
        pygame.key.set_repeat(400, 50)

        # Checkbox rects (in panel-local coords, inside a 672 px tall surface)
        chk_top = _DOCS_TOP + (len(_PRESETS) + 1) * _DOC_ROW_H + 16
        self._chk_rects = [
            pygame.Rect(8, chk_top, _CHK_SIZE, _CHK_SIZE),
            pygame.Rect(8, chk_top + 24, _CHK_SIZE, _CHK_SIZE),
            pygame.Rect(8, chk_top + 48, _CHK_SIZE, _CHK_SIZE),
        ]
        self._chk_labels = ["Lowercase", "Rm punct", "Rm stops"]
        self._chk_flags = ["lowercase", "rm_punct", "rm_stops"]

        # Custom text field rect
        self._field_rect = pygame.Rect(8, chk_top + 82, _PANEL_W - 16, 22)
        # Lang toggle rect
        self._lang_rect = pygame.Rect(8, chk_top + 112, 60, 20)

        self._tooltip_lines: list[str] | None = None
        self._tooltip_panel_pos: tuple[int, int] = (0, 0)

    # ------------------------------------------------------------------
    def is_custom_active(self) -> bool:
        return self._custom_active

    # ------------------------------------------------------------------
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Return True if the event was consumed."""
        if event.type == pygame.KEYDOWN and self._custom_active:
            if event.key == pygame.K_BACKSPACE:
                self._state.custom_text = self._state.custom_text[:-1]
                return True
            if event.unicode and len(self._state.custom_text) < _MAX_CUSTOM_LEN:
                self._state.custom_text += event.unicode
                return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if event.pos[0] < _PANEL_W and event.pos[1] >= 0:
                self._open_tooltip(event.pos)
                return True
            return False

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False

        self._tooltip_lines = None
        pos = event.pos

        # Document rows
        for i, (title, _, _lang) in enumerate(_PRESETS):
            row_rect = pygame.Rect(4, _DOCS_TOP + i * _DOC_ROW_H, _PANEL_W - 8, _DOC_ROW_H - 2)
            if row_rect.collidepoint(pos):
                self._state.selected_idx = i
                self._custom_active = False
                return True

        # "Wlasny" row
        wlasny_rect = pygame.Rect(
            4, _DOCS_TOP + len(_PRESETS) * _DOC_ROW_H, _PANEL_W - 8, _DOC_ROW_H - 2
        )
        if wlasny_rect.collidepoint(pos):
            self._state.selected_idx = len(_PRESETS)
            self._custom_active = True
            return True

        # Checkboxes
        for i, rect in enumerate(self._chk_rects):
            if rect.collidepoint(pos):
                setattr(
                    self._state, self._chk_flags[i], not getattr(self._state, self._chk_flags[i])
                )
                return True

        # Lang toggle (only in custom mode)
        if self._custom_active and self._lang_rect.collidepoint(pos):
            self._state.lang = "en" if self._state.lang == "pl" else "pl"
            return True

        return False

    # ------------------------------------------------------------------
    def _open_tooltip(self, pos: tuple[int, int]) -> None:
        # Document rows
        for i, (title, text, _lang) in enumerate(_PRESETS):
            row_rect = pygame.Rect(4, _DOCS_TOP + i * _DOC_ROW_H, _PANEL_W - 8, _DOC_ROW_H - 2)
            if row_rect.collidepoint(pos):
                words = text.split()[:6]
                snippet = " ".join(words) + ("..." if len(text.split()) > 6 else "")
                self._tooltip_lines = [
                    f"Dok: {title}",
                    "",
                    snippet,
                    "",
                    "LPM = wybierz ten dokument",
                ]
                self._tooltip_panel_pos = pos
                return
        # Wlasny row
        wi = len(_PRESETS)
        wlasny_rect = pygame.Rect(4, _DOCS_TOP + wi * _DOC_ROW_H, _PANEL_W - 8, _DOC_ROW_H - 2)
        if wlasny_rect.collidepoint(pos):
            self._tooltip_lines = [
                "Wlasny tekst",
                "",
                "Wpisz swoj tekst i obserwuj",
                "jak zmienia się macierze",
                "BoW / TF / IDF / TF-IDF.",
            ]
            self._tooltip_panel_pos = pos
            return
        # Checkboxes
        _chk_explanations = [
            ["Lowercase", "", "Zamienia litery na male.", "'Ala' i 'ala' to ten sam token."],
            ["Usun interpunkcje", "", "Usuwa kropki, przecinki.", "'slowo.' staje się 'slowo'."],
            ["Usun stop words", "", "Usuwa slowa bez wartosci", "informacyjnej (i, w, z, ale...)."],
        ]
        for i, rect in enumerate(self._chk_rects):
            expanded = pygame.Rect(rect.x - 2, rect.y - 4, _PANEL_W - 12, rect.h + 8)
            if expanded.collidepoint(pos):
                self._tooltip_lines = _chk_explanations[i]
                self._tooltip_panel_pos = pos
                return
        # Lang toggle (only visible when custom active)
        if self._custom_active and self._lang_rect.collidepoint(pos):
            self._tooltip_lines = [
                "Jezyk stop words",
                "",
                "PL = polski slownik slow",
                "EN = angielski slownik slow",
                "LPM = przelacz jezyk",
            ]
            self._tooltip_panel_pos = pos
            return
        self._tooltip_lines = [
            "Panel korpusu",
            "",
            "Wybierz dokument z listy",
            "lub wpisz wlasny tekst.",
            "Opcje filtruja tokeny",
            "w calym potoku.",
        ]
        self._tooltip_panel_pos = pos

    def draw_tooltip(self, surface: pygame.Surface, pipe_h: int) -> None:
        if not self._tooltip_lines:
            return
        lines = self._tooltip_lines
        n = len(lines)
        bh = n * _TOOLTIP_LINE + _TOOLTIP_PAD * 2
        sx = self._tooltip_panel_pos[0]
        sy = self._tooltip_panel_pos[1] + pipe_h
        tx = max(_PANEL_W + 4, min(sx + _PANEL_W, surface.get_width() - _TOOLTIP_W - 4))
        ty = max(pipe_h + 4, min(sy, surface.get_height() - bh - 4))
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

    # ------------------------------------------------------------------
    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _PANEL, (0, 0, _PANEL_W, surface.get_height()))
        pygame.draw.line(
            surface, (40, 40, 70), (_PANEL_W - 1, 0), (_PANEL_W - 1, surface.get_height())
        )

        # Header
        hdr = get_font(12).render("KORPUS", True, _PURPLE)
        surface.blit(hdr, (8, 12))

        # Document rows
        docs = self._state.active_docs()
        for i, (title, _text, _lang) in enumerate(_PRESETS):
            y = _DOCS_TOP + i * _DOC_ROW_H
            active = i == self._state.selected_idx and not self._custom_active
            bg = (30, 28, 12) if active else _PANEL
            pygame.draw.rect(surface, bg, (4, y, _PANEL_W - 8, _DOC_ROW_H - 2), border_radius=2)
            col = _AMBER if active else _DIM
            lbl = get_font(11).render(title, True, col)
            surface.blit(lbl, (10, y + (_DOC_ROW_H - 2 - lbl.get_height()) // 2))

        # Wlasny row
        wi = len(_PRESETS)
        wy = _DOCS_TOP + wi * _DOC_ROW_H
        active_custom = self._custom_active
        bg = (12, 22, 32) if active_custom else _PANEL
        pygame.draw.rect(surface, bg, (4, wy, _PANEL_W - 8, _DOC_ROW_H - 2), border_radius=2)
        pygame.draw.rect(
            surface,
            _BLUE if active_custom else (40, 40, 70),
            (4, wy, _PANEL_W - 8, _DOC_ROW_H - 2),
            1,
            border_radius=2,
        )
        wlbl = get_font(11).render("+ Wlasny", True, _BLUE if active_custom else _DIM)
        surface.blit(wlbl, (10, wy + (_DOC_ROW_H - 2 - wlbl.get_height()) // 2))

        # Separator
        sep_y = _DOCS_TOP + (wi + 1) * _DOC_ROW_H + 8
        pygame.draw.line(surface, (40, 40, 70), (8, sep_y), (_PANEL_W - 8, sep_y))

        # Checkboxes
        chk_vals = [self._state.lowercase, self._state.rm_punct, self._state.rm_stops]
        for i, rect in enumerate(self._chk_rects):
            pygame.draw.rect(surface, (30, 30, 55), rect, border_radius=2)
            pygame.draw.rect(surface, _AMBER, rect, 1, border_radius=2)
            if chk_vals[i]:
                pygame.draw.line(
                    surface, _AMBER, (rect.x + 2, rect.centery), (rect.centerx, rect.bottom - 2), 2
                )
                pygame.draw.line(
                    surface,
                    _AMBER,
                    (rect.centerx, rect.bottom - 2),
                    (rect.right - 2, rect.y + 2),
                    2,
                )
            clbl = get_font(10).render(self._chk_labels[i], True, _WHITE if chk_vals[i] else _DIM)
            surface.blit(clbl, (rect.right + 6, rect.y))

        # Custom text field + lang toggle
        if self._custom_active:
            pygame.draw.rect(surface, (25, 30, 50), self._field_rect, border_radius=2)
            pygame.draw.rect(surface, _BLUE, self._field_rect, 1, border_radius=2)
            disp = (
                self._state.custom_text[-30:]
                if len(self._state.custom_text) > 30
                else self._state.custom_text
            )
            ts = get_font(10).render(disp + "|", True, _WHITE)
            surface.blit(
                ts,
                (
                    self._field_rect.x + 3,
                    self._field_rect.y + (self._field_rect.h - ts.get_height()) // 2,
                ),
            )

            pygame.draw.rect(surface, (20, 25, 45), self._lang_rect, border_radius=2)
            pygame.draw.rect(surface, _BLUE, self._lang_rect, 1, border_radius=2)
            ll = get_font(10).render(self._state.lang.upper(), True, _BLUE)
            surface.blit(
                ll,
                (
                    self._lang_rect.x + (self._lang_rect.w - ll.get_width()) // 2,
                    self._lang_rect.y + (self._lang_rect.h - ll.get_height()) // 2,
                ),
            )

        # Live stat
        vocab_count = len(
            {
                t
                for _, text in docs
                for t in (text.lower().split() if self._state.lowercase else text.split())
            }
        )
        stat = get_font(10).render(f"Slownik: ~{vocab_count} tokenow", True, _DIM)
        surface.blit(stat, (8, surface.get_height() - 20))

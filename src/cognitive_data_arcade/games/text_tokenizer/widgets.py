# src/cognitive_data_arcade/games/text_tokenizer/widgets.py
from __future__ import annotations

from dataclasses import dataclass, field

import pygame

from cognitive_data_arcade.engine.fonts import get_font

PRESET_TWEET_PL = (
    "Badanie wykazalo, ze czas reakcji wzrosl o 120 ms! "
    "CZAS REAKCJI jest kluczowy w Stroopie."
)
PRESET_ABSTRACT_EN = (
    "Reaction time increased in the congruent condition. "
    "The effect was observed across all participants."
)
PRESET_SMS_PL = (
    "hej, jutro mamy kognitywistyke? "
    "bo nie pamietam czy sa zajecia czy nie ma :)"
)

_PRESETS: list[tuple[str, str, str]] = [
    ("Tweet PL",     PRESET_TWEET_PL,    "pl"),
    ("Abstract EN",  PRESET_ABSTRACT_EN, "en"),
    ("SMS PL",       PRESET_SMS_PL,      "pl"),
    ("Wlasny",       "",                 ""),
]
_MAX_TEXT_LEN = 180
_BAR_H = 48
_W = 1024
_BG    = (12, 12, 28)
_PANEL = (18, 18, 42)
_WHITE = (240, 240, 240)
_DIM   = (120, 120, 160)
_AMBER = (243, 156, 18)
_BLUE  = (52, 152, 219)


@dataclass
class SharedState:
    text: str = field(default_factory=lambda: PRESET_TWEET_PL)
    lang: str = "pl"
    lowercase: bool = True
    rm_punct: bool = True
    rm_stops: bool = False
    ngram_n: int = 2
    topn: int = 10
    show_stops_in_chart: bool = False


class SharedInputBar:
    def __init__(self, state: SharedState) -> None:
        self._state = state
        self._active_preset = 0
        self._custom_active = False

        btn_w = 90
        btn_gap = 6
        total_btns = len(_PRESETS) * (btn_w + btn_gap) + 70  # 70 for lang toggle
        field_w = _W - total_btns - 16
        self._field_rect = pygame.Rect(8, 10, field_w, 28)

        x = field_w + 16
        self._btn_rects: list[pygame.Rect] = []
        for _ in _PRESETS:
            self._btn_rects.append(pygame.Rect(x, 10, btn_w, 28))
            x += btn_w + btn_gap

        self._lang_toggle_rect = pygame.Rect(x, 10, 62, 28)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN and self._custom_active:
            if event.key == pygame.K_BACKSPACE:
                self._state.text = self._state.text[:-1]
                return True
            if event.unicode and len(self._state.text) < _MAX_TEXT_LEN:
                self._state.text += event.unicode
                return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self._btn_rects):
                if rect.collidepoint(event.pos):
                    self._active_preset = i
                    if i < 3:
                        label, text, lang = _PRESETS[i]
                        self._state.text = text
                        self._state.lang = lang
                        self._custom_active = False
                    else:
                        self._custom_active = True
                        if not self._state.text:
                            self._state.text = PRESET_TWEET_PL
                    return True
            if self._custom_active and self._lang_toggle_rect.collidepoint(event.pos):
                self._state.lang = "en" if self._state.lang == "pl" else "pl"
                return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _BG, (0, 0, _W, _BAR_H))
        pygame.draw.line(surface, (40, 40, 70), (0, _BAR_H - 1), (_W, _BAR_H - 1))

        font = get_font(11)
        lbl = font.render("TEKST:", True, (155, 89, 182))
        surface.blit(lbl, (8, (_BAR_H - lbl.get_height()) // 2 + 2))

        # Text field
        field_col = (30, 30, 55) if self._custom_active else (20, 20, 40)
        border_col = _AMBER if self._custom_active else (50, 50, 80)
        pygame.draw.rect(surface, field_col, self._field_rect, border_radius=3)
        pygame.draw.rect(surface, border_col, self._field_rect, 1, border_radius=3)
        text_surf = get_font(10).render(
            self._state.text[:100] + ("..." if len(self._state.text) > 100 else ""),
            True, _WHITE,
        )
        surface.blit(text_surf, (self._field_rect.x + 4,
                                  self._field_rect.y + (self._field_rect.h - text_surf.get_height()) // 2))

        # Preset buttons
        for i, (label, _, _lang) in enumerate(_PRESETS):
            rect = self._btn_rects[i]
            active = i == self._active_preset
            bg = (50, 50, 90) if active else (20, 20, 40)
            border = _AMBER if active else (50, 50, 80)
            pygame.draw.rect(surface, bg, rect, border_radius=3)
            pygame.draw.rect(surface, border, rect, 1, border_radius=3)
            col = _AMBER if active else _DIM
            lbl_s = get_font(10).render(label, True, col)
            surface.blit(lbl_s, (rect.x + (rect.w - lbl_s.get_width()) // 2,
                                  rect.y + (rect.h - lbl_s.get_height()) // 2))

        # Lang toggle (only visible in custom mode)
        if self._custom_active:
            rect = self._lang_toggle_rect
            pygame.draw.rect(surface, (25, 25, 50), rect, border_radius=3)
            pygame.draw.rect(surface, _BLUE, rect, 1, border_radius=3)
            lang_lbl = get_font(10).render(self._state.lang.upper(), True, _BLUE)
            surface.blit(lang_lbl, (rect.x + (rect.w - lang_lbl.get_width()) // 2,
                                     rect.y + (rect.h - lang_lbl.get_height()) // 2))

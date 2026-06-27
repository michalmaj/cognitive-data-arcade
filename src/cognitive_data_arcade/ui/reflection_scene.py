from __future__ import annotations

from typing import Any

import pygame

from cognitive_data_arcade.engine.colors import BG as _BG, DIM as _DIM, ORANGE, WHITE as _WHITE
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene

_INDIGO = (99, 102, 241)
_BRIGHT_GREEN = (74, 222, 128)
_PURPLE = (167, 139, 250)
_CARD_BG = (19, 21, 42)
_QUESTION_BG = (15, 17, 32)

_COLOR_MAP: dict[str, tuple[int, int, int]] = {
    "indigo": _INDIGO,
    "orange": ORANGE,
    "green": _BRIGHT_GREEN,
}

_MARGIN_X = 40
_CARDS_TOP = 60
_CARD_GAP = 16
_CARD_PAD = 16
_QUESTION_TOP_OFFSET = 20
_QUESTION_LEFT_BORDER = 4


def _wrap(text: str, font: pygame.font.Font, max_w: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        words = para.split()
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if font.size(candidate)[0] <= max_w:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


class ReflectionScene(Scene):
    def __init__(
        self,
        reflection: dict[str, Any],
        strings: Strings,
        back_scene: Scene,
    ) -> None:
        self._reflection = reflection
        self._strings = strings
        self._back = back_scene
        self._done = False
        pygame.font.init()
        self._font_title = get_font(28)
        self._font_card_label = get_font(15)
        self._font_card_body = get_font(18)
        self._font_q_label = get_font(15)
        self._font_q_text = get_font(20)
        self._font_hint = get_font(20)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._done = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._done = True

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._back if self._done else None

    def draw(self, surface: pygame.Surface) -> None:
        lang = self._strings.language
        data = self._reflection.get(lang) or self._reflection.get("en", {})
        surface.fill(_BG)
        w, h = surface.get_size()

        # Title
        title_surf = self._font_title.render(data.get("title", "Reflection"), True, _WHITE)
        surface.blit(title_surf, (14, 12))

        # ESC hint (top-right)
        hint_text = "ESC — powrot" if lang == "pl" else "ESC — back"
        hint_surf = self._font_hint.render(hint_text, True, _DIM)
        surface.blit(hint_surf, (w - hint_surf.get_width() - 14, 12))

        # Cards
        cards = data.get("cards", [])
        n = len(cards)
        if n > 0:
            total_gap = _CARD_GAP * (n - 1)
            card_w = (w - 2 * _MARGIN_X - total_gap) // n
            card_y = _CARDS_TOP + title_surf.get_height() + 16
            card_x = _MARGIN_X

            body_wrap_w = card_w - 2 * _CARD_PAD
            max_card_h = 0
            for card in cards:
                body_lines = _wrap(card.get("text", ""), self._font_card_body, body_wrap_w)
                ch = (
                    _CARD_PAD
                    + self._font_card_label.get_height()
                    + 8
                    + len(body_lines) * (self._font_card_body.get_height() + 2)
                    + _CARD_PAD
                )
                max_card_h = max(max_card_h, ch)

            for card in cards:
                color = _COLOR_MAP.get(card.get("color", "indigo"), _INDIGO)
                rect = pygame.Rect(card_x, card_y, card_w, max_card_h)

                pygame.draw.rect(surface, _CARD_BG, rect, border_radius=6)
                border_rect = pygame.Rect(card_x, card_y, card_w, 3)
                pygame.draw.rect(surface, color, border_rect, border_radius=3)

                label_text = card.get("label", "").upper()
                label_surf = self._font_card_label.render(label_text, True, color)
                surface.blit(label_surf, (card_x + _CARD_PAD, card_y + _CARD_PAD))

                body_lines = _wrap(card.get("text", ""), self._font_card_body, body_wrap_w)
                body_y = card_y + _CARD_PAD + label_surf.get_height() + 8
                for line in body_lines:
                    line_surf = self._font_card_body.render(line, True, _WHITE)
                    surface.blit(line_surf, (card_x + _CARD_PAD, body_y))
                    body_y += self._font_card_body.get_height() + 2

                card_x += card_w + _CARD_GAP

            question_top = card_y + max_card_h + _QUESTION_TOP_OFFSET
        else:
            question_top = _CARDS_TOP + title_surf.get_height() + 16

        # Question block (purple left border)
        q_label_text = "Zastanow sie" if lang == "pl" else "Think about it"
        q_label_surf = self._font_q_label.render(q_label_text.upper(), True, _PURPLE)

        question_text = data.get("question", "")
        q_wrap_w = w - 2 * _MARGIN_X - _CARD_PAD * 2 - _QUESTION_LEFT_BORDER - 6
        q_lines = _wrap(question_text, self._font_q_text, q_wrap_w)
        q_h = (
            _CARD_PAD
            + q_label_surf.get_height()
            + 6
            + len(q_lines) * (self._font_q_text.get_height() + 2)
            + _CARD_PAD
        )

        q_rect = pygame.Rect(_MARGIN_X, question_top, w - 2 * _MARGIN_X, q_h)
        pygame.draw.rect(surface, _QUESTION_BG, q_rect, border_radius=4)
        pygame.draw.rect(
            surface,
            _PURPLE,
            pygame.Rect(_MARGIN_X, question_top, _QUESTION_LEFT_BORDER, q_h),
        )

        text_x = _MARGIN_X + _QUESTION_LEFT_BORDER + _CARD_PAD
        surface.blit(q_label_surf, (text_x, question_top + _CARD_PAD))
        q_y = question_top + _CARD_PAD + q_label_surf.get_height() + 6
        for line in q_lines:
            line_surf = self._font_q_text.render(line, True, _WHITE)
            surface.blit(line_surf, (text_x, q_y))
            q_y += self._font_q_text.get_height() + 2

        # Bottom hint
        bottom_hint = (
            "Nacisnij ESC lub kliknij, zeby wrocic"
            if lang == "pl"
            else "Press ESC or click to return"
        )
        bh_surf = self._font_hint.render(bottom_hint, True, _DIM)
        surface.blit(bh_surf, (w // 2 - bh_surf.get_width() // 2, h - 40))

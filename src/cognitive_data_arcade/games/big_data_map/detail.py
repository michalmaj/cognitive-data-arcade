from __future__ import annotations

import pygame
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.engine.colors import BG as _BG, ORANGE as _ORANGE

from .concept_data import DISPLAY_NUM, MODULE_COLORS, MODULE_NAMES, get_connected, _node_map

_W, _H = 1024, 768

_TEXT_LIGHT = (240, 240, 240)
_TEXT_DIM = (100, 100, 140)
_DIVIDER = (30, 30, 60)
_CONNECTED_DOT_R = 8

# Layout constants
_MARGIN = 40
_HEADER_H = 90
_DESC_Y = _HEADER_H + 16
_CONNECTIONS_LABEL_Y = _DESC_Y + 64
_CONNECTIONS_Y = _CONNECTIONS_LABEL_Y + 32
_ROW_H = 90
_FOOTER_H = 44


class ConceptDetailScene(Scene):
    """Full-screen detail panel for a single concept node."""

    def __init__(self, lesson_num: int, strings: Strings, back_scene: Scene | None) -> None:
        self._lesson_num = lesson_num
        self._strings = strings
        self._back_scene = back_scene
        self._done = False

        self._node = _node_map.get(lesson_num)
        self._connections = get_connected(lesson_num, max_count=5)

        self._font_title = get_font(26)
        self._font_module = get_font(14)
        self._font_desc = get_font(18)
        self._font_conn_name = get_font(15)
        self._font_conn_reason = get_font(13)
        self._font_hint = get_font(16)

    # --- scene protocol ---

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self._done = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._done = True

    def update(self, dt: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._back_scene if self._done else None

    # --- drawing ---

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        if self._node is None:
            return
        lang = self._strings.language if hasattr(self._strings, "language") else "pl"
        self._draw_header(surface, lang)
        self._draw_description(surface, lang)
        self._draw_connections(surface, lang)
        self._draw_footer(surface, lang)

    def _draw_header(self, surface: pygame.Surface, lang: str) -> None:
        node = self._node
        assert node is not None
        color = MODULE_COLORS[node.module]
        display = DISPLAY_NUM.get(node.lesson_num, node.lesson_num)
        name = (node.name_pl if lang == "pl" else node.name_en).replace("\n", " ")
        mod_name = MODULE_NAMES[node.module][0 if lang == "pl" else 1]

        # Coloured left accent bar
        pygame.draw.rect(surface, color, (_MARGIN - 6, 16, 6, _HEADER_H - 16))

        # Number badge
        badge_surf = self._font_title.render(str(display), True, color)
        surface.blit(badge_surf, (_MARGIN + 4, 20))

        # Lesson name
        name_surf = self._font_title.render(name, True, _TEXT_LIGHT)
        surface.blit(name_surf, (_MARGIN + 4 + badge_surf.get_width() + 14, 20))

        # Module label below
        mod_surf = self._font_module.render(mod_name, True, color)
        surface.blit(mod_surf, (_MARGIN + 4, 20 + badge_surf.get_height() + 4))

        pygame.draw.line(surface, _DIVIDER, (_MARGIN, _HEADER_H), (_W - _MARGIN, _HEADER_H), 1)

    def _draw_description(self, surface: pygame.Surface, lang: str) -> None:
        node = self._node
        assert node is not None
        desc = node.description_pl if lang == "pl" else node.description_en
        desc_surf = self._font_desc.render(desc, True, _TEXT_LIGHT)
        surface.blit(desc_surf, (_MARGIN, _DESC_Y))

    def _draw_connections(self, surface: pygame.Surface, lang: str) -> None:
        if lang == "pl":
            label = "Powiazania logiczne:"
        else:
            label = "Logical connections:"
        lbl_surf = self._font_module.render(label, True, _ORANGE)
        surface.blit(lbl_surf, (_MARGIN, _CONNECTIONS_LABEL_Y))

        for i, (other, reason_pl, reason_en) in enumerate(self._connections):
            row_y = _CONNECTIONS_Y + i * _ROW_H
            color = MODULE_COLORS[other.module]
            display = DISPLAY_NUM.get(other.lesson_num, other.lesson_num)
            other_name = (other.name_pl if lang == "pl" else other.name_en).replace("\n", " ")
            reason = reason_pl if lang == "pl" else reason_en

            # Coloured dot
            pygame.draw.circle(
                surface, color, (_MARGIN + _CONNECTED_DOT_R, row_y + 14), _CONNECTED_DOT_R
            )

            # Node number + name
            node_label = f"{display}. {other_name}"
            name_surf = self._font_conn_name.render(node_label, True, color)
            surface.blit(name_surf, (_MARGIN + _CONNECTED_DOT_R * 2 + 8, row_y + 2))

            # Reason text (may be long — truncate if needed)
            max_reason_w = _W - _MARGIN * 2 - _CONNECTED_DOT_R * 2 - 8
            reason_surf = self._font_conn_reason.render(reason, True, _TEXT_DIM)
            if reason_surf.get_width() > max_reason_w:
                # Clip to available width
                clip_rect = pygame.Rect(0, 0, max_reason_w, reason_surf.get_height())
                surface.blit(
                    reason_surf, (_MARGIN + _CONNECTED_DOT_R * 2 + 8, row_y + 26), clip_rect
                )
            else:
                surface.blit(reason_surf, (_MARGIN + _CONNECTED_DOT_R * 2 + 8, row_y + 26))

            # Thin separator
            if i < len(self._connections) - 1:
                sep_y = row_y + _ROW_H - 4
                pygame.draw.line(surface, _DIVIDER, (_MARGIN, sep_y), (_W - _MARGIN, sep_y), 1)

    def _draw_footer(self, surface: pygame.Surface, lang: str) -> None:
        footer_y = _H - _FOOTER_H
        pygame.draw.line(surface, _DIVIDER, (0, footer_y), (_W, footer_y), 1)
        if lang == "pl":
            hint = "BACKSPACE / ESC / kliknij — powrot do sieci pojec"
        else:
            hint = "BACKSPACE / ESC / click — back to concept network"
        hint_surf = self._font_hint.render(hint, True, _TEXT_DIM)
        surface.blit(hint_surf, ((_W - hint_surf.get_width()) // 2, footer_y + 10))

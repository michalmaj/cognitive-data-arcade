from __future__ import annotations

import importlib
from typing import Callable

import pygame

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    ORANGE as _ORANGE,
    DIM as _DIM,
)

_SECTIONS = ("theory", "notes", "tasks")
_LEFT = 40
_TAB_Y = 16
_DIVIDER_Y = 58
_TEXT_Y = 80
_HINT_Y_OFFSET = 36

_TOC_PANEL_W = 330
_TOC_SECTION_H = 40
_TOC_ITEM_H = 32
_TOC_PAD = 14
_TOC_PREVIEW_CHARS = 48
_TOC_BTN_W = 44
_TOC_BTN_H = 34
_TOC_PANEL_BG = (14, 14, 38, 235)
_TOC_HOVER_BG = (40, 40, 80)
_TOC_ACTIVE_BG = (55, 40, 100)


def _load_content(lesson_num: int, lang: str) -> list[tuple[str, str]]:
    try:
        mod = importlib.import_module(f"cognitive_data_arcade.lessons.lesson_{lesson_num:02d}")
    except ImportError:
        return []
    data = getattr(mod, "CONTENT", {})
    lang_data = data.get(lang) or data.get("pl") or {}
    slides: list[tuple[str, str]] = []
    for section in _SECTIONS:
        for text in lang_data.get(section, []):
            slides.append((section, text))
    return slides


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


def _preview(text: str) -> str:
    text = text.replace("\n", " ")
    if len(text) <= _TOC_PREVIEW_CHARS:
        return text
    return text[:_TOC_PREVIEW_CHARS].rstrip() + "…"


class LessonReaderScene(Scene):
    def __init__(
        self,
        lesson_num: int,
        strings: Strings,
        back_scene: Scene | None,
        play_factory: Callable[[], Scene] | None = None,
    ) -> None:
        self._strings = strings
        self._back = back_scene
        self._play_factory = play_factory
        self._done = False
        self._next: Scene | None = None
        self._slides = _load_content(lesson_num, strings.language)
        self._idx = 0
        self._font_section = get_font(32)
        self._font_text = get_font(28)
        self._font_hint = get_font(24)
        self._font_toc = get_font(20)

        # TOC state
        self._toc_open = False
        self._toc_item_rects: list[tuple[int, pygame.Rect]] = []

        # Pre-compute tab hit rects (window is always 1024 wide)
        self._tab_rects: dict[str, pygame.Rect] = {}
        tab_x = _LEFT
        for s in _SECTIONS:
            label = self._section_label(s)
            lw, _lh = self._font_section.size(label)
            self._tab_rects[s] = pygame.Rect(tab_x, _TAB_Y, lw, _DIVIDER_Y - _TAB_Y)
            tab_x += lw + 48

        # TOC button — top-right corner of header
        self._toc_btn_rect = pygame.Rect(
            1024 - _LEFT - _TOC_BTN_W, _TAB_Y + 2, _TOC_BTN_W, _TOC_BTN_H
        )

    def _section_label(self, section: str) -> str:
        return {
            "theory": self._strings.lesson_theory,
            "notes": self._strings.lesson_notes,
            "tasks": self._strings.lesson_tasks,
        }.get(section, section)

    def _jump_to_section(self, section: str) -> None:
        for i, (s, _) in enumerate(self._slides):
            if s == section:
                if self._slides[self._idx][0] != section:
                    audio.play_sfx("navigate")
                self._idx = i
                return

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self._slides:
            self._done = True
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._toc_open:
                # Click on a TOC item → jump and close
                for slide_idx, rect in self._toc_item_rects:
                    if rect.collidepoint(event.pos):
                        if slide_idx != self._idx:
                            audio.play_sfx("navigate")
                        self._idx = slide_idx
                        self._toc_open = False
                        return
                # Click anywhere else → close TOC
                self._toc_open = False
                return

            # TOC button
            if self._toc_btn_rect.collidepoint(event.pos):
                self._toc_open = True
                return

            # Tab bar click
            for s, rect in self._tab_rects.items():
                if rect.collidepoint(event.pos):
                    self._jump_to_section(s)
                    return

            # Left/right half click — navigate pages
            surf = pygame.display.get_surface()
            w = surf.get_size()[0] if surf else 1024
            if event.pos[0] >= w // 2:
                prev = self._slides[self._idx][0]
                self._idx = (self._idx + 1) % len(self._slides)
                if self._slides[self._idx][0] != prev:
                    audio.play_sfx("navigate")
            else:
                prev = self._slides[self._idx][0]
                self._idx = (self._idx - 1) % len(self._slides)
                if self._slides[self._idx][0] != prev:
                    audio.play_sfx("navigate")
            return

        if event.type != pygame.KEYDOWN:
            return
        key = event.key

        if key == pygame.K_t:
            self._toc_open = not self._toc_open
            return

        if key == pygame.K_ESCAPE:
            if self._toc_open:
                self._toc_open = False
                return
            self._next = self._back
            self._done = True
            return

        if self._toc_open:
            return

        if key == pygame.K_RETURN and self._play_factory is not None:
            self._next = self._play_factory()
            self._done = True
        elif key in (pygame.K_SPACE, pygame.K_RIGHT):
            prev = self._slides[self._idx][0]
            self._idx = (self._idx + 1) % len(self._slides)
            if self._slides[self._idx][0] != prev:
                audio.play_sfx("navigate")
        elif key in (pygame.K_LEFT, pygame.K_BACKSPACE):
            prev = self._slides[self._idx][0]
            self._idx = (self._idx - 1) % len(self._slides)
            if self._slides[self._idx][0] != prev:
                audio.play_sfx("navigate")

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next if self._done else None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()

        if not self._slides:
            return

        section, text = self._slides[self._idx]

        # Section tab bar
        tab_x = _LEFT
        for s in _SECTIONS:
            label = self._section_label(s)
            color = _ORANGE if s == section else _DIM
            surf = self._font_section.render(label, True, color)
            surface.blit(surf, (tab_x, _TAB_Y))
            if s == section:
                underline_y = _TAB_Y + surf.get_height() + 2
                pygame.draw.line(
                    surface,
                    _ORANGE,
                    (tab_x, underline_y),
                    (tab_x + surf.get_width(), underline_y),
                    2,
                )
            tab_x += surf.get_width() + 48

        # TOC toggle button (three horizontal lines)
        btn = self._toc_btn_rect
        btn_color = _ORANGE if self._toc_open else _DIM
        pygame.draw.rect(surface, (25, 25, 50), btn, border_radius=4)
        pygame.draw.rect(surface, btn_color, btn, 1, border_radius=4)
        for i in range(3):
            line_y = btn.y + 8 + i * 8
            pygame.draw.line(
                surface, btn_color, (btn.x + 8, line_y), (btn.x + btn.w - 8, line_y), 2
            )

        # Divider
        pygame.draw.line(surface, _DIM, (_LEFT, _DIVIDER_Y), (w - _LEFT, _DIVIDER_Y))

        # Slide text
        lines = _wrap(text, self._font_text, w - _LEFT * 2)
        text_y = _TEXT_Y
        for line in lines:
            surf = self._font_text.render(line, True, _WHITE)
            surface.blit(surf, (_LEFT, text_y))
            text_y += surf.get_height() + 8

        # Section slide counter (bottom right)
        section_names = [s for s, _ in self._slides]
        section_total = section_names.count(section)
        section_pos = section_names[: self._idx + 1].count(section)
        counter = f"{self._section_label(section)}  {section_pos} / {section_total}"
        c_surf = self._font_hint.render(counter, True, _DIM)
        surface.blit(c_surf, (w - c_surf.get_width() - _LEFT, h - _HINT_Y_OFFSET))

        # Hint (bottom left)
        hint = self._font_hint.render(self._strings.lesson_reader_hint, True, _DIM)
        surface.blit(hint, (_LEFT, h - _HINT_Y_OFFSET))
        if self._play_factory is not None:
            play_hint = self._font_hint.render(self._strings.lesson_reader_play_hint, True, _ORANGE)
            surface.blit(play_hint, (_LEFT, h - _HINT_Y_OFFSET - play_hint.get_height() - 4))

        # TOC dropdown panel (drawn last — on top of everything)
        if self._toc_open:
            self._draw_toc_panel(surface, w)

    def _draw_toc_panel(self, surface: pygame.Surface, w: int) -> None:
        panel_x = w - _TOC_PANEL_W - _LEFT
        item_y = _DIVIDER_Y + _TOC_PAD

        # Calculate total panel height
        total_h = _TOC_PAD
        for s in _SECTIONS:
            items = [i for i, (sec, _) in enumerate(self._slides) if sec == s]
            if items:
                total_h += _TOC_SECTION_H + len(items) * _TOC_ITEM_H
        total_h += _TOC_PAD

        panel_rect = pygame.Rect(
            panel_x - _TOC_PAD, _DIVIDER_Y, _TOC_PANEL_W + _TOC_PAD * 2, total_h
        )

        # Semi-transparent panel background
        panel_surf = pygame.Surface((panel_rect.w, panel_rect.h), pygame.SRCALPHA)
        panel_surf.fill(_TOC_PANEL_BG)
        surface.blit(panel_surf, (panel_rect.x, panel_rect.y))
        pygame.draw.rect(surface, _DIM, panel_rect, 1, border_radius=6)

        self._toc_item_rects = []

        for s in _SECTIONS:
            items = [(i, txt) for i, (sec, txt) in enumerate(self._slides) if sec == s]
            if not items:
                continue

            # Section heading
            sec_label = f"  {self._section_label(s)}  ({len(items)})"
            sec_surf = self._font_toc.render(sec_label, True, _ORANGE)
            surface.blit(sec_surf, (panel_x, item_y + 8))
            item_y += _TOC_SECTION_H

            for slide_idx, txt in items:
                item_rect = pygame.Rect(
                    panel_x - _TOC_PAD, item_y, _TOC_PANEL_W + _TOC_PAD, _TOC_ITEM_H
                )

                # Highlight current or hovered
                if slide_idx == self._idx:
                    pygame.draw.rect(surface, _TOC_ACTIVE_BG, item_rect)

                color = _ORANGE if slide_idx == self._idx else _WHITE
                preview_surf = self._font_toc.render(f"  · {_preview(txt)}", True, color)
                surface.blit(preview_surf, (panel_x, item_y + 6))
                self._toc_item_rects.append((slide_idx, item_rect))
                item_y += _TOC_ITEM_H

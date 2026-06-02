from __future__ import annotations

import importlib

import pygame

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene

_BG = (26, 26, 46)
_WHITE = (240, 240, 240)
_ORANGE = (243, 156, 18)
_DIM = (100, 100, 150)

_SECTIONS = ("theory", "notes", "tasks")
_LEFT = 40
_TAB_Y = 16
_DIVIDER_Y = 58
_TEXT_Y = 80
_HINT_Y_OFFSET = 36


def _load_content(lesson_num: int, lang: str) -> list[tuple[str, str]]:
    try:
        mod = importlib.import_module(
            f"cognitive_data_arcade.lessons.lesson_{lesson_num:02d}"
        )
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


class LessonReaderScene(Scene):
    def __init__(
        self,
        lesson_num: int,
        strings: Strings,
        back_scene: Scene | None,
    ) -> None:
        self._strings = strings
        self._back = back_scene
        self._done = False
        self._slides = _load_content(lesson_num, strings.language)
        self._idx = 0
        pygame.font.init()
        self._font_section = pygame.font.SysFont(None, 32)
        self._font_text = pygame.font.SysFont(None, 28)
        self._font_hint = pygame.font.SysFont(None, 24)

    def _section_label(self, section: str) -> str:
        return {
            "theory": self._strings.lesson_theory,
            "notes":  self._strings.lesson_notes,
            "tasks":  self._strings.lesson_tasks,
        }.get(section, section)

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self._slides:
            self._done = True
            return
        if event.type != pygame.KEYDOWN:
            return
        key = event.key
        if key == pygame.K_ESCAPE:
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
        return self._back if self._done else None

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
                    surface, _ORANGE,
                    (tab_x, underline_y),
                    (tab_x + surf.get_width(), underline_y),
                    2,
                )
            tab_x += surf.get_width() + 48

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

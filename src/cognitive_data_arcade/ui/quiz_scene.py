"""QuizScene — checkpoint multiple-choice question shown after a lesson."""

from __future__ import annotations

import pygame

from cognitive_data_arcade.data.quiz_data import get_question
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

_W, _H = 1024, 640
_BG = (13, 15, 26)
_SURFACE = (22, 24, 40)
_SURFACE2 = (30, 32, 56)
_ACCENT = (99, 102, 241)
_TEXT = (240, 241, 255)
_DIM = (90, 96, 144)
_GREEN = (74, 222, 128)
_RED = (231, 76, 60)


class QuizScene(Scene):
    """Single multiple-choice checkpoint question for lesson_num."""

    def __init__(
        self,
        lesson_num: int,
        pm: ProfileManager,
        strings: Strings,
        back_scene: Scene,
    ) -> None:
        self._lesson_num = lesson_num
        self._pm = pm
        self._strings = strings
        self._back = back_scene
        self._done = False
        self._next: Scene | None = None
        self._question = get_question(lesson_num)
        self._selected: int | None = None
        self._answered = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if self._answered:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                self._next = self._back
                self._done = True
            return
        if event.key == pygame.K_ESCAPE:
            self._next = self._back
            self._done = True
        elif event.key == pygame.K_1:
            self._selected = 0
        elif event.key == pygame.K_2:
            self._selected = 1
        elif event.key == pygame.K_3:
            self._selected = 2
        elif event.key in (pygame.K_RETURN, pygame.K_y) and self._selected is not None:
            self._confirm()

    def _confirm(self) -> None:
        correct = self._selected == self._question["correct"]
        self._pm.record_quiz_result(self._lesson_num, correct)
        self._answered = True
        self._next = self._back
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()
        if self._question is None:
            return
        is_pl = self._strings.language == "pl"

        # Header
        pygame.draw.rect(surface, _SURFACE, (0, 0, w, 52))
        pygame.draw.line(surface, _SURFACE2, (0, 52), (w, 52))
        hdr = get_font(16).render(
            f"Lekcja {self._lesson_num} - pytanie kontrolne"
            if is_pl
            else f"Lesson {self._lesson_num} - checkpoint",
            True,
            _DIM,
        )
        surface.blit(hdr, (32, 16))

        # Question
        q_key = "q_pl" if is_pl else "q_en"
        q_surf = get_font(24).render(self._question[q_key], True, _TEXT)
        surface.blit(q_surf, (w // 2 - q_surf.get_width() // 2, 80))

        # Options
        opts_key = "options_pl" if is_pl else "options_en"
        options = self._question[opts_key]
        correct_idx = self._question["correct"]
        opt_y = 150
        btn_w = w - 120
        btn_h = 52
        btn_x = 60

        for i, opt in enumerate(options):
            rect = pygame.Rect(btn_x, opt_y, btn_w, btn_h)

            if self._answered:
                if i == correct_idx:
                    bg, border = (20, 50, 30), _GREEN
                elif i == self._selected:
                    bg, border = (50, 20, 20), _RED
                else:
                    bg, border = _SURFACE, _SURFACE2
            elif self._selected == i:
                bg, border = (28, 32, 70), _ACCENT
            else:
                bg, border = _SURFACE, _SURFACE2

            pygame.draw.rect(surface, bg, rect, border_radius=8)
            pygame.draw.rect(surface, border, rect, 2, border_radius=8)

            num_surf = get_font(20).render(f"[{i + 1}]", True, _ACCENT)
            surface.blit(num_surf, (btn_x + 14, opt_y + (btn_h - num_surf.get_height()) // 2))

            opt_surf = get_font(20).render(opt, True, _TEXT)
            surface.blit(opt_surf, (btn_x + 56, opt_y + (btn_h - opt_surf.get_height()) // 2))

            opt_y += btn_h + 12

        # Hint
        if self._answered:
            hint_text = "SPACJA - dalej" if is_pl else "SPACE - continue"
        elif self._selected is not None:
            hint_text = (
                "ENTER - potwierdz  |  [1/2/3] - zmien"
                if is_pl
                else "ENTER - confirm  |  [1/2/3] - change"
            )
        else:
            hint_text = (
                "[1/2/3] - wybierz  |  ESC - pominij"
                if is_pl
                else "[1/2/3] - choose  |  ESC - skip"
            )
        hint = get_font(16).render(hint_text, True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 36))

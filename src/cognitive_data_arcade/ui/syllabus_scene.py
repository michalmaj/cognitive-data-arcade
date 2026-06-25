"""SyllabusScene — visual map of all 6 acts and their completion status."""

from __future__ import annotations

import pygame

from cognitive_data_arcade.data.act_content import ACT_INTROS
from cognitive_data_arcade.engine.badges import _MODULE_LESSONS
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
_DONE = (74, 222, 128)
_TOPBAR_H = 52


class SyllabusScene(Scene):
    """Shows 6 acts in a 2x3 grid with title, lesson count and completion status."""

    def __init__(self, pm: ProfileManager, strings: Strings, back_scene: Scene) -> None:
        self._pm = pm
        self._strings = strings
        self._back = back_scene
        self._done = False
        self._next: Scene | None = None
        profile = pm.load()
        completed = set(profile.completed_lessons)
        self._completed_acts: set[int] = {
            idx
            for idx, lessons in enumerate(_MODULE_LESSONS)
            if all(n in completed for n in lessons)
        }
        self._total_lessons = sum(len(lessons) for lessons in _MODULE_LESSONS)
        self._done_lessons = len(completed)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
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
        self._draw_topbar(surface)
        self._draw_grid(surface)
        self._draw_footer(surface)

    def _draw_topbar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _SURFACE, (0, 0, _W, _TOPBAR_H))
        pygame.draw.line(surface, _SURFACE2, (0, _TOPBAR_H), (_W, _TOPBAR_H))
        is_pl = self._strings.language == "pl"
        title_text = "Sylabus kursu" if is_pl else "Course Syllabus"
        title = get_font(24).render(title_text, True, _TEXT)
        surface.blit(
            title,
            (_W // 2 - title.get_width() // 2, _TOPBAR_H // 2 - title.get_height() // 2),
        )
        progress_text = f"{self._done_lessons} / {self._total_lessons}"
        prog = get_font(20).render(progress_text, True, _DONE)
        surface.blit(
            prog,
            (_W - prog.get_width() - 24, _TOPBAR_H // 2 - prog.get_height() // 2),
        )

    def _draw_grid(self, surface: pygame.Surface) -> None:
        is_pl = self._strings.language == "pl"
        cols, rows = 3, 2
        pad = 20
        card_w = (_W - pad * (cols + 1)) // cols
        card_h = (_H - _TOPBAR_H - 40 - pad * (rows + 1)) // rows

        for idx in range(6):
            col = idx % cols
            row = idx // cols
            cx = pad + col * (card_w + pad)
            cy = _TOPBAR_H + pad + row * (card_h + pad)
            rect = pygame.Rect(cx, cy, card_w, card_h)

            is_done = idx in self._completed_acts
            border_color = _DONE if is_done else _SURFACE2
            bg_color = (18, 22, 36) if is_done else _SURFACE

            pygame.draw.rect(surface, bg_color, rect, border_radius=8)
            pygame.draw.rect(surface, border_color, rect, 2, border_radius=8)

            act_num = get_font(13).render(
                f"AKT {idx + 1}" if is_pl else f"ACT {idx + 1}", True, _ACCENT
            )
            surface.blit(act_num, (cx + 12, cy + 10))

            content = ACT_INTROS[idx]
            title_key = "title_pl" if is_pl else "title_en"
            raw_title = content[title_key]
            short_title = raw_title.split(":", 1)[-1].strip() if ":" in raw_title else raw_title
            if len(short_title) > 24:
                short_title = short_title[:22] + ".."
            title_surf = get_font(18).render(short_title, True, _TEXT)
            surface.blit(title_surf, (cx + 12, cy + 28))

            lessons = _MODULE_LESSONS[idx]
            lesson_count = get_font(15).render(
                f"{len(lessons)} lekcji" if is_pl else f"{len(lessons)} lessons",
                True,
                _DIM,
            )
            surface.blit(lesson_count, (cx + 12, cy + card_h - 28))

            if is_done:
                done_surf = get_font(15).render("UKONCZONO" if is_pl else "DONE", True, _DONE)
                surface.blit(done_surf, (cx + card_w - done_surf.get_width() - 12, cy + 10))

    def _draw_footer(self, surface: pygame.Surface) -> None:
        is_pl = self._strings.language == "pl"
        hint_text = "ESC  powrot" if is_pl else "ESC  back"
        hint = get_font(16).render(hint_text, True, _DIM)
        surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 28))

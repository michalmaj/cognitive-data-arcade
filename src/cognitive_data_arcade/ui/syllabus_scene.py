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
_ACCENT_LIGHT = (129, 140, 248)
_TEXT = (240, 241, 255)
_DIM = (90, 96, 144)
_DONE = (74, 222, 128)
_HOVER_BORDER = (160, 163, 255)
_TOPBAR_H = 52


class SyllabusScene(Scene):
    """Shows 6 acts in a 2x3 grid with title, description, lesson count and completion."""

    def __init__(self, pm: ProfileManager, strings: Strings, back_scene: Scene) -> None:
        self._pm = pm
        self._strings = strings
        self._back = back_scene
        self._done = False
        self._next: Scene | None = None
        self._card_rects: list[pygame.Rect] = []
        self._hovered: int | None = None
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
        if event.type == pygame.MOUSEMOTION:
            self._hovered = self._card_at(event.pos)
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            idx = self._card_at(event.pos)
            if idx is not None:
                self._launch_act(idx)
            return
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self._next = self._back
            self._done = True

    def _card_at(self, pos: tuple[int, int]) -> int | None:
        for i, rect in enumerate(self._card_rects):
            if rect.collidepoint(pos):
                return i
        return None

    def _launch_act(self, module_idx: int) -> None:
        from cognitive_data_arcade.ui.act_intro_scene import ActIntroScene
        from cognitive_data_arcade.ui.module_runner_scene import ModuleRunnerScene

        runner = ModuleRunnerScene(module_idx, self._pm, self._strings)
        fresh_syllabus = SyllabusScene(self._pm, self._strings, self._back)
        intro = ActIntroScene(
            module_idx=module_idx,
            pm=self._pm,
            strings=self._strings,
            back_scene=fresh_syllabus,
            confirm_scene=runner,
        )
        self._next = intro
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
        pad = 16
        card_w = (_W - pad * (cols + 1)) // cols
        card_h = (_H - _TOPBAR_H - 32 - pad * (rows + 1)) // rows
        self._card_rects = []

        for idx in range(6):
            col = idx % cols
            row = idx // cols
            cx = pad + col * (card_w + pad)
            cy = _TOPBAR_H + pad + row * (card_h + pad)
            rect = pygame.Rect(cx, cy, card_w, card_h)
            self._card_rects.append(rect)

            is_done = idx in self._completed_acts
            is_hovered = idx == self._hovered

            bg_color = (18, 22, 36) if is_done else _SURFACE
            if is_hovered:
                border_color = _HOVER_BORDER
                border_w = 2
            elif is_done:
                border_color = _DONE
                border_w = 2
            else:
                border_color = _SURFACE2
                border_w = 1

            pygame.draw.rect(surface, bg_color, rect, border_radius=8)
            pygame.draw.rect(surface, border_color, rect, border_w, border_radius=8)

            # Act chip
            act_label = f"AKT {idx + 1}" if is_pl else f"ACT {idx + 1}"
            act_surf = get_font(13).render(act_label, True, _ACCENT)
            surface.blit(act_surf, (cx + 12, cy + 10))

            # DONE badge (top-right)
            if is_done:
                done_label = "UKOŃCZONO" if is_pl else "DONE"
                done_surf = get_font(13).render(done_label, True, _DONE)
                surface.blit(done_surf, (cx + card_w - done_surf.get_width() - 12, cy + 10))

            # Short title (Unicode OK — Space Grotesk)
            title_key = "short_title_pl" if is_pl else "short_title_en"
            title_surf = get_font(18).render(ACT_INTROS[idx][title_key], True, _TEXT)
            surface.blit(title_surf, (cx + 12, cy + 30))

            # Description (2 lines)
            desc_key = "desc_pl" if is_pl else "desc_en"
            desc_font = get_font(14)
            desc_y = cy + 56
            for line in ACT_INTROS[idx][desc_key].split("\n"):
                if not line.strip():
                    continue
                ds = desc_font.render(line, True, _DIM)
                surface.blit(ds, (cx + 12, desc_y))
                desc_y += desc_font.get_height() + 2

            # Lesson count (bottom)
            lessons = _MODULE_LESSONS[idx]
            count_text = f"{len(lessons)} lekcji" if is_pl else f"{len(lessons)} lessons"
            count_surf = get_font(13).render(count_text, True, _DIM)
            surface.blit(count_surf, (cx + 12, cy + card_h - 24))

            # Hover arrow hint
            if is_hovered:
                arrow = get_font(13).render(
                    "kliknij aby zacząć >" if is_pl else "click to start >", True, _ACCENT_LIGHT
                )
                surface.blit(arrow, (cx + card_w - arrow.get_width() - 12, cy + card_h - 24))

    def _draw_footer(self, surface: pygame.Surface) -> None:
        is_pl = self._strings.language == "pl"
        hint_text = (
            "ESC  powrót  |  kliknij akt aby przejść do intro"
            if is_pl
            else "ESC  back  |  click an act to open its intro"
        )
        hint = get_font(15).render(hint_text, True, _DIM)
        surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 26))

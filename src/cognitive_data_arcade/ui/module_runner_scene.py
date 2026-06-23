# src/cognitive_data_arcade/ui/module_runner_scene.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font, get_font_medium
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.menu import _LESSON_DATA, _MODULES

_W, _H = 1024, 640
_BG = (13, 15, 26)
_SURFACE = (22, 24, 40)
_SURFACE2 = (30, 32, 56)
_ACCENT = (99, 102, 241)
_ACCENT_LIGHT = (129, 140, 248)
_TEXT = (240, 241, 255)
_TEXT_DIM = (90, 96, 144)
_TEXT_DARK = (61, 64, 96)
_DONE_COLOR = (74, 222, 128)
_TOPBAR_H = 56
_HINTBAR_H = 28


def _module_lessons(module_idx: int) -> list[dict]:
    """Return the LESSON_DATA dicts for the given module index (0-5)."""
    _, _, start, count = _MODULES[module_idx]
    return _LESSON_DATA[start : start + count]


class ModuleRunnerScene(Scene):
    def __init__(self, module_idx: int, pm: ProfileManager, strings: Strings) -> None:
        self._module_idx = module_idx
        self._pm = pm
        self._strings = strings
        self._lessons = _module_lessons(module_idx)
        profile = pm.load()
        self._completed: set[int] = set(profile.completed_lessons)
        self._current_step = self._find_current_step(self._completed)
        self._done = False
        self._next: Scene | None = None
        self._zagraj_rect: pygame.Rect | None = None
        self._teoria_rect: pygame.Rect | None = None

    def _find_current_step(self, completed: set[int]) -> int:
        for i, lesson in enumerate(self._lessons):
            if lesson["num"] not in completed:
                return i
        return len(self._lessons) - 1

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)
            return
        k = event.key
        if k == pygame.K_ESCAPE:
            from cognitive_data_arcade.ui.menu import LessonMenuScene

            self._next = LessonMenuScene(self._pm, self._strings)
            self._done = True
        elif k in (pygame.K_RIGHT, pygame.K_DOWN):
            self._current_step = min(len(self._lessons) - 1, self._current_step + 1)
        elif k in (pygame.K_LEFT, pygame.K_UP):
            self._current_step = max(0, self._current_step - 1)
        elif k == pygame.K_RETURN:
            self._launch_game()
        elif k == pygame.K_t:
            self._launch_teoria()

    def _handle_click(self, pos: tuple[int, int]) -> None:
        if self._zagraj_rect and self._zagraj_rect.collidepoint(pos):
            self._launch_game()
        elif self._teoria_rect and self._teoria_rect.collidepoint(pos):
            self._launch_teoria()

    def _current_lesson(self) -> dict:
        return self._lessons[self._current_step]

    def _launch_game(self) -> None:
        from cognitive_data_arcade.ui.game_launcher import game_factory_for

        lesson_num = self._current_lesson()["num"]
        factory = game_factory_for(lesson_num, self._pm, self._strings)
        if factory is None:
            return
        self._next = factory()
        self._done = True

    def _launch_teoria(self) -> None:
        from cognitive_data_arcade.ui.game_launcher import game_factory_for
        from cognitive_data_arcade.ui.lesson_reader import LessonReaderScene

        lesson_num = self._current_lesson()["num"]
        back = ModuleRunnerScene(self._module_idx, self._pm, self._strings)
        self._next = LessonReaderScene(
            lesson_num,
            self._strings,
            back,
            play_factory=game_factory_for(lesson_num, self._pm, self._strings),
        )
        self._done = True

    def _refresh_and_check_complete(self) -> None:
        profile = self._pm.load()
        self._completed = set(profile.completed_lessons)
        self._current_step = self._find_current_step(self._completed)
        lesson_nums = {d["num"] for d in self._lessons}
        if lesson_nums.issubset(self._completed):
            self._pm.clear_current_module()
            try:
                from cognitive_data_arcade.ui.module_complete_scene import (
                    ModuleCompleteScene,
                )

                self._next = ModuleCompleteScene(self._module_idx, self._pm, self._strings)
                self._done = True
            except ImportError:
                pass

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_topbar(surface)
        self._draw_stepper(surface)
        self._draw_lesson_card(surface)
        self._draw_mini_bar(surface)
        self._draw_hintbar(surface)

    def _draw_topbar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _SURFACE, (0, 0, _W, _TOPBAR_H))
        pygame.draw.line(surface, _SURFACE2, (0, _TOPBAR_H), (_W, _TOPBAR_H))

        back_lbl = get_font(20).render("<  menu", True, _TEXT_DARK)
        surface.blit(back_lbl, (20, (_TOPBAR_H - back_lbl.get_height()) // 2))

        lang = self._strings.language
        mname = _MODULES[self._module_idx][0] if lang == "pl" else _MODULES[self._module_idx][1]
        title = get_font_medium(22).render(mname, True, _TEXT)
        surface.blit(
            title, (_W // 2 - title.get_width() // 2, (_TOPBAR_H - title.get_height()) // 2)
        )

        done_in_module = sum(1 for d in self._lessons if d["num"] in self._completed)
        count_lbl = get_font(20).render(
            f"{done_in_module} / {len(self._lessons)}", True, _DONE_COLOR
        )
        surface.blit(
            count_lbl,
            (_W - count_lbl.get_width() - 20, (_TOPBAR_H - count_lbl.get_height()) // 2),
        )

    def _draw_stepper(self, surface: pygame.Surface) -> None:
        n = len(self._lessons)
        circle_r = 14
        y_center = _TOPBAR_H + 38
        total_w = _W - 120
        step_w = total_w // (n - 1) if n > 1 else 0
        x_start = 60

        for i in range(n):
            cx = x_start + i * step_w
            lesson_num = self._lessons[i]["num"]
            is_done = lesson_num in self._completed
            is_current = i == self._current_step

            if i < n - 1:
                nx = x_start + (i + 1) * step_w
                line_color = _DONE_COLOR if is_done else _SURFACE2
                pygame.draw.line(
                    surface, line_color, (cx + circle_r, y_center), (nx - circle_r, y_center), 2
                )

            if is_done:
                pygame.draw.circle(surface, _DONE_COLOR, (cx, y_center), circle_r)
                num_surf = get_font(13).render(str(i + 1), True, _BG)
            elif is_current:
                pygame.draw.circle(surface, _ACCENT, (cx, y_center), circle_r)
                pygame.draw.circle(surface, _ACCENT_LIGHT, (cx, y_center), circle_r, 2)
                num_surf = get_font(13).render(str(i + 1), True, _TEXT)
            else:
                pygame.draw.circle(surface, _SURFACE2, (cx, y_center), circle_r)
                num_surf = get_font(13).render(str(i + 1), True, _TEXT_DARK)
            surface.blit(
                num_surf, (cx - num_surf.get_width() // 2, y_center - num_surf.get_height() // 2)
            )

    def _draw_lesson_card(self, surface: pygame.Surface) -> None:
        lesson = self._current_lesson()
        card_w, card_h = 520, 210
        card_x = (_W - card_w) // 2
        card_y = _TOPBAR_H + 80

        pygame.draw.rect(surface, _SURFACE, (card_x, card_y, card_w, card_h), border_radius=8)
        pygame.draw.rect(surface, _ACCENT, (card_x, card_y, card_w, card_h), 1, border_radius=8)

        lang = self._strings.language
        step_lbl = get_font(16).render(
            f"KROK {self._current_step + 1} Z {len(self._lessons)}"
            if lang == "pl"
            else f"STEP {self._current_step + 1} OF {len(self._lessons)}",
            True,
            _ACCENT_LIGHT,
        )
        surface.blit(step_lbl, (card_x + 20, card_y + 14))

        name_surf = get_font_medium(26).render(lesson["name"], True, _TEXT)
        surface.blit(name_surf, (card_x + 20, card_y + 38))

        type_color = {
            "arcade": _ACCENT,
            "lab": (34, 211, 238),
            "puzzle": (251, 191, 36),
        }.get(lesson["type"], _TEXT_DIM)
        type_surf = get_font(18).render(lesson["type"], True, type_color)
        surface.blit(type_surf, (card_x + 20, card_y + 70))

        desc = lesson.get("desc_pl" if lang == "pl" else "desc_en", "")
        first_line = desc.split("\n")[0] if desc else ""
        desc_surf = get_font(18).render(first_line, True, _TEXT_DIM)
        surface.blit(desc_surf, (card_x + 20, card_y + 94))

        btn_w = (card_w - 60) // 2
        btn_h = 38
        btn_y = card_y + card_h - btn_h - 16

        teoria_x = card_x + 20
        self._teoria_rect = pygame.Rect(teoria_x, btn_y, btn_w, btn_h)
        pygame.draw.rect(surface, _SURFACE2, self._teoria_rect, border_radius=5)
        pygame.draw.rect(surface, _TEXT_DARK, self._teoria_rect, 1, border_radius=5)
        t_lbl = get_font(18).render("Teoria" if lang == "pl" else "Theory", True, _TEXT)
        surface.blit(
            t_lbl,
            (
                teoria_x + btn_w // 2 - t_lbl.get_width() // 2,
                btn_y + (btn_h - t_lbl.get_height()) // 2,
            ),
        )

        zagraj_x = card_x + 40 + btn_w
        self._zagraj_rect = pygame.Rect(zagraj_x, btn_y, btn_w, btn_h)
        pygame.draw.rect(surface, _ACCENT, self._zagraj_rect, border_radius=5)
        z_lbl = get_font_medium(18).render("Zagraj" if lang == "pl" else "Play", True, _TEXT)
        surface.blit(
            z_lbl,
            (
                zagraj_x + btn_w // 2 - z_lbl.get_width() // 2,
                btn_y + (btn_h - z_lbl.get_height()) // 2,
            ),
        )

    def _draw_mini_bar(self, surface: pygame.Surface) -> None:
        n = len(self._lessons)
        bar_y = _TOPBAR_H + 310
        cell_w = min(80, (_W - 80) // n)
        total_w = n * cell_w + (n - 1) * 4
        bar_x = (_W - total_w) // 2

        for i, lesson in enumerate(self._lessons):
            bx = bar_x + i * (cell_w + 4)
            is_done = lesson["num"] in self._completed
            is_current = i == self._current_step
            if is_done:
                bg, fg = _SURFACE, _DONE_COLOR
            elif is_current:
                bg, fg = _ACCENT, _TEXT
            else:
                bg, fg = _BG, _TEXT_DARK
            pygame.draw.rect(surface, bg, (bx, bar_y, cell_w, 24), border_radius=3)
            if is_current:
                pygame.draw.rect(
                    surface, _ACCENT_LIGHT, (bx, bar_y, cell_w, 24), 1, border_radius=3
                )
            lbl = get_font(13).render(f"L{lesson['num']:02d}", True, fg)
            surface.blit(lbl, (bx + cell_w // 2 - lbl.get_width() // 2, bar_y + 5))

    def _draw_hintbar(self, surface: pygame.Surface) -> None:
        hint_y = _H - _HINTBAR_H
        pygame.draw.rect(surface, _SURFACE, (0, hint_y, _W, _HINTBAR_H))
        lang = self._strings.language
        if lang == "pl":
            txt = "strzalki = prev/next  |  ENTER = Zagraj  |  T = Teoria  |  ESC = menu"
        else:
            txt = "arrows = prev/next  |  ENTER = Play  |  T = Theory  |  ESC = menu"
        hint = get_font(16).render(txt, True, _TEXT_DARK)
        surface.blit(
            hint,
            (_W // 2 - hint.get_width() // 2, hint_y + (_HINTBAR_H - hint.get_height()) // 2),
        )

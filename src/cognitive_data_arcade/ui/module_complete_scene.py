# src/cognitive_data_arcade/ui/module_complete_scene.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.data.act_content import ACT_BRIDGES
from cognitive_data_arcade.data.home_prompts import HOME_PROMPTS
from cognitive_data_arcade.engine.badges import _MODULE_BADGES, load_badge_icon
from cognitive_data_arcade.engine.fonts import get_font, get_font_medium
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.menu import _MODULES

_W, _H = 1024, 640
_BG = (13, 15, 26)
_SURFACE = (22, 24, 40)
_SURFACE2 = (30, 32, 56)
_ACCENT = (99, 102, 241)
_ACCENT_LIGHT = (129, 140, 248)
_TEXT = (240, 241, 255)
_TEXT_DIM = (90, 96, 144)
_DONE_COLOR = (74, 222, 128)
_NUM_MODULES = 6


class ModuleCompleteScene(Scene):
    def __init__(self, module_idx: int, pm: ProfileManager, strings: Strings) -> None:
        self._module_idx = module_idx
        self._pm = pm
        self._strings = strings
        pm.clear_current_module()
        profile = pm.load()
        self._total_lessons_done = len(profile.completed_lessons)
        self._badge = _MODULE_BADGES[module_idx]
        self._icon = load_badge_icon(self._badge, size=72)
        self._done = False
        self._next: Scene | None = None
        self._next_btn_rect: pygame.Rect | None = None
        self._menu_btn_rect: pygame.Rect | None = None
        self._home_btn_rect: pygame.Rect | None = None
        self._show_home_prompt = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_click(event.pos)
            return
        if event.type != pygame.KEYDOWN:
            return
        k = event.key
        if k == pygame.K_ESCAPE:
            if self._show_home_prompt:
                self._show_home_prompt = False
            else:
                self._go_menu()
        elif k == pygame.K_RETURN:
            if self._module_idx < _NUM_MODULES - 1:
                self._go_next_module()
            else:
                self._go_menu()

    def _handle_click(self, pos: tuple[int, int]) -> None:
        if self._menu_btn_rect and self._menu_btn_rect.collidepoint(pos):
            self._go_menu()
        elif self._next_btn_rect and self._next_btn_rect.collidepoint(pos):
            self._go_next_module()
        elif self._home_btn_rect and self._home_btn_rect.collidepoint(pos):
            self._show_home_prompt = not self._show_home_prompt

    def _go_menu(self) -> None:
        from cognitive_data_arcade.ui.menu import LessonMenuScene

        self._next = LessonMenuScene(self._pm, self._strings)
        self._done = True

    def _go_next_module(self) -> None:
        from cognitive_data_arcade.ui.module_runner_scene import ModuleRunnerScene
        from cognitive_data_arcade.ui.act_intro_scene import make_act_intro

        next_idx = self._module_idx + 1
        self._pm.set_current_module(next_idx)
        runner = ModuleRunnerScene(next_idx, self._pm, self._strings)
        self._next = make_act_intro(self._pm, next_idx, self._strings, back_scene=runner)
        self._done = True

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        cx, cy = _W // 2, _H // 2 - 40
        lang = self._strings.language

        # badge glow circle
        pygame.draw.circle(surface, (20, 60, 30), (cx, cy - 60), 52)
        pygame.draw.circle(surface, _DONE_COLOR, (cx, cy - 60), 52, 2)

        # badge icon
        if self._icon:
            surface.blit(self._icon, (cx - 36, cy - 96))

        # "MODULE COMPLETE" label
        done_lbl = get_font(16).render(
            "MODUL UKONCZONY" if lang == "pl" else "MODULE COMPLETE",
            True,
            _DONE_COLOR,
        )
        surface.blit(done_lbl, (cx - done_lbl.get_width() // 2, cy - 0))

        # module name
        mname = _MODULES[self._module_idx][0] if lang == "pl" else _MODULES[self._module_idx][1]
        name_surf = get_font_medium(30).render(mname, True, _TEXT)
        surface.blit(name_surf, (cx - name_surf.get_width() // 2, cy + 24))

        # badge name
        badge_name = self._badge.name_pl if lang == "pl" else self._badge.name_en
        badge_lbl = get_font(20).render(
            f"{badge_name}  --  " + ("odblokowana!" if lang == "pl" else "unlocked!"),
            True,
            _ACCENT_LIGHT,
        )
        surface.blit(badge_lbl, (cx - badge_lbl.get_width() // 2, cy + 64))

        # mini stats
        total_surf = get_font(18).render(
            f"{self._total_lessons_done} / 31 "
            + ("lekcji ogolnie" if lang == "pl" else "lessons total"),
            True,
            _TEXT_DIM,
        )
        surface.blit(total_surf, (cx - total_surf.get_width() // 2, cy + 98))

        # buttons
        btn_w, btn_h = 180, 42
        btn_y = cy + 140

        # menu button (always shown)
        menu_x = cx - btn_w - 12
        self._menu_btn_rect = pygame.Rect(menu_x, btn_y, btn_w, btn_h)
        pygame.draw.rect(surface, _SURFACE2, self._menu_btn_rect, border_radius=6)
        pygame.draw.rect(surface, _TEXT_DIM, self._menu_btn_rect, 1, border_radius=6)
        ml = get_font(18).render("<  menu", True, _TEXT_DIM)
        surface.blit(
            ml,
            (menu_x + btn_w // 2 - ml.get_width() // 2, btn_y + (btn_h - ml.get_height()) // 2),
        )

        # next module button (only if not last)
        if self._module_idx < _NUM_MODULES - 1:
            next_x = cx + 12
            self._next_btn_rect = pygame.Rect(next_x, btn_y, btn_w, btn_h)
            pygame.draw.rect(surface, _ACCENT, self._next_btn_rect, border_radius=6)
            nl = get_font_medium(18).render(
                f"Modul {self._module_idx + 2}  >"
                if lang == "pl"
                else f"Module {self._module_idx + 2}  >",
                True,
                _TEXT,
            )
            surface.blit(
                nl,
                (
                    next_x + btn_w // 2 - nl.get_width() // 2,
                    btn_y + (btn_h - nl.get_height()) // 2,
                ),
            )
        else:
            self._next_btn_rect = None

        # "Do domu / Take home" button
        _ORANGE = (251, 146, 60)
        home_btn_w, home_btn_h = 300, 36
        home_btn_x = cx - home_btn_w // 2
        home_btn_y = btn_y + btn_h + 10
        self._home_btn_rect = pygame.Rect(home_btn_x, home_btn_y, home_btn_w, home_btn_h)
        pygame.draw.rect(surface, _BG, self._home_btn_rect, border_radius=6)
        pygame.draw.rect(surface, _ORANGE, self._home_btn_rect, 1, border_radius=6)
        home_lbl_text = (
            "Co zrobic przed kolejnymi zajeciami?"
            if lang == "pl"
            else "What to do before the next session?"
        )
        home_lbl = get_font(14).render(home_lbl_text, True, _ORANGE)
        surface.blit(
            home_lbl,
            (
                cx - home_lbl.get_width() // 2,
                home_btn_y + (home_btn_h - home_lbl.get_height()) // 2,
            ),
        )

        # Bridge narrative text (below the home button)
        bridge_key = "text_pl" if lang == "pl" else "text_en"
        bridge_text = ACT_BRIDGES[self._module_idx][bridge_key]
        bridge_font = get_font(16)
        bridge_y = home_btn_y + home_btn_h + 12
        for bline in bridge_text.split("\n"):
            bline = bline.strip()
            if bline:
                bs = bridge_font.render(bline, True, (90, 96, 144))
                surface.blit(bs, (cx - bs.get_width() // 2, bridge_y))
                bridge_y += bridge_font.get_height() + 4

        # Overlay with home prompt text
        if self._show_home_prompt and self._module_idx in HOME_PROMPTS:
            prompt_text = HOME_PROMPTS[self._module_idx][lang]
            sw, sh = surface.get_size()
            ov = pygame.Surface((sw, sh), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 200))
            surface.blit(ov, (0, 0))
            pw2, ph2 = 560, 280
            px2 = (sw - pw2) // 2
            py2 = (sh - ph2) // 2
            pygame.draw.rect(surface, _SURFACE, (px2, py2, pw2, ph2), border_radius=10)
            pygame.draw.rect(surface, _ORANGE, (px2, py2, pw2, ph2), 2, border_radius=10)
            title_lbl = "Przed kolejnymi zajeciami" if lang == "pl" else "Before the next session"
            ts = get_font(18).render(title_lbl, True, _ORANGE)
            surface.blit(ts, (cx - ts.get_width() // 2, py2 + 14))
            line_y = py2 + 50
            for line in prompt_text.split("\n"):
                line = line.strip()
                if line:
                    ls = get_font(15).render(line, True, _TEXT)
                    surface.blit(ls, (cx - ls.get_width() // 2, line_y))
                    line_y += 26
            close_hint = get_font(13).render(
                "ESC / kliknij ponownie aby zamknac"
                if lang == "pl"
                else "ESC / click again to close",
                True,
                _TEXT_DIM,
            )
            surface.blit(close_hint, (cx - close_hint.get_width() // 2, py2 + ph2 - 28))

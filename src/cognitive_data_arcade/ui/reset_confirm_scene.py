from __future__ import annotations

import pygame
from cognitive_data_arcade.engine.colors import BG as _BG, WHITE as _WHITE
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

_W, _H = 1024, 768
_PANEL_BG = (14, 14, 36)
_BORDER = (42, 42, 80)
_DIM = (80, 80, 120)
_AMBER = (240, 165, 0)
_RED = (231, 76, 60)
_GREEN = (46, 204, 113)

# One row per reset option: (label_pl, label_en, accent_color)
_OPTIONS = [
    ("Wyczysc punkty i odznaki", "Clear points and badges", _AMBER),
    ("Zresetuj postep modulow", "Reset module progress", (220, 130, 30)),
    ("Pelny reset", "Full reset", _RED),
]

_CONFIRM_TEXTS_PL = [
    "Wyczysc {ap} pkt i {nb} odznak?",
    "Zresetowac postep modulow?",
    "UWAGA! To usunie caly postep! Jestes pewien?",
]
_CONFIRM_TEXTS_EN = [
    "Clear {ap} pts and {nb} badges?",
    "Reset module progress?",
    "WARNING! This deletes all progress! Are you sure?",
]


class ResetConfirmScene(Scene):
    def __init__(
        self,
        pm: ProfileManager,
        strings: Strings,
        profile_back_scene: Scene,
    ) -> None:
        self._pm = pm
        self._strings = strings
        self._profile_back = profile_back_scene
        self._state = "choosing"  # "choosing" | "confirming"
        self._selected: int | None = None
        self._confirm_profile = None
        self._done = False
        self._next: Scene | None = None

    # ------------------------------------------------------------------
    # Scene protocol
    # ------------------------------------------------------------------

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if self._state == "choosing":
            self._handle_choosing(event.key)
        else:
            self._handle_confirming(event.key)

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _handle_choosing(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            self._exit_to_profile()
        elif key == pygame.K_1:
            self._selected = 0
            self._confirm_profile = self._pm.load()
            self._state = "confirming"
        elif key == pygame.K_2:
            self._selected = 1
            self._confirm_profile = self._pm.load()
            self._state = "confirming"
        elif key == pygame.K_3:
            self._selected = 2
            self._confirm_profile = self._pm.load()
            self._state = "confirming"

    def _handle_confirming(self, key: int) -> None:
        if key in (pygame.K_RETURN, pygame.K_y):
            self._execute_reset()
        elif key in (pygame.K_ESCAPE, pygame.K_n):
            self._state = "choosing"

    def _execute_reset(self) -> None:
        if self._selected == 0:
            self._pm.reset_progress()
        elif self._selected == 1:
            self._pm.reset_module_progress()
        elif self._selected == 2:
            self._pm.reset_all()
        self._exit_to_profile()

    def _exit_to_profile(self) -> None:
        from cognitive_data_arcade.ui.profile_screen import ProfileScene

        self._next = ProfileScene(self._pm, self._strings, self._profile_back)
        self._done = True

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)

        # Semi-transparent overlay
        overlay = pygame.Surface((_W, _H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        panel_w, panel_h = 620, 380
        px = (_W - panel_w) // 2
        py = (_H - panel_h) // 2
        pygame.draw.rect(surface, _PANEL_BG, (px, py, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(surface, _BORDER, (px, py, panel_w, panel_h), 2, border_radius=12)

        if self._state == "choosing":
            self._draw_choosing(surface, px, py, panel_w, panel_h)
        else:
            self._draw_confirming(surface, px, py, panel_w, panel_h)

    def _draw_choosing(self, surface: pygame.Surface, px: int, py: int, pw: int, ph: int) -> None:
        is_pl = self._strings.language == "pl"
        title = "Resetuj postep" if is_pl else "Reset Progress"
        t_surf = get_font(28).render(title, True, _WHITE)
        surface.blit(t_surf, (px + pw // 2 - t_surf.get_width() // 2, py + 20))

        btn_h = 52
        btn_gap = 14
        btn_w = pw - 60
        bx = px + 30
        by = py + 72

        for i, (lbl_pl, lbl_en, color) in enumerate(_OPTIONS):
            rect = pygame.Rect(bx, by, btn_w, btn_h)
            pygame.draw.rect(surface, (20, 20, 50), rect, border_radius=8)
            pygame.draw.rect(surface, color, rect, 2, border_radius=8)
            num = get_font(22).render(f"[{i + 1}]", True, color)
            surface.blit(num, (bx + 12, by + (btn_h - num.get_height()) // 2))
            label = lbl_pl if is_pl else lbl_en
            lbl_surf = get_font(22).render(label, True, _WHITE)
            surface.blit(lbl_surf, (bx + 52, by + (btn_h - lbl_surf.get_height()) // 2))
            by += btn_h + btn_gap

        hint = "ESC  anuluj" if is_pl else "ESC  cancel"
        h_surf = get_font(14).render(hint, True, _DIM)
        surface.blit(h_surf, (px + pw // 2 - h_surf.get_width() // 2, py + ph - 28))

    def _draw_confirming(self, surface: pygame.Surface, px: int, py: int, pw: int, ph: int) -> None:
        is_pl = self._strings.language == "pl"
        profile = self._confirm_profile

        lbl_pl, lbl_en, color = _OPTIONS[self._selected]
        option_name = lbl_pl if is_pl else lbl_en

        # Selected option label
        opt_surf = get_font(20).render(option_name, True, color)
        surface.blit(opt_surf, (px + pw // 2 - opt_surf.get_width() // 2, py + 28))

        # Confirmation question
        texts = _CONFIRM_TEXTS_PL if is_pl else _CONFIRM_TEXTS_EN
        question = texts[self._selected].format(
            ap=profile.arcade_points,
            nb=len(profile.badges),
        )
        q_surf = get_font(22).render(question, True, _WHITE)
        surface.blit(q_surf, (px + pw // 2 - q_surf.get_width() // 2, py + 90))

        # TAK / NIE buttons
        btn_w, btn_h = 160, 48
        gap = 30
        total_w = btn_w * 2 + gap
        bx = px + (pw - total_w) // 2
        by = py + ph - 100

        # TAK (yes)
        yes_rect = pygame.Rect(bx, by, btn_w, btn_h)
        pygame.draw.rect(surface, (20, 20, 50), yes_rect, border_radius=8)
        pygame.draw.rect(surface, _RED, yes_rect, 2, border_radius=8)
        yes_lbl = "TAK (ENTER)" if is_pl else "YES (ENTER)"
        y_surf = get_font(18).render(yes_lbl, True, _RED)
        surface.blit(
            y_surf,
            (bx + btn_w // 2 - y_surf.get_width() // 2, by + (btn_h - y_surf.get_height()) // 2),
        )

        # NIE (no)
        no_rect = pygame.Rect(bx + btn_w + gap, by, btn_w, btn_h)
        pygame.draw.rect(surface, (20, 20, 50), no_rect, border_radius=8)
        pygame.draw.rect(surface, _GREEN, no_rect, 2, border_radius=8)
        no_lbl = "NIE (ESC)" if is_pl else "NO (ESC)"
        n_surf = get_font(18).render(no_lbl, True, _GREEN)
        surface.blit(
            n_surf,
            (
                no_rect.x + btn_w // 2 - n_surf.get_width() // 2,
                by + (btn_h - n_surf.get_height()) // 2,
            ),
        )

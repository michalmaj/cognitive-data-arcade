from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.colors import BG as _BG
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene

_W, _H = 1024, 768
_PANEL_BG = (14, 14, 36)
_BORDER = (42, 42, 80)
_DIM = (80, 80, 120)
_RED = (231, 76, 60)
_GREEN = (46, 204, 113)
_WHITE = (240, 241, 255)


class LogoutConfirmScene(Scene):
    """Confirmation overlay before deleting profile and all CSV data.

    profile_back_scene: the scene that ProfileScene uses as its back (e.g. LessonMenuScene).
    On cancel, a fresh ProfileScene is created with this as its back — avoids routing
    to a stale ProfileScene instance that already has _next set.
    """

    def __init__(
        self,
        pm,
        strings: Strings,
        profile_back_scene: Scene | None = None,
    ) -> None:
        self._pm = pm
        self._strings = strings
        self._profile_back = profile_back_scene
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_RETURN:
            self._confirm_logout()
        elif event.key == pygame.K_ESCAPE:
            self._cancel()

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def _confirm_logout(self) -> None:
        self._pm.delete_profile()
        from cognitive_data_arcade.ui.onboarding_scene import OnboardingScene

        self._next = OnboardingScene(self._pm)
        self._done = True

    def _cancel(self) -> None:
        if self._profile_back is not None:
            from cognitive_data_arcade.ui.profile_screen import ProfileScene

            self._next = ProfileScene(self._pm, self._strings, self._profile_back)
        self._done = True

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        overlay = pygame.Surface((_W, _H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        pw, ph = 560, 260
        px = (_W - pw) // 2
        py = (_H - ph) // 2
        pygame.draw.rect(surface, _PANEL_BG, (px, py, pw, ph), border_radius=12)
        pygame.draw.rect(surface, _RED, (px, py, pw, ph), 2, border_radius=12)

        is_pl = self._strings.language == "pl"
        title = "Wyloguj i zresetuj dane" if is_pl else "Log out & reset data"
        t_surf = get_font(26).render(title, True, _RED)
        surface.blit(t_surf, (px + pw // 2 - t_surf.get_width() // 2, py + 22))

        warning = (
            "To usunie Twoj profil i wszystkie zapisane dane (CSV)."
            if is_pl
            else "This will delete your profile and all saved data (CSV files)."
        )
        warning2 = "Nie mozna cofnac." if is_pl else "This cannot be undone."
        for i, line in enumerate([warning, warning2]):
            s = get_font(17).render(line, True, _WHITE)
            surface.blit(s, (px + pw // 2 - s.get_width() // 2, py + 72 + i * 28))

        btn_w, btn_h = 160, 46
        gap = 30
        total_bw = btn_w * 2 + gap
        bx = px + (pw - total_bw) // 2
        by = py + ph - 80

        yes_rect = pygame.Rect(bx, by, btn_w, btn_h)
        pygame.draw.rect(surface, (20, 20, 50), yes_rect, border_radius=8)
        pygame.draw.rect(surface, _RED, yes_rect, 2, border_radius=8)
        yes_lbl = "TAK (ENTER)" if is_pl else "YES (ENTER)"
        ys = get_font(17).render(yes_lbl, True, _RED)
        surface.blit(
            ys, (yes_rect.centerx - ys.get_width() // 2, yes_rect.centery - ys.get_height() // 2)
        )

        no_rect = pygame.Rect(bx + btn_w + gap, by, btn_w, btn_h)
        pygame.draw.rect(surface, (20, 20, 50), no_rect, border_radius=8)
        pygame.draw.rect(surface, _GREEN, no_rect, 2, border_radius=8)
        no_lbl = "NIE (ESC)" if is_pl else "NO (ESC)"
        ns = get_font(17).render(no_lbl, True, _GREEN)
        surface.blit(
            ns, (no_rect.centerx - ns.get_width() // 2, no_rect.centery - ns.get_height() // 2)
        )

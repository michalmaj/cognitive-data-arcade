from __future__ import annotations
import pygame
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.recommendation_bubble.game_state import (
    GameState,
    CATEGORIES,
    CAT_COLORS,
    diversity,
    profile_from_clicks,
)

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
)

_W, _H = 1024, 768
_PANEL = (20, 14, 30)
_C_USER = (155, 89, 182)

_ACT_SECS = 30.0
_EXT_SECS = 10.0
_MIN_CLICKS = 5

_BAR_X = 80
_BAR_W = 864
_BAR_H = 70
_BAR_ROWS = [pygame.Rect(_BAR_X, 120 + i * 90, _BAR_W, _BAR_H) for i in range(len(CATEGORIES))]


class PhaseUserScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._clicks: dict[str, int] = {cat: 0 for cat in CATEGORIES}
        self._timer = 0.0
        self._limit = _ACT_SECS * 1000.0
        self._show_hint = False
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(_BAR_ROWS):
                if rect.collidepoint(event.pos):
                    self._clicks[CATEGORIES[i]] += 1
                    break

    def update(self, dt_ms: float = 0.0) -> None:
        self._timer += dt_ms
        if self._timer >= self._limit:
            total = sum(self._clicks.values())
            if total >= _MIN_CLICKS:
                self._finalise()
            else:
                self._limit += _EXT_SECS * 1000.0
                self._show_hint = True

    def _finalise(self) -> None:
        profile = profile_from_clicks(self._clicks)
        self._state.bubble = profile
        self._state.diversity_act1 = diversity(profile)
        from cognitive_data_arcade.games.recommendation_bubble.phase_interlude import (
            PhaseInterludeScene,
        )

        self._next = PhaseInterludeScene(self._state, next_act="curator")
        self._done = True

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(22).render("AKT 1 -- UZYTKOWNIK", True, _C_USER)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        secs_left = max(0.0, (self._limit - self._timer) / 1000.0)
        timer_s = get_font(16).render(f"{secs_left:.0f}s", True, (230, 126, 34))
        surface.blit(timer_s, (_W - 100, 18))

        total = max(sum(self._clicks.values()), 1)
        for i, cat in enumerate(CATEGORIES):
            rect = _BAR_ROWS[i]
            color = CAT_COLORS[cat]
            pygame.draw.rect(surface, (30, 30, 50), rect, border_radius=4)
            frac = self._clicks[cat] / total
            fill_w = int(rect.w * frac)
            if fill_w > 0:
                pygame.draw.rect(
                    surface,
                    color,
                    pygame.Rect(rect.x, rect.y, fill_w, rect.h),
                    border_radius=4,
                )
            pygame.draw.rect(surface, color, rect, 1, border_radius=4)
            label = get_font(18).render(cat, True, color)
            surface.blit(label, (rect.x + 8, rect.y + rect.h // 2 - 9))
            pct = get_font(16).render(f"{int(frac * 100)}%", True, _WHITE)
            surface.blit(pct, (rect.right - pct.get_width() - 10, rect.y + rect.h // 2 - 8))

        d = diversity(profile_from_clicks(self._clicks))
        d_color = (231, 76, 60) if d < 0.35 else ((243, 156, 18) if d < 0.65 else (46, 204, 113))
        d_lbl = get_font(14).render(f"ROZNORODNOSC: {int(d * 100)}%", True, d_color)
        surface.blit(d_lbl, (_W // 2 - d_lbl.get_width() // 2, _H - 80))

        if self._show_hint:
            hint = get_font(14).render("Kliknij wiecej kategori!", True, (243, 156, 18))
            surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 55))
        else:
            hint = get_font(13).render("klikaj paski zeby konsumowac tresc", True, _DIM)
            surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 55))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

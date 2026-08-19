from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
)
from cognitive_data_arcade.engine.colors import (
    DIM as _DIM,
)
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.recommendation_bubble.game_state import (
    CAT_COLORS,
    CATEGORIES,
    GameState,
    curated_profile,
    diversity,
    generate_slots,
)

_W, _H = 1024, 768
_PANEL = (20, 14, 30)
_C_CURATOR = (39, 174, 96)
_C_SEL = (243, 156, 18)

_ACT_SECS = 45.0
_MAX_SWAPS = 5
_SLOT_W, _SLOT_H = 290, 80
_SLOT_COLS = 2
_GRID_X = (_W - _SLOT_COLS * _SLOT_W - 20) // 2
_GRID_Y = 160


def _slot_rect(idx: int) -> pygame.Rect:
    col = idx % _SLOT_COLS
    row = idx // _SLOT_COLS
    return pygame.Rect(
        _GRID_X + col * (_SLOT_W + 20),
        _GRID_Y + row * (_SLOT_H + 14),
        _SLOT_W,
        _SLOT_H,
    )


_PICK_Y = _GRID_Y + 3 * (_SLOT_H + 14) + 20
_PICK_RECTS = [
    pygame.Rect(_W // 2 - (len(CATEGORIES) * 110) // 2 + i * 110, _PICK_Y, 100, 38)
    for i in range(len(CATEGORIES))
]


class PhaseCuratorScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._slots: list[str] = generate_slots(state.bubble, n=6, seed=1)
        self._swaps_left = _MAX_SWAPS
        self._selected_slot: int | None = None
        self._timer = 0.0
        self._limit = _ACT_SECS * 1000.0
        self._done = False
        self._next: Scene | None = None

    def _do_swap(self, new_cat: str) -> None:
        if self._swaps_left <= 0 or self._selected_slot is None:
            return
        self._slots[self._selected_slot] = new_cat
        self._swaps_left -= 1
        self._selected_slot = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        for i in range(6):
            if _slot_rect(i).collidepoint(event.pos):
                self._selected_slot = i
                return
        if self._selected_slot is not None:
            for i, rect in enumerate(_PICK_RECTS):
                if rect.collidepoint(event.pos):
                    self._do_swap(CATEGORIES[i])
                    return
            self._selected_slot = None

    def update(self, dt_ms: float = 0.0) -> None:
        self._timer += dt_ms
        if self._timer >= self._limit:
            self._finalise()

    def _finalise(self) -> None:
        if self._done:
            return
        cp = curated_profile(self._slots)
        d2 = diversity(cp)
        self._state.diversity_act2 = d2
        self._state.score_curator = int(d2 * 100)
        self._state.curator_slots = list(self._slots)
        from cognitive_data_arcade.games.recommendation_bubble.phase_interlude import (
            PhaseInterludeScene,
        )

        self._next = PhaseInterludeScene(self._state, next_act="algo")
        self._done = True

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(22).render("AKT 2 -- KURATOR", True, _C_CURATOR)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))
        secs_left = max(0.0, (self._limit - self._timer) / 1000.0)
        surface.blit(get_font(16).render(f"{secs_left:.0f}s", True, (230, 126, 34)), (_W - 100, 18))
        surface.blit(
            get_font(16).render(f"zamiany: {self._swaps_left}/{_MAX_SWAPS}", True, _DIM),
            (20, 18),
        )

        for i in range(6):
            rect = _slot_rect(i)
            cat = self._slots[i]
            color = CAT_COLORS[cat]
            border_color = _C_SEL if i == self._selected_slot else color
            border_w = 2 if i == self._selected_slot else 1
            pygame.draw.rect(surface, (20, 20, 40), rect, border_radius=6)
            pygame.draw.rect(surface, border_color, rect, border_w, border_radius=6)
            lbl = get_font(18).render(cat, True, color)
            surface.blit(lbl, (rect.x + rect.w // 2 - lbl.get_width() // 2, rect.y + 28))

        if self._selected_slot is not None:
            prompt = get_font(14).render("Wybierz nowa kategorie:", True, _C_SEL)
            surface.blit(prompt, (_W // 2 - prompt.get_width() // 2, _PICK_Y - 24))
            for i, rect in enumerate(_PICK_RECTS):
                cat = CATEGORIES[i]
                color = CAT_COLORS[cat]
                pygame.draw.rect(surface, (20, 20, 40), rect, border_radius=4)
                pygame.draw.rect(surface, color, rect, 1, border_radius=4)
                lbl = get_font(13).render(cat, True, color)
                surface.blit(lbl, (rect.x + rect.w // 2 - lbl.get_width() // 2, rect.y + 11))

        d = diversity(curated_profile(self._slots))
        d_color = (231, 76, 60) if d < 0.35 else ((243, 156, 18) if d < 0.65 else (46, 204, 113))
        surface.blit(
            get_font(14).render(f"ROZNORODNOSC: {int(d * 100)}%", True, d_color),
            (_W // 2 - 80, _H - 60),
        )
        hint = get_font(14).render("kliknij slot aby zamienic kategorie", True, _DIM)
        surface.blit(hint, (14, _H - 28))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

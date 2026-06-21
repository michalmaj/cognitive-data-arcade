from __future__ import annotations
import random
import pygame
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.recommendation_bubble.game_state import (
    GameState,
    CATEGORIES,
    CAT_COLORS,
    ENGAGEMENT,
    diversity,
    profile_from_clicks,
    generate_slots,
)

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    DIM as _DIM,
)

_W, _H = 1024, 768
_PANEL = (20, 14, 30)
_C_ALGO = (230, 126, 34)
_GOLD = (243, 156, 18)

_ACT_SECS = 30.0
_TILE_W, _TILE_H = 290, 80
_TILE_COLS = 2
_GRID_X = (_W - _TILE_COLS * _TILE_W - 20) // 2
_GRID_Y = 160


class PhaseAlgoScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._rng = random.Random(99)
        self._displayed: list[str] = generate_slots(state.bubble, n=6, seed=99)
        self._score = 0
        self._clicked_cats: list[str] = []
        self._timer = 0.0
        self._limit = _ACT_SECS * 1000.0
        self._done = False
        self._next: Scene | None = None

    def _tile_rect(self, idx: int) -> pygame.Rect:
        col = idx % _TILE_COLS
        row = idx // _TILE_COLS
        return pygame.Rect(
            _GRID_X + col * (_TILE_W + 20),
            _GRID_Y + row * (_TILE_H + 14),
            _TILE_W,
            _TILE_H,
        )

    def _spawn_tile(self) -> str:
        return self._rng.choices(
            list(self._state.bubble.keys()),
            weights=list(self._state.bubble.values()),
            k=1,
        )[0]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        for i in range(6):
            if self._tile_rect(i).collidepoint(event.pos):
                cat = self._displayed[i]
                self._score += ENGAGEMENT[cat]
                self._clicked_cats.append(cat)
                self._displayed[i] = self._spawn_tile()
                return

    def update(self, dt_ms: float = 0.0) -> None:
        self._timer += dt_ms
        if self._timer >= self._limit:
            self._finalise()

    def _finalise(self) -> None:
        if self._done:
            return
        self._state.score_algo = self._score
        self._state.algo_clicked_cats = list(self._clicked_cats)
        clicks = {cat: self._clicked_cats.count(cat) for cat in CATEGORIES}
        self._state.diversity_act3 = (
            diversity(profile_from_clicks(clicks)) if self._clicked_cats else 0.0
        )
        from cognitive_data_arcade.games.recommendation_bubble.phase_result import PhaseResultScene

        self._next = PhaseResultScene(self._state)
        self._done = True

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(22).render("AKT 3 -- ALGORYTM", True, _C_ALGO)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))
        secs_left = max(0.0, (self._limit - self._timer) / 1000.0)
        surface.blit(get_font(16).render(f"{secs_left:.0f}s", True, _C_ALGO), (_W - 100, 18))

        for i in range(6):
            rect = self._tile_rect(i)
            cat = self._displayed[i]
            color = CAT_COLORS[cat]
            eng = ENGAGEMENT[cat]
            pygame.draw.rect(surface, (20, 20, 40), rect, border_radius=6)
            pygame.draw.rect(surface, color, rect, 1, border_radius=6)
            lbl = get_font(17).render(cat, True, color)
            surface.blit(lbl, (rect.x + 12, rect.y + 16))
            eng_s = get_font(15).render(f"+{eng}", True, (46, 204, 113))
            surface.blit(eng_s, (rect.right - eng_s.get_width() - 12, rect.y + 16))

        score_s = get_font(28).render(f"ENGAGEMENT: {self._score}", True, _GOLD)
        surface.blit(score_s, (_W // 2 - score_s.get_width() // 2, _H - 90))
        hint = get_font(13).render("maks. wynik = najlepsza rekomendacja!", True, _DIM)
        surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 55))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

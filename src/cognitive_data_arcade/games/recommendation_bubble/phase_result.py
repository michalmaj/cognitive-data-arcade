from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
)
from cognitive_data_arcade.engine.colors import (
    DIM as _DIM,
)
from cognitive_data_arcade.engine.colors import (
    WHITE as _WHITE,
)
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.recommendation_bubble.game_state import (
    CAT_COLORS,
    CATEGORIES,
    GameState,
    profile_from_clicks,
)

_W, _H = 1024, 768
_PANEL = (20, 14, 30)
_GOLD = (243, 156, 18)
_GREY = (60, 60, 80)
_C_USER = (155, 89, 182)
_C_CURATOR = (39, 174, 96)
_C_ALGO = (230, 126, 34)

_BTN_REPLAY = pygame.Rect(_W // 2 - 210, _H - 76, 190, 44)
_BTN_MENU = pygame.Rect(_W // 2 + 20, _H - 76, 190, 44)

_AHA_STRONG = (
    "Algorytm nie jest zly. Po prostu optymalizuje to, o co go prosisz. "
    "Twoj profil mowil SPORT -- algorytm dal Ci SPORT. Bez zlych zamiarow."
)
_AHA_WEAK = (
    "Algorytm podazyl za Twoim profilem. Im bardziej zroznicowany profil, "
    "tym bardziej zroznicowane rekomendacje. Wynik algorytmu to efekt Twoich klikniec."
)


def _wrap(text: str, font: pygame.font.Font, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        cand = (cur + " " + w).strip()
        if font.size(cand)[0] <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _profile_from_algo_clicks(state: GameState) -> dict[str, float]:
    cats = state.algo_clicked_cats
    if not cats:
        return state.bubble
    clicks = {cat: cats.count(cat) for cat in CATEGORIES}
    return profile_from_clicks(clicks)


class PhaseResultScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._stars = 3 if state.score_curator >= 65 else (2 if state.score_curator >= 40 else 1)
        algo_profile = _profile_from_algo_clicks(state)
        dominant_frac = max(algo_profile.values())
        self._aha = _AHA_STRONG if dominant_frac >= 0.60 else _AHA_WEAK
        self._done = False
        self._next: Scene | None = None

        # Bubble verdict based on act3 diversity
        d3 = getattr(state, "diversity_act3", 0.5)
        if d3 < 0.35:
            self._bubble_verdict = "Banka: MOCNA (echo chamber)"
            self._bubble_color = (231, 76, 60)
        elif d3 < 0.65:
            self._bubble_verdict = "Banka: UMIARKOWANA"
            self._bubble_color = (243, 156, 18)
        else:
            self._bubble_verdict = "Banka: SLABA (dobra roznorodnosc!)"
            self._bubble_color = (46, 204, 113)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if _BTN_REPLAY.collidepoint(event.pos):
                from cognitive_data_arcade.games.recommendation_bubble.game import (
                    RecommendationBubbleScene,
                )

                self._next = RecommendationBubbleScene()
                self._done = True
            elif _BTN_MENU.collidepoint(event.pos):
                self._next = None
                self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def _curated_profile(self) -> dict[str, float]:
        from cognitive_data_arcade.games.recommendation_bubble.game_state import (
            curated_profile,
            generate_slots,
        )

        slots = self._state.curator_slots or generate_slots(self._state.bubble, n=6, seed=1)
        return curated_profile(slots)

    def _draw_bar_chart(
        self,
        surface: pygame.Surface,
        profile: dict[str, float],
        x: int,
        y: int,
        w: int,
        h: int,
        label: str,
        label_color: tuple[int, int, int],
        div_value: float,
    ) -> None:
        lbl = get_font(11).render(label, True, label_color)
        surface.blit(lbl, (x + w // 2 - lbl.get_width() // 2, y))
        bar_w = w // len(CATEGORIES) - 4
        max_bar_h = h - 40
        for i, cat in enumerate(CATEGORIES):
            bx = x + i * (bar_w + 4)
            bh = int(profile[cat] * max_bar_h)
            color = CAT_COLORS[cat]
            if bh > 0:
                pygame.draw.rect(
                    surface, color, pygame.Rect(bx, y + 18 + (max_bar_h - bh), bar_w, bh)
                )
        d_color = (
            (231, 76, 60)
            if div_value < 0.35
            else ((243, 156, 18) if div_value < 0.65 else (46, 204, 113))
        )
        d_s = get_font(11).render(f"D={int(div_value * 100)}%", True, d_color)
        surface.blit(d_s, (x + w // 2 - d_s.get_width() // 2, y + h - 18))

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(22).render("Recommendation Bubble -- Wyniki", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        for i in range(3):
            filled = i < self._stars
            color = _GOLD if filled else _GREY
            cx = _W // 2 - 30 + i * 30
            pygame.draw.circle(surface, color, (cx, 80), 10, 0 if filled else 2)

        chart_w = 280
        chart_h = 200
        charts = [
            (self._state.bubble, "AKT 1 UZYTKOWNIK", _C_USER, self._state.diversity_act1),
            (self._curated_profile(), "AKT 2 KURATOR", _C_CURATOR, self._state.diversity_act2),
            (
                _profile_from_algo_clicks(self._state),
                "AKT 3 ALGORYTM",
                _C_ALGO,
                self._state.diversity_act3,
            ),
        ]
        gap = (_W - 3 * chart_w) // 4
        for i, (profile, label, color, d) in enumerate(charts):
            cx = gap + i * (chart_w + gap)
            self._draw_bar_chart(surface, profile, cx, 110, chart_w, chart_h, label, color, d)

        aha_y = 340
        box_h = 80
        pygame.draw.rect(surface, (10, 20, 30), (50, aha_y, _W - 100, box_h), border_radius=6)
        pygame.draw.rect(surface, _GOLD, (50, aha_y, _W - 100, box_h), 1, border_radius=6)
        lbl_s = get_font(11).render("SPOSTRZEZENIE", True, _GOLD)
        surface.blit(lbl_s, (64, aha_y + 6))
        aha_font = get_font(12)
        wrapped = _wrap(self._aha, aha_font, _W - 140)
        for li, line in enumerate(wrapped):
            ls = aha_font.render(line, True, _DIM)
            surface.blit(ls, (64, aha_y + 22 + li * 16))

        score_y = 440
        pygame.draw.rect(surface, _PANEL, (50, score_y, _W - 100, 60), border_radius=4)
        score_text = get_font(16).render(
            f"Kurator: {self._state.score_curator} pkt  |  Algo engagement: {self._state.score_algo}",
            True,
            _DIM,
        )
        surface.blit(score_text, (_W // 2 - score_text.get_width() // 2, score_y + 20))

        verdict_surf = get_font(16).render(self._bubble_verdict, True, self._bubble_color)
        surface.blit(verdict_surf, (_W // 2 - verdict_surf.get_width() // 2, score_y + 70))

        pygame.draw.rect(surface, _PANEL, _BTN_REPLAY, border_radius=6)
        pygame.draw.rect(surface, _GREY, _BTN_REPLAY, 1, border_radius=6)
        r_lbl = get_font(16).render("Zagraj ponownie", True, (180, 180, 200))
        surface.blit(
            r_lbl,
            (
                _BTN_REPLAY.x + (_BTN_REPLAY.w - r_lbl.get_width()) // 2,
                _BTN_REPLAY.y + (_BTN_REPLAY.h - r_lbl.get_height()) // 2,
            ),
        )
        pygame.draw.rect(surface, _PANEL, _BTN_MENU, border_radius=6)
        pygame.draw.rect(surface, _C_USER, _BTN_MENU, 1, border_radius=6)
        m_lbl = get_font(16).render("Menu", True, _C_USER)
        surface.blit(
            m_lbl,
            (
                _BTN_MENU.x + (_BTN_MENU.w - m_lbl.get_width()) // 2,
                _BTN_MENU.y + (_BTN_MENU.h - m_lbl.get_height()) // 2,
            ),
        )

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

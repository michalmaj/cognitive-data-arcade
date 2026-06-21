from __future__ import annotations

import random

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

_W, _H = 1024, 720
_BG = (15, 15, 35)
_PANEL = (18, 18, 42)
_WHITE = (240, 240, 240)
_DIM = (100, 100, 130)
_AMBER = (240, 165, 0)
_GREEN = (39, 174, 96)
_RED = (231, 76, 60)
_GREY = (60, 60, 80)
_BLUE = (52, 152, 219)
_PURPLE = (155, 89, 182)

_TYPE_LABELS = {
    "neighbors": "Sasiedzi",
    "odd_one_out": "Intruz",
    "bridge": "Most",
    "analogy": "Analogia",
}
_TYPE_COLORS = {
    "neighbors": _BLUE,
    "odd_one_out": _RED,
    "bridge": _GREEN,
    "analogy": _PURPLE,
}
_AHA_INSIGHTS = [
    "Embeddingi to nie slownik -- to geometria kontekstu.",
    "Krol - mezczyzna + kobieta = krolowa. Matematyka znaczenia!",
    "Klastry semantyczne istnieja bez etykiet -- emergencja.",
    "Im wiecej tekstu, tym lepsza mapa. GPT-4 widzi kosmos slow.",
    "Cosine similarity mierzy kat, nie odleglosc. Skala nie ma znaczenia.",
]


def _calc_stats(round_results: list[dict]) -> dict[str, tuple[int, int]]:
    stats: dict[str, list[int]] = {t: [0, 0] for t in _TYPE_LABELS}
    for r in round_results:
        t = r["type"]
        if t in stats:
            stats[t][1] += 1
            if r["correct"]:
                stats[t][0] += 1
    return {k: (v[0], v[1]) for k, v in stats.items()}


class PhaseResultScene(Scene):
    def __init__(self, session_score: int, round_results: list[dict]) -> None:
        self._session_score = session_score
        self._round_results = round_results
        self._insight = random.choice(_AHA_INSIGHTS)
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._advance()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._advance()

    def _advance(self) -> None:
        from cognitive_data_arcade.games.semantic_space.phase_intro import PhaseIntroScene

        self._next = PhaseIntroScene()
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(22).render("Koniec sesji!", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        score_lbl = get_font(36).render(f"{self._session_score} pkt", True, _AMBER)
        surface.blit(score_lbl, (_W // 2 - score_lbl.get_width() // 2, 72))

        sub = get_font(13).render("Wyniki wedlug typu misji:", True, _DIM)
        surface.blit(sub, (_W // 2 - sub.get_width() // 2, 118))

        self._draw_bar_chart(surface, 150)

        insight_lbl = get_font(13).render(f"AHA: {self._insight}", True, _AMBER)
        surface.blit(insight_lbl, (_W // 2 - insight_lbl.get_width() // 2, 560))

        en_note = get_font(11).render("EN: king - man + woman = queen (Word2Vec, 2013)", True, _DIM)
        surface.blit(en_note, (_W // 2 - en_note.get_width() // 2, 585))

        btn = pygame.Rect(_W // 2 - 160, _H - 80, 320, 50)
        pygame.draw.rect(surface, _BLUE, btn, border_radius=8)
        bl = get_font(16).render("GRAJ PONOWNIE (SPACJA)", True, _WHITE)
        surface.blit(bl, (btn.centerx - bl.get_width() // 2, btn.centery - bl.get_height() // 2))

    def _draw_bar_chart(self, surface: pygame.Surface, top: int) -> None:
        stats = _calc_stats(self._round_results)
        types = list(_TYPE_LABELS.keys())
        chart_x = 80
        chart_w = _W - 160
        bar_area_h = 300
        n = len(types)
        bar_w = chart_w // (n * 2 + 1)
        bar_gap = bar_w
        max_h = bar_area_h - 40
        bottom = top + bar_area_h

        pygame.draw.line(surface, _GREY, (chart_x, top), (chart_x, bottom))
        pygame.draw.line(surface, _GREY, (chart_x, bottom), (chart_x + chart_w, bottom))

        font10 = get_font(10)
        for pct in (0, 50, 100):
            y = bottom - int(pct / 100 * max_h)
            pygame.draw.line(surface, (35, 35, 55), (chart_x, y), (chart_x + chart_w, y))
            pl = font10.render(f"{pct}%", True, _GREY)
            surface.blit(pl, (chart_x - pl.get_width() - 4, y - pl.get_height() // 2))

        for i, t in enumerate(types):
            correct, total = stats[t]
            pct = correct / total if total > 0 else 0
            bar_h = int(pct * max_h)
            bx = chart_x + bar_gap + i * (bar_w + bar_gap)
            by = bottom - bar_h
            color = _TYPE_COLORS[t]
            if bar_h > 0:
                pygame.draw.rect(surface, color, (bx, by, bar_w, bar_h))
            pygame.draw.rect(surface, color, (bx, bottom - 2, bar_w, 2))
            cat_lbl = font10.render(_TYPE_LABELS[t], True, _DIM)
            surface.blit(cat_lbl, (bx + bar_w // 2 - cat_lbl.get_width() // 2, bottom + 6))
            if total > 0:
                pt = font10.render(f"{int(pct * 100)}%", True, color)
                surface.blit(pt, (bx + bar_w // 2 - pt.get_width() // 2, max(top + 4, by - 14)))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

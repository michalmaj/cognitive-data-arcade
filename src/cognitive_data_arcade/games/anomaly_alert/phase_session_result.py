# src/cognitive_data_arcade/games/anomaly_alert/phase_session_result.py
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

_W, _H = 1024, 720
_BG = (15, 15, 35)
_PANEL = (18, 18, 42)
_WHITE = (240, 240, 240)
_DIM = (120, 120, 160)
_BLUE = (52, 152, 219)
_GREEN = (46, 204, 113)
_RED = (231, 76, 60)
_AMBER = (243, 156, 18)
_GOLD = (255, 215, 0)

_CHART_W, _CHART_H = 560, 300
_CHART_X = (_W - _CHART_W) // 2
_CHART_Y = 120

_REPLAY_RECT = pygame.Rect(_W // 2 - 140, _H - 70, 280, 46)


def _bar_color(score: int) -> str:
    if score >= 40:
        return "#2ecc71"
    if score >= 20:
        return "#f39c12"
    return "#e74c3c"


def _build_chart(round_results: list[dict]) -> pygame.Surface:
    scores = [r["score"] for r in round_results]
    labels = [f"R{r['round_idx'] + 1}" for r in round_results]
    colors = [_bar_color(s) for s in scores]

    fig, ax = plt.subplots(figsize=(_CHART_W / 96, _CHART_H / 96), dpi=96)
    ax.bar(range(len(scores)), scores, color=colors, edgecolor="#333355")
    ax.set_xticks(range(len(scores)))
    ax.set_xticklabels(labels, fontsize=9, color="#888899")
    ax.set_ylim(0, 55)
    ax.set_ylabel("Pkt", color="#888899", fontsize=9)
    ax.set_title("Wyniki rund", color="#ccccdd", fontsize=10)
    ax.set_facecolor("#0f0f1a")
    fig.patch.set_facecolor("#111130")
    ax.tick_params(colors="#888899")
    for sp in ax.spines.values():
        sp.set_edgecolor("#333355")
    ax.axhline(40, color="#2ecc71", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.axhline(20, color="#f39c12", linewidth=0.8, linestyle="--", alpha=0.5)
    fig.tight_layout()
    return figure_to_surface(fig, (_CHART_W, _CHART_H))


class PhaseSessionResultScene(Scene):
    def __init__(self, round_results: list[dict]) -> None:
        self._results = round_results
        self._total = sum(r["score"] for r in round_results)
        self._chart_surf = _build_chart(round_results)
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self._replay()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if _REPLAY_RECT.collidepoint(event.pos):
                self._replay()

    def _replay(self) -> None:
        from cognitive_data_arcade.games.anomaly_alert.phase_intro import PhaseIntroScene

        self._next = PhaseIntroScene()
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(24).render("Anomaly Alert -- Podsumowanie", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        if self._total >= 240:
            col, rank = _GOLD, "Zloto"
        elif self._total >= 150:
            col, rank = _AMBER, "Srebro"
        else:
            col, rank = (180, 100, 60), "Braz"

        sc = get_font(42).render(f"{self._total} pkt", True, col)
        surface.blit(sc, (12, 62))
        rk = get_font(18).render(rank, True, col)
        surface.blit(rk, (12 + sc.get_width() + 12, 74))

        surface.blit(self._chart_surf, (_CHART_X, _CHART_Y))
        self._draw_table(surface)

        pygame.draw.rect(surface, _PANEL, _REPLAY_RECT, border_radius=8)
        pygame.draw.rect(surface, _BLUE, _REPLAY_RECT, 2, border_radius=8)
        btn_lbl = get_font(18).render("Zagraj ponownie", True, _BLUE)
        surface.blit(
            btn_lbl,
            (
                _REPLAY_RECT.centerx - btn_lbl.get_width() // 2,
                _REPLAY_RECT.centery - btn_lbl.get_height() // 2,
            ),
        )

    def _draw_table(self, surface: pygame.Surface) -> None:
        headers = ["Runda", "Typ", "Trafione", "Alarmy", "Bonus", "Pkt"]
        col_xs = [20, 90, 260, 360, 450, 530]
        ty = _CHART_Y + _CHART_H + 10

        for hdr, cx in zip(headers, col_xs):
            s = get_font(11).render(hdr, True, (155, 89, 182))
            surface.blit(s, (cx, ty))
        ty += 20
        pygame.draw.line(surface, (60, 60, 90), (16, ty), (_W - 16, ty), 1)
        ty += 6

        _GREEN = (46, 204, 113)
        _RED = (231, 76, 60)
        _AMBER = (243, 156, 18)
        _DIM = (120, 120, 160)

        for r in self._results:
            score_col = _GREEN if r["score"] >= 40 else (_AMBER if r["score"] >= 20 else _RED)
            cells = [
                (f"R{r['round_idx'] + 1}", _DIM),
                (r["chart_type"], _DIM),
                (
                    f"{r['found']}/{r['total_anomalies']}",
                    _GREEN if r["found"] == r["total_anomalies"] else _AMBER,
                ),
                (str(r["false_alarms"]), _RED if r["false_alarms"] > 0 else _GREEN),
                (f"+{r['time_bonus']}", _AMBER if r["time_bonus"] else _DIM),
                (str(r["score"]), score_col),
            ]
            for (text, col), cx in zip(cells, col_xs):
                s = get_font(11).render(text, True, col)
                surface.blit(s, (cx, ty))
            ty += 18

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

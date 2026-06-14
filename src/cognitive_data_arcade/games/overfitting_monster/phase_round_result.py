# src/cognitive_data_arcade/games/overfitting_monster/phase_round_result.py
from __future__ import annotations

from dataclasses import dataclass

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.overfitting_monster.scenarios import Scenario

_BG     = (15, 15, 35)
_PANEL  = (18, 18, 42)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_GREEN  = (39, 174, 96)
_RED    = (231, 76, 60)
_BLUE   = (52, 152, 219)
_YELLOW = (243, 156, 18)
_ORANGE = (230, 126, 34)
_FIG_BG = "#0f0f23"
_AX_BG  = "#1a1a3e"

_W, _H = 1024, 720
_TOP_H = 40
_LEFT_W = 500
_TOTAL_ROUNDS = 5


@dataclass
class RoundDisplay:
    scenario: Scenario
    k: int
    split_pct: int
    X_train: np.ndarray
    y_train: np.ndarray
    X_test: np.ndarray
    y_test: np.ndarray
    train_acc: float
    test_acc: float
    stars: int
    score: int


def _wrap_text(text: str, font: pygame.font.Font, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _render_boundary(d: RoundDisplay) -> pygame.Surface:
    from sklearn.neighbors import KNeighborsClassifier
    from matplotlib.colors import ListedColormap

    clf = KNeighborsClassifier(n_neighbors=d.k)
    clf.fit(d.X_train, d.y_train)

    xx, yy = np.meshgrid(np.linspace(0, 1, 120), np.linspace(0, 1, 120))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    fig, ax = plt.subplots(
        figsize=(_LEFT_W / 96, (_H - _TOP_H - 70) / 96),
        dpi=96,
        facecolor=_FIG_BG,
    )
    ax.set_facecolor(_AX_BG)
    cmap = ListedColormap(["#8B1A1A", "#1A4B8B"])
    ax.pcolormesh(xx, yy, Z, cmap=cmap, alpha=0.25, shading="auto")

    for cls, color in [(0, "#e74c3c"), (1, "#3498db")]:
        mask = d.y_train == cls
        ax.scatter(d.X_train[mask, 0], d.X_train[mask, 1],
                   c=color, s=25, edgecolors="white", linewidths=0.4, zorder=3)
        mask_te = d.y_test == cls
        ax.scatter(d.X_test[mask_te, 0], d.X_test[mask_te, 1],
                   c=color, marker="D", s=30, edgecolors="white", linewidths=0.4, zorder=3)

    pred_test = clf.predict(d.X_test)
    wrong = pred_test != d.y_test
    if wrong.any():
        ax.scatter(d.X_test[wrong, 0], d.X_test[wrong, 1],
                   c="white", marker="x", s=55, linewidths=1.5, zorder=5)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(
        f"k={d.k}  |  trening: krazki  |  test: romby  |  x = blad",
        color="#787890", fontsize=7, pad=2,
    )
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a2a50")

    return figure_to_surface(fig, (_LEFT_W, _H - _TOP_H - 70))


class PhaseRoundResultScene(Scene):
    def __init__(
        self,
        display: RoundDisplay,
        round_idx: int,
        session_seed: int,
        session_score: int,
        round_results: list[dict],
        scenario_order: list[int],
    ) -> None:
        self._display = display
        self._round_idx = round_idx
        self._session_seed = session_seed
        self._session_score = session_score
        self._round_results = round_results
        self._scenario_order = scenario_order
        self._done = False
        self._next: Scene | None = None
        self._boundary_surf = _render_boundary(display)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._btn_rect().collidepoint(event.pos):
                self._advance()

    def _btn_rect(self) -> pygame.Rect:
        return pygame.Rect(_W // 2 - 130, _H - 62, 260, 44)

    def _advance(self) -> None:
        is_last = self._round_idx >= _TOTAL_ROUNDS - 1
        if is_last:
            from cognitive_data_arcade.games.overfitting_monster.phase_session_result import (
                PhaseSessionResultScene,
            )
            self._next = PhaseSessionResultScene(
                session_score=self._session_score,
                round_results=self._round_results,
            )
        else:
            from cognitive_data_arcade.games.overfitting_monster.phase_draw import PhaseDrawScene
            from cognitive_data_arcade.games.overfitting_monster.scenarios import SCENARIOS
            next_idx = self._round_idx + 1
            self._next = PhaseDrawScene(
                scenario=SCENARIOS[self._scenario_order[next_idx]],
                round_idx=next_idx,
                session_seed=self._session_seed,
                session_score=self._session_score,
                round_results=self._round_results,
                scenario_order=self._scenario_order,
            )
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        d = self._display

        # Top strip
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, _TOP_H))
        strip = get_font(18).render(
            f"Runda {self._round_idx + 1}/{_TOTAL_ROUNDS}  -  {d.scenario.name_pl}  -  Wyniki",
            True, _WHITE,
        )
        surface.blit(strip, (_W // 2 - strip.get_width() // 2, 10))

        # Left: KNN boundary
        if self._boundary_surf:
            surface.blit(self._boundary_surf, (0, _TOP_H))

        # Right panel
        rx = _LEFT_W + 8
        rw = _W - rx - 8
        self._draw_right(surface, rx, rw, d)

        # Button
        btn = self._btn_rect()
        label = "Nastepna runda" if self._round_idx < _TOTAL_ROUNDS - 1 else "Zakoncz"
        pygame.draw.rect(surface, _PANEL, btn, border_radius=6)
        pygame.draw.rect(surface, _BLUE, btn, 2, border_radius=6)
        lbl = get_font(18).render(label, True, _BLUE)
        surface.blit(lbl, (btn.centerx - lbl.get_width() // 2, btn.centery - lbl.get_height() // 2))

    def _draw_right(self, surface: pygame.Surface, rx: int, rw: int, d: RoundDisplay) -> None:
        y = _TOP_H + 12

        # Accuracy bars
        surface.blit(get_font(14).render("Dokladnosc:", True, _DIM), (rx, y))
        y += 24
        bar_max = rw - 64
        for label, acc, color in [
            ("Trening", d.train_acc, _GREEN),
            ("Test", d.test_acc, _RED),
        ]:
            lbl = get_font(13).render(label, True, color)
            surface.blit(lbl, (rx, y))
            bw = int(bar_max * acc)
            if bw > 0:
                pygame.draw.rect(surface, color,
                                  pygame.Rect(rx + 58, y + 2, bw, 14), border_radius=3)
            pct = get_font(12).render(f"{acc:.0%}", True, color)
            surface.blit(pct, (rx + 60 + bar_max, y + 1))
            y += 26

        # Gap
        gap = (d.train_acc - d.test_acc) * 100
        gap_color = _GREEN if gap < 5 else (_ORANGE if gap < 15 else _RED)
        surface.blit(get_font(13).render(f"Gap: {gap:.1f} pp", True, gap_color), (rx, y))
        y += 28

        # Stars (ASCII)
        star_str = ("xxx" if d.stars == 3 else "xx." if d.stars == 2 else "x..")
        bonus_pts = {3: 20, 2: 10, 1: 0}[d.stars]
        star_surf = get_font(20).render(star_str, True, _YELLOW)
        surface.blit(star_surf, (rx, y))
        bonus_surf = get_font(12).render(f"+{bonus_pts} pkt bonus", True, _YELLOW)
        surface.blit(bonus_surf, (rx + star_surf.get_width() + 6, y + 4))
        y += 36

        pygame.draw.line(surface, _DIM, (rx, y), (rx + rw, y))
        y += 8

        # Insight text
        font = get_font(12)
        for line in _wrap_text(d.scenario.insight_pl, font, rw - 4):
            surf = font.render(line, True, _DIM)
            surface.blit(surf, (rx, y))
            y += 18

        y += 12
        # Score
        score_col = _GREEN if d.score >= 100 else (_YELLOW if d.score >= 70 else _RED)
        score_surf = get_font(32).render(f"+{d.score} pkt", True, score_col)
        surface.blit(score_surf, (rx + rw // 2 - score_surf.get_width() // 2, y))

        y += 50
        # Params recap
        params = get_font(11).render(
            f"k={d.k}  |  podzial: {d.split_pct}% / {100 - d.split_pct}%",
            True, _DIM,
        )
        surface.blit(params, (rx, y))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

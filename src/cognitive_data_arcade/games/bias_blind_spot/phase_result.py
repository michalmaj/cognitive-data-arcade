# src/cognitive_data_arcade/games/bias_blind_spot/phase_result.py
"""Result screen: 3-column summary, stars, AHA text, replay/menu buttons."""

from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
)
from cognitive_data_arcade.engine.colors import (
    DIM as _DIM,
)
from cognitive_data_arcade.engine.colors import (
    GREEN as _GREEN,
)
from cognitive_data_arcade.engine.colors import (
    RED as _RED,
)
from cognitive_data_arcade.engine.colors import (
    WHITE as _WHITE,
)
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.bias_blind_spot.game_state import (
    CONSEQUENCE_TABLE,
    STARTING_BIAS,
    GameState,
    stars_from_score,
)

_W, _H = 1024, 768
_PANEL = (16, 20, 36)
_GOLD = (243, 156, 18)
_GREY = (60, 60, 80)

_C_APP = (155, 89, 182)
_C_ENG = (39, 174, 96)
_C_REG = (230, 126, 34)

_BTN_REPLAY = pygame.Rect(_W // 2 - 210, _H - 70, 190, 44)
_BTN_MENU = pygame.Rect(_W // 2 + 20, _H - 70, 190, 44)

_AHA_LINES = [
    "Bias w AI nie pochodzi ze zlej woli. Pochodzi z historii.",
    "Algorytm nauczyl się swiata takiego jakim byl.",
    "Usuniecie chronionego atrybutu nie usuwa dyskryminacji",
    "(inne cechy niosa ta sama informacje -- proxy features).",
    "Sprawiedliwosc ma wiele definicji -- nie daja się naraz spelnic.",
]

_METRICS_LABELS = [
    ("parity", "Parytet dem."),
    ("opportunity", "Rowne szanse"),
    ("calibration", "Kalibracja"),
]


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


class PhaseResultScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._stars = stars_from_score(state.score_engineer)
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if _BTN_REPLAY.collidepoint(event.pos):
                from cognitive_data_arcade.games.bias_blind_spot.game import BiasBlindSpotScene

                self._next = BiasBlindSpotScene()
                self._done = True
            elif _BTN_MENU.collidepoint(event.pos):
                self._next = None
                self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def _draw_col_applicant(self, surface: pygame.Surface, x: int, y: int, w: int) -> None:
        f13 = get_font(13)
        f11 = get_font(11)
        lbl = f13.render("AKT 1 -- APLIKANT", True, _C_APP)
        surface.blit(lbl, (x + w // 2 - lbl.get_width() // 2, y))
        y += 26
        if self._state.act1_correct:
            msg = "Poprawnie! Kod pocztowy."
            col = _GREEN
        else:
            msg = f"Wybrano: {self._state.act1_choice}"
            col = _RED
        ms = f11.render(msg, True, col)
        surface.blit(ms, (x + w // 2 - ms.get_width() // 2, y))
        y += 22
        note = f11.render("Prawidlowa odp.: kod pocztowy", True, _DIM)
        surface.blit(note, (x + w // 2 - note.get_width() // 2, y))

    def _draw_col_engineer(self, surface: pygame.Surface, x: int, y: int, w: int) -> None:
        f13 = get_font(13)
        f11 = get_font(11)
        lbl = f13.render("AKT 2 -- INZYNIER", True, _C_ENG)
        surface.blit(lbl, (x + w // 2 - lbl.get_width() // 2, y))
        y += 26

        bias_vals = [STARTING_BIAS] + list(self._state.bias_rounds)
        chart_top = y
        chart_h = 90
        chart_w = w - 20
        max_bias = 40.0
        pts = []
        n = len(bias_vals)
        for i, bv in enumerate(bias_vals):
            px = x + 10 + (int(i / (n - 1) * chart_w) if n > 1 else chart_w // 2)
            py = chart_top + chart_h - int((bv / max_bias) * chart_h)
            pts.append((px, py))
        if len(pts) > 1:
            for i in range(len(pts) - 1):
                pygame.draw.line(surface, _C_ENG, pts[i], pts[i + 1], 2)
        for px, py in pts:
            pygame.draw.circle(surface, _C_ENG, (px, py), 4)

        y += chart_h + 8
        score_s = f11.render(f"Wynik: {self._state.score_engineer}/100", True, _GOLD)
        surface.blit(score_s, (x + w // 2 - score_s.get_width() // 2, y))

    def _draw_col_regulator(self, surface: pygame.Surface, x: int, y: int, w: int) -> None:
        f13 = get_font(13)
        f11 = get_font(11)
        lbl = f13.render("AKT 3 -- REGULATOR", True, _C_REG)
        surface.blit(lbl, (x + w // 2 - lbl.get_width() // 2, y))
        y += 26
        choice = self._state.regulator_choice
        ch_s = f11.render(f"Wybor: {choice}", True, _C_REG)
        surface.blit(ch_s, (x, y))
        y += 22
        if choice and choice in CONSEQUENCE_TABLE:
            row = CONSEQUENCE_TABLE[choice]
            for key, label in _METRICS_LABELS:
                ok = row[key]
                col = _GREEN if ok else _RED
                status = "OK" if ok else "NARUSZONE"
                ls = f11.render(f"{label}: {status}", True, col)
                surface.blit(ls, (x, y))
                y += 18
            acc_s = f11.render(f"Dokladnosc: {row['accuracy'] * 100:.0f}%", True, _WHITE)
            surface.blit(acc_s, (x, y))

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(22).render("Bias Blind Spot -- Wyniki", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        for i in range(3):
            filled = i < self._stars
            color = _GOLD if filled else _GREY
            cx = _W // 2 - 30 + i * 30
            pygame.draw.circle(surface, color, (cx, 78), 10, 0 if filled else 2)

        col_w = 300
        gap = (_W - 3 * col_w) // 4
        col_y = 100
        self._draw_col_applicant(surface, gap, col_y, col_w)
        self._draw_col_engineer(surface, gap + col_w + gap, col_y, col_w)
        self._draw_col_regulator(surface, gap + 2 * (col_w + gap), col_y, col_w)

        aha_y = 300
        box_h = 110
        pygame.draw.rect(surface, (10, 20, 30), (50, aha_y, _W - 100, box_h), border_radius=6)
        pygame.draw.rect(surface, _GOLD, (50, aha_y, _W - 100, box_h), 1, border_radius=6)
        f11 = get_font(11)
        lbl_s = f11.render("SPOSTRZEZENIE", True, _GOLD)
        surface.blit(lbl_s, (64, aha_y + 6))
        ly = aha_y + 24
        for line in _AHA_LINES:
            ls = f11.render(line, True, _DIM)
            surface.blit(ls, (64, ly))
            ly += 16

        pygame.draw.rect(surface, _PANEL, _BTN_REPLAY, border_radius=6)
        pygame.draw.rect(surface, _GREY, _BTN_REPLAY, 1, border_radius=6)
        rl = get_font(16).render("Zagraj ponownie", True, (180, 180, 200))
        surface.blit(
            rl,
            (
                _BTN_REPLAY.x + (_BTN_REPLAY.w - rl.get_width()) // 2,
                _BTN_REPLAY.y + (_BTN_REPLAY.h - rl.get_height()) // 2,
            ),
        )

        pygame.draw.rect(surface, _PANEL, _BTN_MENU, border_radius=6)
        pygame.draw.rect(surface, _C_APP, _BTN_MENU, 1, border_radius=6)
        ml = get_font(16).render("Menu", True, _C_APP)
        surface.blit(
            ml,
            (
                _BTN_MENU.x + (_BTN_MENU.w - ml.get_width()) // 2,
                _BTN_MENU.y + (_BTN_MENU.h - ml.get_height()) // 2,
            ),
        )

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

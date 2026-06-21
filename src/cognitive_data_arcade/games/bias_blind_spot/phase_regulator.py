# src/cognitive_data_arcade/games/bias_blind_spot/phase_regulator.py
"""Act 3 -- Regulator: choose fairness criterion, see consequence table."""

from __future__ import annotations
import pygame
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.bias_blind_spot.game_state import GameState, CONSEQUENCE_TABLE

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
    GREEN as _GREEN,
    RED as _RED,
)

_W, _H = 1024, 720
_PANEL = (16, 20, 36)
_GOLD = (243, 156, 18)

_PANELS = [
    {
        "key": "parity",
        "color": (155, 89, 182),
        "title": "Rzecznik rownosci",
        "quote": (
            "Wskaznik zatwierdzenia gr. A: 71%, gr. B: 38%.",
            "To dyskryminacja. Wymagam parytetu demograficznego.",
        ),
        "criterion": "Parytet demograficzny",
    },
    {
        "key": "opportunity",
        "color": (39, 174, 96),
        "title": "Bank",
        "quote": (
            "Model ma 82% trafnosci.",
            "Obnizenie progu dla gr. B zniszczy portfel kredytowy.",
        ),
        "criterion": "Rowne szanse (FPR)",
    },
    {
        "key": "calibration",
        "color": (230, 126, 34),
        "title": "Prawnik / EU AI Act",
        "quote": (
            "Kalibracja jest wymogiem prawnym.",
            "Parytet i rowne szanse nie moga byc egzekwowane naraz.",
        ),
        "criterion": "Kalibracja",
    },
]

_PANEL_W = 290
_PANEL_H = 200
_PANEL_TOP = 80
_PANEL_GAP = 22
_PANEL_LEFT = (_W - 3 * _PANEL_W - 2 * _PANEL_GAP) // 2

_TABLE_TOP = 330
_TABLE_LEFT = 60

_METRICS = ["parity", "opportunity", "calibration"]
_METRIC_LABELS = ["Parytet dem.", "Rowne szanse", "Kalibracja"]

_AHA = (
    "To nie bug -- twierdzenie matematyczne (Chouldechova 2017).",
    "Nie istnieje algorytm spelniajacy wszystkie 3 kryteria naraz.",
    "Ta decyzja jest polityczna, nie techniczna.",
)

_BTN_ADV = pygame.Rect(_W // 2 - 140, _H - 70, 280, 44)


class PhaseRegulatorScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._chosen: str | None = None
        self._show_table = False
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        pos = event.pos
        if self._show_table:
            if _BTN_ADV.collidepoint(pos):
                self._advance()
            return
        for i, p in enumerate(_PANELS):
            pr = self._panel_rect(i)
            if pr.collidepoint(pos):
                self._chosen = p["key"]
                self._state.regulator_choice = p["key"]
                self._show_table = True
                return

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def _advance(self) -> None:
        if self._done:
            return
        from cognitive_data_arcade.games.bias_blind_spot.phase_result import PhaseResultScene

        self._next = PhaseResultScene(self._state)
        self._done = True

    def _panel_rect(self, idx: int) -> pygame.Rect:
        x = _PANEL_LEFT + idx * (_PANEL_W + _PANEL_GAP)
        return pygame.Rect(x, _PANEL_TOP, _PANEL_W, _PANEL_H)

    def _draw_stakeholder_panels(self, surface: pygame.Surface) -> None:
        f13 = get_font(13)
        f11 = get_font(11)
        for i, p in enumerate(_PANELS):
            r = self._panel_rect(i)
            is_chosen = self._chosen == p["key"]
            bg = (20, 20, 30)
            border = p["color"] if is_chosen else (60, 60, 80)
            pygame.draw.rect(surface, bg, r, border_radius=8)
            pygame.draw.rect(surface, border, r, 2 if is_chosen else 1, border_radius=8)

            title_s = f13.render(p["title"], True, p["color"])
            surface.blit(title_s, (r.x + 10, r.y + 10))

            crit_s = f11.render(f">> {p['criterion']}", True, p["color"])
            surface.blit(crit_s, (r.x + 10, r.y + 32))

            y = r.y + 58
            for line in p["quote"]:
                ls = f11.render(line, True, _DIM)
                surface.blit(ls, (r.x + 10, y))
                y += 18

    def _draw_consequence_table(self, surface: pygame.Surface) -> None:
        if self._chosen is None:
            return
        row = CONSEQUENCE_TABLE[self._chosen]
        f13 = get_font(13)
        f11 = get_font(11)

        hdr = f13.render(f"KONSEKWENCJE -- wybor: {self._chosen.upper()}", True, _GOLD)
        surface.blit(hdr, (_TABLE_LEFT, _TABLE_TOP))

        y = _TABLE_TOP + 30
        for metric, label in zip(_METRICS, _METRIC_LABELS):
            ok = row[metric]
            col = _GREEN if ok else _RED
            status = "OK" if ok else "NARUSZONE"
            ls = f11.render(f"{label}: {status}", True, col)
            surface.blit(ls, (_TABLE_LEFT, y))
            y += 22

        acc_s = f11.render(f"Dokladnosc modelu: {row['accuracy'] * 100:.0f}%", True, _WHITE)
        surface.blit(acc_s, (_TABLE_LEFT, y + 6))

        ay = y + 36
        for line in _AHA:
            as_ = f11.render(line, True, _GOLD)
            surface.blit(as_, (_TABLE_LEFT, ay))
            ay += 18

        pygame.draw.rect(surface, _PANEL, _BTN_ADV, border_radius=6)
        pygame.draw.rect(surface, _WHITE, _BTN_ADV, 1, border_radius=6)
        bl = f13.render("Przejdz do wynikow  [klik]", True, _WHITE)
        surface.blit(
            bl,
            (
                _BTN_ADV.x + _BTN_ADV.w // 2 - bl.get_width() // 2,
                _BTN_ADV.y + _BTN_ADV.h // 2 - bl.get_height() // 2,
            ),
        )

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(20).render("Akt 3: Regulator -- wybierz kryterium", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        if not self._show_table:
            instr = get_font(13).render(
                "Kliknij panel interesariusza, aby wybrac jego kryterium.", True, _DIM
            )
            surface.blit(instr, (_W // 2 - instr.get_width() // 2, 58))

        self._draw_stakeholder_panels(surface)

        if self._show_table:
            self._draw_consequence_table(surface)

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

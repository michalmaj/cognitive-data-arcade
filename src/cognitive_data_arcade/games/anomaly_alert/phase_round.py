# src/cognitive_data_arcade/games/anomaly_alert/phase_round.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.anomaly_alert.detector import find_clicked_element
from cognitive_data_arcade.games.anomaly_alert.renderers import CHART_RENDERER
from cognitive_data_arcade.games.anomaly_alert.scenarios import Scenario

_W, _H = 1024, 768
_CHART_X, _CHART_Y = 0, 56
_CHART_W, _CHART_H = 680, 624
_PANEL_X = 680
_TOP_H = 56
from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    DIM as _DIM,
    GREEN as _GREEN,
    RED as _RED,
)

_PANEL = (18, 18, 42)
_AMBER = (243, 156, 18)

_CONFIRM_RECT = pygame.Rect(690, 650, 324, 44)
_POPUP_W, _POPUP_H = 290, 150


class PhaseRoundScene(Scene):
    def __init__(
        self,
        scenario: Scenario,
        round_idx: int,
        round_results: list[dict],
        session_seed: int = 0,
    ) -> None:
        self._scenario = scenario
        self._round_idx = round_idx
        self._round_results = round_results
        self._seed = session_seed ^ round_idx ^ 0xAA20

        renderer = CHART_RENDERER[scenario.chart_type]
        self._chart_surf, self._elements = renderer(scenario, self._seed)

        self._selected: set[int] = set()
        self._elapsed: float = 0.0
        self._done = False
        self._next: Scene | None = None
        self._popup_visible = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self._popup_visible:
                self._popup_visible = False
                return
            if event.key == pygame.K_RETURN:
                self._confirm()
                return

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if event.button == 3:
            cx = event.pos[0] - _CHART_X
            cy = event.pos[1] - _CHART_Y
            if 0 <= cx < _CHART_W and 0 <= cy < _CHART_H:
                self._popup_visible = not self._popup_visible
            return

        if event.button != 1:
            return

        if _CONFIRM_RECT.collidepoint(event.pos):
            self._confirm()
            return

        if self._popup_visible:
            self._popup_visible = False
            return

        cx = event.pos[0] - _CHART_X
        cy = event.pos[1] - _CHART_Y
        if 0 <= cx < _CHART_W and 0 <= cy < _CHART_H:
            idx = find_clicked_element(self._elements, (cx, cy))
            if idx is not None:
                if idx in self._selected:
                    self._selected.discard(idx)
                else:
                    self._selected.add(idx)

    def _confirm(self) -> None:
        from cognitive_data_arcade.games.anomaly_alert.phase_round_result import (
            PhaseRoundResultScene,
        )
        from cognitive_data_arcade.games.anomaly_alert.detector import compute_round_score

        found = sum(1 for i in self._selected if self._elements[i].is_anomaly)
        false_alarms = sum(1 for i in self._selected if not self._elements[i].is_anomaly)
        time_bonus = 10 if self._elapsed < 45.0 else 0
        score = compute_round_score(found, false_alarms, time_bonus)

        result = {
            "round_idx": self._round_idx,
            "chart_type": self._scenario.chart_type,
            "scenario_name": self._scenario.name_pl,
            "found": found,
            "total_anomalies": self._scenario.n_anomalies,
            "false_alarms": false_alarms,
            "time_bonus": time_bonus,
            "score": score,
            "chart_surf": self._chart_surf,
            "elements": self._elements,
            "selected_idxs": frozenset(self._selected),
        }
        new_results = self._round_results + [result]

        self._next = PhaseRoundResultScene(
            result=result,
            round_idx=self._round_idx,
            round_results=new_results,
            session_seed=self._seed,
        )
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        self._elapsed += dt_ms / 1000.0

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)

        # Header
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, _TOP_H))
        title = get_font(18).render(
            f"Runda {self._round_idx + 1}/6 -- {self._scenario.name_pl}", True, (200, 200, 220)
        )
        surface.blit(title, (12, 18))

        secs = int(self._elapsed)
        mins = secs // 60
        timer_color = _AMBER if self._elapsed < 45.0 else _RED
        timer = get_font(18).render(f"{mins:02d}:{secs % 60:02d}", True, timer_color)
        surface.blit(timer, (_W - timer.get_width() - 12, 18))

        # Chart
        surface.blit(self._chart_surf, (_CHART_X, _CHART_Y))

        # Selection overlays — draw at element centre
        for i in self._selected:
            el = self._elements[i]
            cx = int(el.x_px + el.w_px / 2) + _CHART_X
            cy = int(el.y_px + el.h_px / 2) + _CHART_Y
            pygame.draw.circle(surface, _AMBER, (cx, cy), 14, 3)

        # Right panel
        pygame.draw.rect(surface, _PANEL, (_PANEL_X, 0, _W - _PANEL_X, _H))

        y = _TOP_H + 10
        lbl = get_font(14).render("STATUS", True, (155, 89, 182))
        surface.blit(lbl, (_PANEL_X + 12, y))
        y += 28

        cnt_lbl = get_font(13).render("Zaznaczone:", True, _DIM)
        surface.blit(cnt_lbl, (_PANEL_X + 12, y))
        y += 22
        cnt_val = get_font(22).render(str(len(self._selected)), True, _AMBER)
        surface.blit(cnt_val, (_PANEL_X + 12, y))
        y += 38

        found_preview = sum(1 for i in self._selected if self._elements[i].is_anomaly)
        fp_preview = len(self._selected) - found_preview
        hit_surf = get_font(13).render(f"+{found_preview * 20} pkt (trafione)", True, _GREEN)
        surface.blit(hit_surf, (_PANEL_X + 12, y))
        y += 22
        fp_surf = get_font(13).render(f"-{fp_preview * 5} pkt (alarmy)", True, _RED)
        surface.blit(fp_surf, (_PANEL_X + 12, y))
        y += 36

        bonus_col = _AMBER if self._elapsed < 45.0 else _DIM
        bon = get_font(13).render("+10 pkt jesli <45s", True, bonus_col)
        surface.blit(bon, (_PANEL_X + 12, y))
        y += 44

        hint = get_font(11).render("LPM = zaznacz/odznacz", True, _DIM)
        surface.blit(hint, (_PANEL_X + 12, y))
        y += 20
        hint2 = get_font(11).render("PPM = podpowiedz", True, _DIM)
        surface.blit(hint2, (_PANEL_X + 12, y))

        # Confirm button
        pygame.draw.rect(surface, (10, 10, 25), _CONFIRM_RECT, border_radius=6)
        pygame.draw.rect(surface, _GREEN, _CONFIRM_RECT, 2, border_radius=6)
        lbl2 = get_font(18).render("Zatwierdz", True, _GREEN)
        surface.blit(
            lbl2,
            (
                _CONFIRM_RECT.centerx - lbl2.get_width() // 2,
                _CONFIRM_RECT.centery - lbl2.get_height() // 2,
            ),
        )

        # Hint popup
        if self._popup_visible:
            self._draw_popup(surface)

    def _draw_popup(self, surface: pygame.Surface) -> None:
        px = (_CHART_W - _POPUP_W) // 2
        py = (_CHART_H - _POPUP_H) // 2 + _CHART_Y
        overlay = pygame.Surface((_POPUP_W, _POPUP_H), pygame.SRCALPHA)
        overlay.fill((10, 10, 25, 210))
        surface.blit(overlay, (px, py))
        pygame.draw.rect(surface, (80, 80, 140), (px, py, _POPUP_W, _POPUP_H), 1, border_radius=6)

        words = self._scenario.hint_pl.split()
        lines: list[str] = []
        current = ""
        for w in words:
            test = (current + " " + w).strip()
            if get_font(12).size(test)[0] < _POPUP_W - 20:
                current = test
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)

        ty = py + 10
        for line in lines[:8]:
            s = get_font(12).render(line, True, (200, 200, 220))
            surface.blit(s, (px + 10, ty))
            ty += 18

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

# src/cognitive_data_arcade/games/anomaly_alert/phase_round_result.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

_W, _H = 1024, 768
_CHART_X, _CHART_Y = 0, 56
_CHART_W, _CHART_H = 680, 624
_PANEL_X = 680
_TOP_H = 56
from cognitive_data_arcade.engine.colors import (
    BG as _BG,
)
from cognitive_data_arcade.engine.colors import (
    BLUE as _BLUE,
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

_PANEL = (18, 18, 42)
_AMBER = (243, 156, 18)

_NEXT_RECT = pygame.Rect(690, 650, 324, 44)


class PhaseRoundResultScene(Scene):
    def __init__(
        self,
        result: dict,
        round_idx: int,
        round_results: list[dict],
        session_seed: int = 0,
    ) -> None:
        self._result = result
        self._round_idx = round_idx
        self._round_results = round_results
        self._session_seed = session_seed
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self._advance()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if _NEXT_RECT.collidepoint(event.pos):
                self._advance()

    def _advance(self) -> None:
        from cognitive_data_arcade.games.anomaly_alert.scenarios import SCENARIOS

        next_idx = self._round_idx + 1
        if next_idx < len(SCENARIOS):
            from cognitive_data_arcade.games.anomaly_alert.phase_round import PhaseRoundScene

            self._next = PhaseRoundScene(
                scenario=SCENARIOS[next_idx],
                round_idx=next_idx,
                round_results=self._round_results,
                session_seed=self._session_seed,
            )
        else:
            from cognitive_data_arcade.games.anomaly_alert.phase_session_result import (
                PhaseSessionResultScene,
            )

            self._next = PhaseSessionResultScene(round_results=self._round_results)
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, _TOP_H))

        r = self._result
        title = get_font(18).render(
            f"Wynik rundy {self._round_idx + 1}/6 -- {r['scenario_name']}", True, _WHITE
        )
        surface.blit(title, (12, 16))

        # Chart with overlays
        surface.blit(r["chart_surf"], (_CHART_X, _CHART_Y))
        self._draw_overlays(surface)

        # Insight text in footer area
        from cognitive_data_arcade.games.anomaly_alert.scenarios import SCENARIOS

        scenario = SCENARIOS[self._round_idx]
        ins_surf = get_font(11).render(scenario.insight_pl[:95], True, (155, 89, 182))
        surface.blit(ins_surf, (4, _CHART_Y + _CHART_H + 4))

        # Right panel -- score breakdown
        pygame.draw.rect(surface, _PANEL, (_PANEL_X, 0, _W - _PANEL_X, _H))
        self._draw_score_panel(surface)

        # Next/Finish button
        is_last = self._round_idx == 5
        btn_label = "Zakoncz" if is_last else "Nastepna runda"
        btn_col = _AMBER if is_last else _BLUE
        pygame.draw.rect(surface, (10, 10, 25), _NEXT_RECT, border_radius=6)
        pygame.draw.rect(surface, btn_col, _NEXT_RECT, 2, border_radius=6)
        lbl = get_font(18).render(btn_label, True, btn_col)
        surface.blit(
            lbl,
            (
                _NEXT_RECT.centerx - lbl.get_width() // 2,
                _NEXT_RECT.centery - lbl.get_height() // 2,
            ),
        )

    def _draw_overlays(self, surface: pygame.Surface) -> None:
        r = self._result
        elements = r["elements"]
        selected = r["selected_idxs"]

        for i, el in enumerate(elements):
            if not el.is_anomaly and i not in selected:
                continue
            cx = int(el.x_px + el.w_px / 2) + _CHART_X
            cy = int(el.y_px + el.h_px / 2) + _CHART_Y

            if el.is_anomaly and i in selected:
                # True positive: green ring
                pygame.draw.circle(surface, _GREEN, (cx, cy), 15, 3)
            elif el.is_anomaly and i not in selected:
                # False negative: thin red ring (missed)
                pygame.draw.circle(surface, _RED, (cx, cy), 15, 1)
            elif not el.is_anomaly and i in selected:
                # False positive: yellow X
                d = 10
                pygame.draw.line(surface, _AMBER, (cx - d, cy - d), (cx + d, cy + d), 3)
                pygame.draw.line(surface, _AMBER, (cx + d, cy - d), (cx - d, cy + d), 3)

    def _draw_score_panel(self, surface: pygame.Surface) -> None:
        r = self._result
        x = _PANEL_X + 12
        y = _TOP_H + 14

        hdr = get_font(14).render("WYNIK RUNDY", True, (155, 89, 182))
        surface.blit(hdr, (x, y))
        y += 32

        rows = [
            (f"Trafione: {r['found']}/{r['total_anomalies']}", f"+{r['found'] * 20}", _GREEN),
            (f"Falszywki: {r['false_alarms']}", f"-{r['false_alarms'] * 5}", _RED),
            ("Bonus czasu:", f"+{r['time_bonus']}", _AMBER),
        ]
        for label, val, col in rows:
            lbl_s = get_font(13).render(label, True, _DIM)
            val_s = get_font(13).render(val, True, col)
            surface.blit(lbl_s, (x, y))
            surface.blit(val_s, (_W - 20 - val_s.get_width(), y))
            y += 24

        pygame.draw.line(surface, (60, 60, 90), (x, y + 4), (_W - 12, y + 4), 1)
        y += 16

        score = r["score"]
        score_col = _GREEN if score >= 40 else (_AMBER if score >= 20 else _RED)
        sc_surf = get_font(36).render(f"{score} pkt", True, score_col)
        surface.blit(sc_surf, (_PANEL_X + (_W - _PANEL_X) // 2 - sc_surf.get_width() // 2, y))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

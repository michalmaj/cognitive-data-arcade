# src/cognitive_data_arcade/games/hypothesis_arena/scene.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.hypothesis_arena.phase_a import PhaseAScene
from cognitive_data_arcade.games.hypothesis_arena.phase_b import PhaseBScene
from cognitive_data_arcade.games.hypothesis_arena.phase_c import PhaseCScene

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    DIM as _DIM,
    ORANGE as _ORANGE,
)

_PANEL = (18, 18, 42)

_NAV_H = 48
_W = 1024
_INNER_H = 768 - _NAV_H  # 720

_PHASE_NAMES = ["Eksploracja", "Eksperyment", "Sandbox"]


class HypothesisArenaScene(Scene):
    def __init__(self, pm, strings) -> None:
        self._pm = pm
        self._strings = strings
        self._phase_switches: int = 0
        self._done: bool = False
        self._next: Scene | None = None
        self._phase_idx = 0
        self._phases: list[Scene] = [PhaseAScene(), PhaseBScene(), PhaseCScene()]
        self._inner = pygame.Surface((_W, _INNER_H))

    @property
    def _active(self) -> Scene:
        return self._phases[self._phase_idx]

    def _offset_mouse_event(self, event: pygame.event.Event, dy: int) -> pygame.event.Event:
        d = dict(event.__dict__)
        if "pos" in d:
            x, y = d["pos"]
            d["pos"] = (x, y + dy)
        return pygame.event.Event(event.type, d)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self._phase_idx = (self._phase_idx + 1) % len(self._phases)
                self._phase_switches += 1
                return
            if event.key == pygame.K_LEFT:
                self._phase_idx = (self._phase_idx - 1) % len(self._phases)
                self._phase_switches += 1
                return
            if event.key == pygame.K_q:
                self._done = True
                return
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            event = self._offset_mouse_event(event, dy=-_NAV_H)
        self._active.handle_event(event)

    def update(self, dt_ms: float = 0.0) -> None:
        self._active.update(dt_ms)

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        if self._done and self._next is None:
            self._next = self._build_next_scene()
        return self._next

    def _build_next_scene(self) -> Scene:
        from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        ap = min(100, 30 + self._phase_switches * 5)
        session = SessionResult(
            task_name="hypothesis_arena",
            participant_id=self._pm.load().device_uuid,
            session_id="sandbox_session",
            total_trials=3,
            correct_trials=min(3, self._phase_switches),
            avg_reaction_time_ms=0.0,
            min_reaction_time_ms=0.0,
            max_reaction_time_ms=0.0,
            arcade_points_earned=ap,
            science_points_earned=0,
        )
        profile_before = self._pm.load()
        badge_engine = BadgeEngine()
        new_badge_ids = badge_engine.evaluate(session, profile_before)
        self._pm.add_ap(ap)
        for bid in new_badge_ids:
            self._pm.award_badge(bid)
        profile_after = self._pm.load()
        return SessionSummaryScene(
            session=session,
            new_badge_ids=new_badge_ids,
            profile_before=profile_before,
            profile_after=profile_after,
            strings=self._strings,
            profile_manager=self._pm,
        )

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, _NAV_H))
        font = get_font(18)
        font_sm = get_font(14)
        # left/right arrows
        surface.blit(font.render("<", True, _DIM), (12, (_NAV_H - 20) // 2))
        surface.blit(font.render(">", True, _DIM), (_W - 22, (_NAV_H - 20) // 2))
        # phase tabs
        tab_w = 160
        tab_x0 = (_W - len(_PHASE_NAMES) * tab_w) // 2
        for i, name in enumerate(_PHASE_NAMES):
            tx = tab_x0 + i * tab_w
            active = i == self._phase_idx
            col = _ORANGE if active else _DIM
            lbl = f"{i + 1}. {name}"
            tw = font.size(lbl)[0]
            surface.blit(font.render(lbl, True, col), (tx + (tab_w - tw) // 2, (_NAV_H - 20) // 2))
            if active:
                pygame.draw.line(
                    surface, _ORANGE, (tx + 4, _NAV_H - 3), (tx + tab_w - 4, _NAV_H - 3), 2
                )
        # hint
        hint = font_sm.render("LEWO / PRAWO = zmien faze", True, _DIM)
        surface.blit(hint, (20, _NAV_H - 16))
        # inner scene
        self._inner.fill(_BG)
        self._active.draw(self._inner)
        surface.blit(self._inner, (0, _NAV_H))

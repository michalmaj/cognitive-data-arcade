# src/cognitive_data_arcade/games/text_tokenizer/scene.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerEngine, TokenizerState
from cognitive_data_arcade.games.text_tokenizer.phase_frequency import PhaseFrequencyScene
from cognitive_data_arcade.games.text_tokenizer.phase_ngrams import PhaseNgramsScene
from cognitive_data_arcade.games.text_tokenizer.phase_tokenizer import PhaseTokenizerScene
from cognitive_data_arcade.games.text_tokenizer.widgets import SharedInputBar, SharedState

_W, _H = 1024, 768
_INPUT_BAR_H = 48
_NAV_H = 36
_PHASE_H = _H - _INPUT_BAR_H - _NAV_H  # 684

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    DIM as _DIM,
)

_NAV_BG = (12, 12, 28)
_AMBER = (243, 156, 18)

_TAB_NAMES = ["1 - Tokenizer", "2 - N-gramy", "3 - Czestotliwosc"]
_N_TABS = len(_TAB_NAMES)


class TextTokenizerLabScene(Scene):
    def __init__(self, pm=None, strings=None) -> None:
        self._pm = pm
        self._strings = strings
        self._done = False
        self._next: Scene | None = None
        self._tab = 0
        self._tab_switches: int = 0

        self._state = SharedState()
        self._engine = TokenizerEngine()
        self._result: TokenizerState = self._recompute()

        self._input_bar = SharedInputBar(self._state)
        self._phases: list[Scene] = [
            PhaseTokenizerScene(self._state),
            PhaseNgramsScene(self._state),
            PhaseFrequencyScene(self._state),
        ]
        self._tab_rects: list[pygame.Rect] = []

    def current_tab(self) -> int:
        return self._tab

    def _recompute(self) -> TokenizerState:
        return self._engine.process(
            self._state.text,
            self._state.lowercase,
            self._state.rm_punct,
            self._state.rm_stops,
            self._state.lang,
            self._state.ngram_n,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                if not self._done and self._pm is not None:
                    self._next = self._build_next_scene()
                self._done = True
                return
            if event.key == pygame.K_RIGHT:
                self._tab = (self._tab + 1) % _N_TABS
                self._tab_switches += 1
                return
            if event.key == pygame.K_LEFT:
                self._tab = (self._tab - 1) % _N_TABS
                self._tab_switches += 1
                return

        # Tab bar click (coords in input-bar space, tab rects are within nav area)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self._tab_rects):
                adjusted_pos = (event.pos[0], event.pos[1] - _INPUT_BAR_H)
                if rect.collidepoint(adjusted_pos):
                    if i != self._tab:
                        self._tab_switches += 1
                    self._tab = i
                    return

        # Input bar (original coordinates)
        changed = self._input_bar.handle_event(event)

        # Phase events (offset y by input bar + nav height)
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            adj = _offset_mouse(event, dy=-(_INPUT_BAR_H + _NAV_H))
            self._phases[self._tab].handle_event(adj)
        elif not changed:
            self._phases[self._tab].handle_event(event)

        self._result = self._recompute()

    def update(self, dt_ms: float = 0.0) -> None:
        self._phases[self._tab].update(dt_ms)

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)

        # Input bar (top 48px)
        self._input_bar.draw(surface)

        # Nav bar (36px, below input bar)
        nav_surf = pygame.Surface((_W, _NAV_H))
        nav_surf.fill(_NAV_BG)
        pygame.draw.line(nav_surf, (40, 40, 70), (0, _NAV_H - 1), (_W, _NAV_H - 1))

        self._tab_rects = []
        font_nav = get_font(13)
        tx = 12
        for i, name in enumerate(_TAB_NAMES):
            tw = font_nav.size(name)[0] + 24
            rect = pygame.Rect(tx, 4, tw, _NAV_H - 8)
            self._tab_rects.append(rect)
            active = i == self._tab
            bg = (50, 50, 90) if active else _NAV_BG
            border = _AMBER if active else (40, 40, 70)
            pygame.draw.rect(nav_surf, bg, rect, border_radius=4)
            pygame.draw.rect(nav_surf, border, rect, 1, border_radius=4)
            col = _AMBER if active else _DIM
            lbl = font_nav.render(name, True, col)
            nav_surf.blit(lbl, (tx + 12, rect.y + (rect.h - lbl.get_height()) // 2))
            tx += tw + 6

        hint = get_font(11).render("LEWO / PRAWO = zmien faze", True, _DIM)
        nav_surf.blit(hint, (_W - hint.get_width() - 12, (_NAV_H - hint.get_height()) // 2))
        surface.blit(nav_surf, (0, _INPUT_BAR_H))

        # Phase content (remaining 636px)
        phase_surf = pygame.Surface((_W, _PHASE_H))
        phase_surf.fill(_BG)
        self._phases[self._tab].draw(phase_surf, self._result)
        surface.blit(phase_surf, (0, _INPUT_BAR_H + _NAV_H))

    def _build_next_scene(self) -> "Scene":
        from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        ap = min(100, 30 + self._tab_switches * 5)
        session = SessionResult(
            task_name="text_tokenizer_lab",
            participant_id=self._pm.load().device_uuid,
            session_id="sandbox_session",
            total_trials=3,
            correct_trials=min(3, self._tab_switches),
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


def _offset_mouse(event: pygame.event.Event, dy: int) -> pygame.event.Event:
    d = dict(event.__dict__)
    if "pos" in d:
        x, y = d["pos"]
        d["pos"] = (x, y + dy)
    return pygame.event.Event(event.type, d)

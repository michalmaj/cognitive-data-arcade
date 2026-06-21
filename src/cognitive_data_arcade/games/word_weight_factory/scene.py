# src/cognitive_data_arcade/games/word_weight_factory/scene.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.word_weight_factory.corpus import CorpusState
from cognitive_data_arcade.games.word_weight_factory.engine import WeightEngine, WeightMatrix
from cognitive_data_arcade.games.word_weight_factory.widgets import CorpusPanel
from cognitive_data_arcade.games.word_weight_factory.step_corpus import StepCorpusScene
from cognitive_data_arcade.games.word_weight_factory.step_bow import StepBowScene
from cognitive_data_arcade.games.word_weight_factory.step_tf import StepTfScene
from cognitive_data_arcade.games.word_weight_factory.step_idf import StepIdfScene
from cognitive_data_arcade.games.word_weight_factory.step_tfidf import StepTfidfScene

_W, _H = 1024, 720
_PIPE_H = 48  # pipeline bar height
_PANEL_W = 220  # CorpusPanel width
_STEP_H = _H - _PIPE_H  # 672
_STEP_W = _W - _PANEL_W  # 804

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    DIM as _DIM,
)

_NAV_BG = (12, 12, 28)
_AMBER = (243, 156, 18)

_STEP_NAMES = ["KORPUS", "BoW", "TF", "IDF", "TF-IDF"]
_N_STEPS = len(_STEP_NAMES)


class WordWeightFactoryScene(Scene):
    def __init__(self) -> None:
        self._done = False
        self._next: Scene | None = None
        self._step = 0

        self._state = CorpusState()
        self._engine = WeightEngine()
        self._matrix = self._recompute()

        self._corpus_panel = CorpusPanel(self._state)
        self._steps: list[Scene] = [
            StepCorpusScene(self._state),
            StepBowScene(self._state),
            StepTfScene(self._state),
            StepIdfScene(self._state),
            StepTfidfScene(self._state),
        ]
        self._step_label_rects: list[pygame.Rect] = []

    # ------------------------------------------------------------------
    def _recompute(self) -> WeightMatrix:
        docs_list = self._state.active_docs()
        return self._engine.process(
            docs=[text for _, text in docs_list],
            titles=[title for title, _ in docs_list],
            lowercase=self._state.lowercase,
            rm_punct=self._state.rm_punct,
            rm_stops=self._state.rm_stops,
            lang=self._state.lang,
        )

    # ------------------------------------------------------------------
    def handle_event(self, event: pygame.event.Event) -> None:
        # Pipeline step navigation keys (only when not in custom text input)
        if event.type == pygame.KEYDOWN and not self._corpus_panel.is_custom_active():
            if event.key == pygame.K_RIGHT:
                self._step = (self._step + 1) % _N_STEPS
                return
            if event.key == pygame.K_LEFT:
                self._step = (self._step - 1) % _N_STEPS
                return

        # Pipeline bar label click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self._step_label_rects):
                if rect.collidepoint(event.pos):
                    self._step = i
                    return

        # CorpusPanel (in panel-local coords: y offset by -_PIPE_H, x unchanged)
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            panel_event = _offset_mouse(event, dx=0, dy=-_PIPE_H)
            consumed = self._corpus_panel.handle_event(panel_event)
            if consumed:
                self._matrix = self._recompute()
                return
        elif event.type == pygame.KEYDOWN:
            consumed = self._corpus_panel.handle_event(event)
            if consumed:
                self._matrix = self._recompute()
                return

        # Current step scene (offset: y -= _PIPE_H, x -= _PANEL_W)
        if event.type in (
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEMOTION,
            pygame.MOUSEWHEEL,
        ):
            step_event = _offset_mouse(event, dx=-_PANEL_W, dy=-_PIPE_H)
            self._steps[self._step].handle_event(step_event)
        else:
            self._steps[self._step].handle_event(event)

        self._matrix = self._recompute()

    # ------------------------------------------------------------------
    def update(self, dt_ms: float = 0.0) -> None:
        self._steps[self._step].update(dt_ms)

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    # ------------------------------------------------------------------
    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)

        # -- Pipeline bar (top 48 px) ------------------------------------------
        pipe_surf = pygame.Surface((_W, _PIPE_H))
        pipe_surf.fill(_NAV_BG)
        pygame.draw.line(pipe_surf, (40, 40, 70), (0, _PIPE_H - 1), (_W, _PIPE_H - 1))

        self._step_label_rects = []
        font_nav = get_font(13)
        tx = 20
        for i, name in enumerate(_STEP_NAMES):
            tw = font_nav.size(name)[0] + 20
            rect = pygame.Rect(tx, 8, tw, _PIPE_H - 16)
            self._step_label_rects.append(rect)
            active = i == self._step
            bg = (50, 50, 90) if active else _NAV_BG
            border = _AMBER if active else (40, 40, 70)
            pygame.draw.rect(pipe_surf, bg, rect, border_radius=4)
            pygame.draw.rect(pipe_surf, border, rect, 1, border_radius=4)
            col = _AMBER if active else _DIM
            lbl = font_nav.render(name, True, col)
            pipe_surf.blit(lbl, (tx + 10, rect.y + (rect.h - lbl.get_height()) // 2))
            tx += tw
            # Arrow between steps
            if i < _N_STEPS - 1:
                arr = get_font(11).render("->", True, (50, 50, 80))
                pipe_surf.blit(arr, (tx + 2, rect.y + (rect.h - arr.get_height()) // 2))
                tx += 18

        hint = get_font(11).render("LEWO / PRAWO = zmien krok", True, _DIM)
        pipe_surf.blit(hint, (_W - hint.get_width() - 12, (_PIPE_H - hint.get_height()) // 2))
        surface.blit(pipe_surf, (0, 0))

        # -- Content area (below pipeline bar) --------------------------------
        content_surf = pygame.Surface((_W, _STEP_H))
        content_surf.fill(_BG)

        # Left panel (CorpusPanel)
        panel_surf = pygame.Surface((_PANEL_W, _STEP_H))
        self._corpus_panel.draw(panel_surf)
        content_surf.blit(panel_surf, (0, 0))

        # Step scene
        step_surf = pygame.Surface((_STEP_W, _STEP_H))
        self._steps[self._step].draw(step_surf, self._matrix)
        content_surf.blit(step_surf, (_PANEL_W, 0))

        surface.blit(content_surf, (0, _PIPE_H))

        # Draw CorpusPanel tooltip on top of everything (screen coords)
        self._corpus_panel.draw_tooltip(surface, _PIPE_H)


def _offset_mouse(event: pygame.event.Event, dx: int = 0, dy: int = 0) -> pygame.event.Event:
    d = dict(event.__dict__)
    if "pos" in d:
        x, y = d["pos"]
        d["pos"] = (x + dx, y + dy)
    return pygame.event.Event(event.type, d)

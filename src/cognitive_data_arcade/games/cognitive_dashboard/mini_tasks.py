from __future__ import annotations

import enum
import random
from collections.abc import Callable

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.cognitive_dashboard.config import (
    FEEDBACK_MS,
    FIXATION_MS,
    MINI_TRIALS,
    TIMEOUT_MS,
)
from cognitive_data_arcade.games.cognitive_dashboard.session import DashboardSession, TaskResult

_BG    = (26, 26, 46)
_WHITE = (240, 240, 240)
_DIM   = (100, 100, 150)
_GREEN = (39, 174, 96)
_RED   = (231, 76, 60)
_W, _H = 1024, 768


class _Phase(enum.Enum):
    FIXATION = "fixation"
    STIMULUS = "stimulus"
    FEEDBACK = "feedback"


# ── MiniRTScene ───────────────────────────────────────────────────────────────

class MiniRTScene(Scene):
    _CIRCLE_R = 80

    def __init__(self, session: DashboardSession, back_factory: Callable[[], Scene]) -> None:
        self._session = session
        self._back_factory = back_factory
        self._phase = _Phase.FIXATION
        self._timer = 0.0
        self._trial_idx = 0
        self._rt_ms: list[float] = []
        self._correct: list[bool] = []
        self._last_correct = True
        self._rt_start = 0
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if self._phase == _Phase.STIMULUS and event.key == pygame.K_SPACE:
            rt = float(pygame.time.get_ticks() - self._rt_start)
            self._record(rt, True)

    def update(self, dt_ms: float) -> None:
        self._timer += dt_ms
        if self._phase == _Phase.FIXATION and self._timer >= FIXATION_MS:
            self._phase = _Phase.STIMULUS
            self._timer = 0.0
            self._rt_start = pygame.time.get_ticks()
        elif self._phase == _Phase.STIMULUS and self._timer >= TIMEOUT_MS:
            self._record(-1.0, False)
        elif self._phase == _Phase.FEEDBACK and self._timer >= FEEDBACK_MS:
            self._advance()

    def _record(self, rt: float, correct: bool) -> None:
        self._rt_ms.append(rt)
        self._correct.append(correct)
        self._last_correct = correct
        self._phase = _Phase.FEEDBACK
        self._timer = 0.0

    def _advance(self) -> None:
        self._trial_idx += 1
        if self._trial_idx >= MINI_TRIALS:
            self._session.rt = TaskResult(
                rt_ms=self._rt_ms,
                correct=self._correct,
                condition=["simple"] * MINI_TRIALS,
            )
            self._next = self._back_factory()
            self._done = True
        else:
            self._phase = _Phase.FIXATION
            self._timer = 0.0

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()
        cx, cy = w // 2, h // 2
        font = get_font(36)

        progress = font.render(f"{self._trial_idx + 1} / {MINI_TRIALS}", True, _DIM)
        surface.blit(progress, (w - progress.get_width() - 20, 20))

        if self._phase == _Phase.FIXATION:
            f = get_font(60)
            fix = f.render("+", True, _DIM)
            surface.blit(fix, (cx - fix.get_width() // 2, cy - fix.get_height() // 2))
        elif self._phase == _Phase.STIMULUS:
            pygame.draw.circle(surface, _WHITE, (cx, cy), self._CIRCLE_R)
            hint = font.render("SPACJA", True, _DIM)
            surface.blit(hint, (cx - hint.get_width() // 2, cy + self._CIRCLE_R + 20))
        elif self._phase == _Phase.FEEDBACK:
            color = _GREEN if self._last_correct else _RED
            label = "OK" if self._last_correct else "ZA WOLNO"
            fb = get_font(48).render(label, True, color)
            surface.blit(fb, (cx - fb.get_width() // 2, cy - fb.get_height() // 2))


# ── MiniStroopScene ───────────────────────────────────────────────────────────

_STROOP_WORDS = ["CZERWONY", "ZIELONY", "NIEBIESKI"]
_STROOP_RGB = {
    "CZERWONY":  (231, 76, 60),
    "ZIELONY":   (39, 174, 96),
    "NIEBIESKI": (52, 152, 219),
}
_STROOP_KEY = {
    "CZERWONY":  pygame.K_r,
    "ZIELONY":   pygame.K_g,
    "NIEBIESKI": pygame.K_b,
}
_CONGRUENT_TRIALS = [
    ("CZERWONY", "CZERWONY"), ("ZIELONY", "ZIELONY"),
    ("NIEBIESKI", "NIEBIESKI"), ("CZERWONY", "CZERWONY"),
]
_INCONGRUENT_TRIALS = [
    ("CZERWONY", "ZIELONY"), ("ZIELONY", "NIEBIESKI"),
    ("NIEBIESKI", "CZERWONY"), ("ZIELONY", "CZERWONY"),
]


def _make_stroop_trials() -> list[dict]:
    assert len(_CONGRUENT_TRIALS) + len(_INCONGRUENT_TRIALS) == MINI_TRIALS
    trials = (
        [{"word": w, "ink": i, "condition": "congruent"} for w, i in _CONGRUENT_TRIALS]
        + [{"word": w, "ink": i, "condition": "incongruent"} for w, i in _INCONGRUENT_TRIALS]
    )
    random.shuffle(trials)
    return trials


class MiniStroopScene(Scene):
    def __init__(self, session: DashboardSession, back_factory: Callable[[], Scene]) -> None:
        self._session = session
        self._back_factory = back_factory
        self._trials = _make_stroop_trials()
        self._phase = _Phase.FIXATION
        self._timer = 0.0
        self._trial_idx = 0
        self._rt_ms: list[float] = []
        self._correct: list[bool] = []
        self._condition: list[str] = []
        self._last_correct = True
        self._rt_start = 0
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if self._phase != _Phase.STIMULUS:
            return
        t = self._trials[self._trial_idx]
        correct_key = _STROOP_KEY[t["ink"]]
        if event.key in (_STROOP_KEY[w] for w in _STROOP_WORDS):
            rt = float(pygame.time.get_ticks() - self._rt_start)
            self._record(rt, event.key == correct_key, t["condition"])

    def update(self, dt_ms: float) -> None:
        self._timer += dt_ms
        if self._phase == _Phase.FIXATION and self._timer >= FIXATION_MS:
            self._phase = _Phase.STIMULUS
            self._timer = 0.0
            self._rt_start = pygame.time.get_ticks()
        elif self._phase == _Phase.STIMULUS and self._timer >= TIMEOUT_MS:
            t = self._trials[self._trial_idx]
            self._record(-1.0, False, t["condition"])
        elif self._phase == _Phase.FEEDBACK and self._timer >= FEEDBACK_MS:
            self._advance()

    def _record(self, rt: float, correct: bool, condition: str) -> None:
        self._rt_ms.append(rt)
        self._correct.append(correct)
        self._condition.append(condition)
        self._last_correct = correct
        self._phase = _Phase.FEEDBACK
        self._timer = 0.0

    def _advance(self) -> None:
        self._trial_idx += 1
        if self._trial_idx >= MINI_TRIALS:
            self._session.stroop = TaskResult(
                rt_ms=self._rt_ms,
                correct=self._correct,
                condition=self._condition,
            )
            self._next = self._back_factory()
            self._done = True
        else:
            self._phase = _Phase.FIXATION
            self._timer = 0.0

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()
        cx, cy = w // 2, h // 2
        font_sm = get_font(28)

        progress = font_sm.render(f"{self._trial_idx + 1} / {MINI_TRIALS}", True, _DIM)
        surface.blit(progress, (w - progress.get_width() - 20, 20))

        hint = font_sm.render("R = czerwony   G = zielony   B = niebieski", True, _DIM)
        surface.blit(hint, (cx - hint.get_width() // 2, h - 50))

        if self._phase == _Phase.FIXATION:
            fix = get_font(60).render("+", True, _DIM)
            surface.blit(fix, (cx - fix.get_width() // 2, cy - fix.get_height() // 2))
        elif self._phase == _Phase.STIMULUS:
            t = self._trials[self._trial_idx]
            color = _STROOP_RGB[t["ink"]]
            word = get_font(80).render(t["word"], True, color)
            surface.blit(word, (cx - word.get_width() // 2, cy - word.get_height() // 2))
        elif self._phase == _Phase.FEEDBACK:
            color = _GREEN if self._last_correct else _RED
            label = "OK" if self._last_correct else "BLAD"
            fb = get_font(48).render(label, True, color)
            surface.blit(fb, (cx - fb.get_width() // 2, cy - fb.get_height() // 2))


# ── MiniFlankerScene ──────────────────────────────────────────────────────────

_FLANKER_TRIALS = [
    {"arrows": "<<<<<", "direction": "left",  "condition": "congruent"},
    {"arrows": ">>>>>", "direction": "right", "condition": "congruent"},
    {"arrows": "<<<<<", "direction": "left",  "condition": "congruent"},
    {"arrows": ">>>>>", "direction": "right", "condition": "congruent"},
    {"arrows": ">><>>", "direction": "left",  "condition": "incongruent"},
    {"arrows": "<<><<", "direction": "right", "condition": "incongruent"},
    {"arrows": ">><>>", "direction": "left",  "condition": "incongruent"},
    {"arrows": "<<><<", "direction": "right", "condition": "incongruent"},
]


def _make_flanker_trials() -> list[dict]:
    assert len(_FLANKER_TRIALS) == MINI_TRIALS
    trials = list(_FLANKER_TRIALS)
    random.shuffle(trials)
    return trials


class MiniFlankerScene(Scene):
    def __init__(self, session: DashboardSession, back_factory: Callable[[], Scene]) -> None:
        self._session = session
        self._back_factory = back_factory
        self._trials = _make_flanker_trials()
        self._phase = _Phase.FIXATION
        self._timer = 0.0
        self._trial_idx = 0
        self._rt_ms: list[float] = []
        self._correct: list[bool] = []
        self._condition: list[str] = []
        self._last_correct = True
        self._rt_start = 0
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if self._phase != _Phase.STIMULUS:
            return
        if event.key not in (pygame.K_LEFT, pygame.K_RIGHT):
            return
        t = self._trials[self._trial_idx]
        correct_key = pygame.K_LEFT if t["direction"] == "left" else pygame.K_RIGHT
        rt = float(pygame.time.get_ticks() - self._rt_start)
        self._record(rt, event.key == correct_key, t["condition"])

    def update(self, dt_ms: float) -> None:
        self._timer += dt_ms
        if self._phase == _Phase.FIXATION and self._timer >= FIXATION_MS:
            self._phase = _Phase.STIMULUS
            self._timer = 0.0
            self._rt_start = pygame.time.get_ticks()
        elif self._phase == _Phase.STIMULUS and self._timer >= TIMEOUT_MS:
            t = self._trials[self._trial_idx]
            self._record(-1.0, False, t["condition"])
        elif self._phase == _Phase.FEEDBACK and self._timer >= FEEDBACK_MS:
            self._advance()

    def _record(self, rt: float, correct: bool, condition: str) -> None:
        self._rt_ms.append(rt)
        self._correct.append(correct)
        self._condition.append(condition)
        self._last_correct = correct
        self._phase = _Phase.FEEDBACK
        self._timer = 0.0

    def _advance(self) -> None:
        self._trial_idx += 1
        if self._trial_idx >= MINI_TRIALS:
            self._session.flanker = TaskResult(
                rt_ms=self._rt_ms,
                correct=self._correct,
                condition=self._condition,
            )
            self._next = self._back_factory()
            self._done = True
        else:
            self._phase = _Phase.FIXATION
            self._timer = 0.0

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()
        cx, cy = w // 2, h // 2

        progress = get_font(28).render(f"{self._trial_idx + 1} / {MINI_TRIALS}", True, _DIM)
        surface.blit(progress, (w - progress.get_width() - 20, 20))

        hint = get_font(28).render("strzalka LEWO / PRAWO = kierunek srodkowej strzalki", True, _DIM)
        surface.blit(hint, (cx - hint.get_width() // 2, h - 50))

        if self._phase == _Phase.FIXATION:
            fix = get_font(60).render("+", True, _DIM)
            surface.blit(fix, (cx - fix.get_width() // 2, cy - fix.get_height() // 2))
        elif self._phase == _Phase.STIMULUS:
            t = self._trials[self._trial_idx]
            arrows = get_font(80).render(t["arrows"], True, _WHITE)
            surface.blit(arrows, (cx - arrows.get_width() // 2, cy - arrows.get_height() // 2))
        elif self._phase == _Phase.FEEDBACK:
            color = _GREEN if self._last_correct else _RED
            label = "OK" if self._last_correct else "BLAD"
            fb = get_font(48).render(label, True, color)
            surface.blit(fb, (cx - fb.get_width() // 2, cy - fb.get_height() // 2))


# ── MiniGoNoGoScene ───────────────────────────────────────────────────────────

def _make_gonogo_trials() -> list[dict]:
    trials = (
        [{"trial_type": "go"} for _ in range(MINI_TRIALS - 2)]
        + [{"trial_type": "nogo"} for _ in range(2)]
    )
    random.shuffle(trials)
    return trials


class MiniGoNoGoScene(Scene):
    _CIRCLE_R = 90

    def __init__(self, session: DashboardSession, back_factory: Callable[[], Scene]) -> None:
        self._session = session
        self._back_factory = back_factory
        self._trials = _make_gonogo_trials()
        self._phase = _Phase.FIXATION
        self._timer = 0.0
        self._trial_idx = 0
        self._rt_ms: list[float] = []
        self._correct: list[bool] = []
        self._condition: list[str] = []
        self._last_correct = True
        self._rt_start = 0
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if self._phase != _Phase.STIMULUS:
            return
        if event.key != pygame.K_SPACE:
            return
        t = self._trials[self._trial_idx]
        rt = float(pygame.time.get_ticks() - self._rt_start)
        correct = t["trial_type"] == "go"
        self._record(rt, correct, t["trial_type"])

    def update(self, dt_ms: float) -> None:
        self._timer += dt_ms
        if self._phase == _Phase.FIXATION and self._timer >= FIXATION_MS:
            self._phase = _Phase.STIMULUS
            self._timer = 0.0
            self._rt_start = pygame.time.get_ticks()
        elif self._phase == _Phase.STIMULUS and self._timer >= TIMEOUT_MS:
            t = self._trials[self._trial_idx]
            correct = t["trial_type"] == "nogo"
            self._record(-1.0, correct, t["trial_type"])
        elif self._phase == _Phase.FEEDBACK and self._timer >= FEEDBACK_MS:
            self._advance()

    def _record(self, rt: float, correct: bool, condition: str) -> None:
        self._rt_ms.append(rt)
        self._correct.append(correct)
        self._condition.append(condition)
        self._last_correct = correct
        self._phase = _Phase.FEEDBACK
        self._timer = 0.0

    def _advance(self) -> None:
        self._trial_idx += 1
        if self._trial_idx >= MINI_TRIALS:
            self._session.gonogo = TaskResult(
                rt_ms=self._rt_ms,
                correct=self._correct,
                condition=self._condition,
            )
            self._next = self._back_factory()
            self._done = True
        else:
            self._phase = _Phase.FIXATION
            self._timer = 0.0

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()
        cx, cy = w // 2, h // 2

        progress = get_font(28).render(f"{self._trial_idx + 1} / {MINI_TRIALS}", True, _DIM)
        surface.blit(progress, (w - progress.get_width() - 20, 20))

        if self._phase == _Phase.FIXATION:
            fix = get_font(60).render("+", True, _DIM)
            surface.blit(fix, (cx - fix.get_width() // 2, cy - fix.get_height() // 2))
        elif self._phase == _Phase.STIMULUS:
            t = self._trials[self._trial_idx]
            color = _GREEN if t["trial_type"] == "go" else _RED
            pygame.draw.circle(surface, color, (cx, cy), self._CIRCLE_R)
            label = "SPACJA" if t["trial_type"] == "go" else "NIE NACISKAJ"
            lbl = get_font(30).render(label, True, _WHITE)
            surface.blit(lbl, (cx - lbl.get_width() // 2, cy + self._CIRCLE_R + 16))
        elif self._phase == _Phase.FEEDBACK:
            color = _GREEN if self._last_correct else _RED
            label = "OK" if self._last_correct else "BLAD"
            fb = get_font(48).render(label, True, color)
            surface.blit(fb, (cx - fb.get_width() // 2, cy - fb.get_height() // 2))

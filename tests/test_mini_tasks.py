# tests/test_mini_tasks.py
from __future__ import annotations

from collections.abc import Callable

import pygame
import pytest

from cognitive_data_arcade.engine import fonts as _fonts_module
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.cognitive_dashboard.config import FIXATION_MS, MINI_TRIALS, TIMEOUT_MS
from cognitive_data_arcade.games.cognitive_dashboard.mini_tasks import (
    MiniFlankerScene,
    MiniGoNoGoScene,
    MiniRTScene,
    MiniStroopScene,
)
from cognitive_data_arcade.games.cognitive_dashboard.session import DashboardSession


@pytest.fixture(autouse=True)
def pg() -> None:
    pygame.init()
    _fonts_module._cache.clear()
    _fonts_module._found_name = None
    yield
    pygame.quit()


class _Stub(Scene):
    def handle_event(self, e: pygame.event.Event) -> None: pass
    def update(self, dt: float) -> None: pass
    def draw(self, s: pygame.Surface) -> None: pass
    def is_done(self) -> bool: return False


def _back() -> Callable[[], Scene]:
    return lambda: _Stub()


def _keydown(key: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, {"key": key, "mod": 0, "unicode": ""})


# ── MiniRTScene ──────────────────────────────────────────────────────────────

def test_mini_rt_not_done_initially() -> None:
    s = DashboardSession()
    scene = MiniRTScene(s, _back())
    assert not scene.is_done()


def test_mini_rt_done_after_all_trials() -> None:
    s = DashboardSession()
    scene = MiniRTScene(s, _back())
    for _ in range(MINI_TRIALS):
        scene.update(float(FIXATION_MS + 10))   # FIXATION → STIMULUS
        scene.handle_event(_keydown(pygame.K_SPACE))
        scene.update(500.0)                      # FEEDBACK → next
    assert scene.is_done()
    assert s.rt is not None
    assert len(s.rt.rt_ms) == MINI_TRIALS
    assert all(c == "simple" for c in s.rt.condition)


def test_mini_rt_timeout_records_miss() -> None:
    s = DashboardSession()
    scene = MiniRTScene(s, _back())
    scene.update(float(FIXATION_MS + 10))       # FIXATION → STIMULUS
    scene.update(float(TIMEOUT_MS + 10))        # timeout
    scene.update(500.0)                         # FEEDBACK → next trial
    # Not done yet — only 1 trial recorded
    assert not scene.is_done()


def test_mini_rt_draw_no_crash() -> None:
    s = DashboardSession()
    scene = MiniRTScene(s, _back())
    surf = pygame.Surface((1024, 768))
    scene.draw(surf)


# ── MiniStroopScene ──────────────────────────────────────────────────────────

def test_mini_stroop_conditions_balanced() -> None:
    s = DashboardSession()
    scene = MiniStroopScene(s, _back())
    for _ in range(MINI_TRIALS):
        scene.update(float(FIXATION_MS + 10))
        scene.handle_event(_keydown(pygame.K_r))
        scene.update(500.0)
    assert s.stroop is not None
    assert s.stroop.condition.count("congruent") == MINI_TRIALS // 2
    assert s.stroop.condition.count("incongruent") == MINI_TRIALS // 2


def test_mini_stroop_draw_no_crash() -> None:
    s = DashboardSession()
    scene = MiniStroopScene(s, _back())
    scene.draw(pygame.Surface((1024, 768)))


# ── MiniFlankerScene ─────────────────────────────────────────────────────────

def test_mini_flanker_conditions_balanced() -> None:
    s = DashboardSession()
    scene = MiniFlankerScene(s, _back())
    for _ in range(MINI_TRIALS):
        scene.update(float(FIXATION_MS + 10))
        scene.handle_event(_keydown(pygame.K_LEFT))
        scene.update(500.0)
    assert s.flanker is not None
    assert s.flanker.condition.count("congruent") == MINI_TRIALS // 2
    assert s.flanker.condition.count("incongruent") == MINI_TRIALS // 2


def test_mini_flanker_draw_no_crash() -> None:
    s = DashboardSession()
    scene = MiniFlankerScene(s, _back())
    scene.draw(pygame.Surface((1024, 768)))


# ── MiniGoNoGoScene ──────────────────────────────────────────────────────────

def test_mini_gonogo_conditions_count() -> None:
    s = DashboardSession()
    scene = MiniGoNoGoScene(s, _back())
    for _ in range(MINI_TRIALS):
        scene.update(float(FIXATION_MS + 10))
        scene.handle_event(_keydown(pygame.K_SPACE))
        scene.update(500.0)
    assert s.gonogo is not None
    assert s.gonogo.condition.count("go") == MINI_TRIALS - 2
    assert s.gonogo.condition.count("nogo") == 2


def test_mini_gonogo_draw_no_crash() -> None:
    s = DashboardSession()
    scene = MiniGoNoGoScene(s, _back())
    scene.draw(pygame.Surface((1024, 768)))

# tests/test_dashboard_scene.py
from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine import fonts as _fonts_module
from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.games.cognitive_dashboard.dashboard_scene import CognitiveDashboardScene
from cognitive_data_arcade.games.cognitive_dashboard.session import DashboardSession, TaskResult
from cognitive_data_arcade.profile.manager import ProfileManager


@pytest.fixture(autouse=True)
def pg() -> None:
    pygame.init()
    _fonts_module._cache.clear()
    _fonts_module._found_name = None
    yield
    pygame.quit()


def _make_result() -> TaskResult:
    return TaskResult(rt_ms=[300.0] * 8, correct=[True] * 8, condition=["simple"] * 8)


def _make_scene(tmp_path, session=None) -> CognitiveDashboardScene:
    pm = ProfileManager(tmp_path / "profile.json")
    s = session or DashboardSession()
    return CognitiveDashboardScene(s, PL, pm)


def test_not_done_initially(tmp_path) -> None:
    assert not _make_scene(tmp_path).is_done()


def test_draw_empty_session_no_crash(tmp_path) -> None:
    scene = _make_scene(tmp_path)
    scene.draw(pygame.Surface((1024, 768)))


def test_draw_complete_session_no_crash(tmp_path) -> None:
    r = _make_result()
    s = DashboardSession(rt=r, stroop=r, flanker=r, gonogo=r)
    scene = _make_scene(tmp_path, s)
    scene.draw(pygame.Surface((1024, 768)))


def test_esc_does_not_exit_scene(tmp_path) -> None:
    # ESC is intercepted by PausableGame wrapper; the scene itself stays alive
    scene = _make_scene(tmp_path)
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE, "mod": 0, "unicode": ""})
    scene.handle_event(event)
    assert not scene.is_done()


def test_synthetic_button_visible_when_empty(tmp_path) -> None:
    scene = _make_scene(tmp_path)
    assert scene._show_synthetic_button()


def test_synthetic_button_hidden_when_rt_played(tmp_path) -> None:
    r = _make_result()
    s = DashboardSession(rt=r)
    scene = _make_scene(tmp_path, s)
    assert not scene._show_synthetic_button()


def test_profile_hidden_when_incomplete(tmp_path) -> None:
    r = _make_result()
    s = DashboardSession(rt=r, stroop=r)
    scene = _make_scene(tmp_path, s)
    assert not s.is_complete()


def test_profile_visible_when_complete(tmp_path) -> None:
    r = _make_result()
    s = DashboardSession(rt=r, stroop=r, flanker=r, gonogo=r)
    assert s.is_complete()

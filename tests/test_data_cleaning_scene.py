# tests/test_data_cleaning_scene.py
from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.games.data_cleaning.scene import DataCleaningScene, Phase
from cognitive_data_arcade.games.data_cleaning.ui_popup import DecisionPopup


class _FakePM:
    def load(self):
        from cognitive_data_arcade.profile.manager import Profile
        return Profile()


def _key(k: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="")


@pytest.fixture(autouse=True)
def pg():
    pygame.init()
    yield
    pygame.quit()


def _make(seed: int = 42) -> DataCleaningScene:
    return DataCleaningScene(EN, _FakePM(), seed=seed)


# ── Initial state ───────────────────────────────────────────────────────────────

def test_initial_phase_is_intro():
    assert _make()._phase == Phase.INTRO


def test_not_done_initially():
    scene = _make()
    assert not scene.is_done()
    assert scene.next_scene() is None


# ── INTRO → IDENTIFY ────────────────────────────────────────────────────────────

def test_enter_on_intro_goes_to_identify():
    scene = _make()
    scene.handle_event(_key(pygame.K_RETURN))
    assert scene._phase == Phase.IDENTIFY


def test_space_on_intro_goes_to_identify():
    scene = _make()
    scene.handle_event(_key(pygame.K_SPACE))
    assert scene._phase == Phase.IDENTIFY


def test_other_key_on_intro_does_nothing():
    scene = _make()
    scene.handle_event(_key(pygame.K_DOWN))
    assert scene._phase == Phase.INTRO


# ── IDENTIFY navigation ─────────────────────────────────────────────────────────

def test_down_moves_cursor():
    scene = _make()
    scene._phase = Phase.IDENTIFY
    scene.handle_event(_key(pygame.K_DOWN))
    assert scene._table.cursor == 1


def test_up_does_not_go_below_zero():
    scene = _make()
    scene._phase = Phase.IDENTIFY
    scene.handle_event(_key(pygame.K_UP))
    assert scene._table.cursor == 0


def test_space_flags_current_row():
    scene = _make()
    scene._phase = Phase.IDENTIFY
    scene.handle_event(_key(pygame.K_SPACE))
    assert 0 in scene._table.flagged


def test_space_unflags_already_flagged():
    scene = _make()
    scene._phase = Phase.IDENTIFY
    scene.handle_event(_key(pygame.K_SPACE))
    scene.handle_event(_key(pygame.K_SPACE))
    assert 0 not in scene._table.flagged


# ── IDENTIFY → FIX ─────────────────────────────────────────────────────────────

def test_f_key_with_flags_goes_to_fix():
    scene = _make()
    scene._phase = Phase.IDENTIFY
    scene.handle_event(_key(pygame.K_SPACE))  # flag row 0
    scene.handle_event(_key(pygame.K_f))
    assert scene._phase == Phase.FIX


def test_f_key_builds_fix_queue():
    scene = _make()
    scene._phase = Phase.IDENTIFY
    scene.handle_event(_key(pygame.K_SPACE))  # flag row 0
    scene.handle_event(_key(pygame.K_f))
    assert 0 in scene._fix_queue


def test_f_key_with_no_flags_goes_to_report():
    scene = _make()
    scene._phase = Phase.IDENTIFY
    scene.handle_event(_key(pygame.K_f))
    assert scene._phase == Phase.REPORT


# ── FIX phase ──────────────────────────────────────────────────────────────────

def test_fix_enter_records_choice():
    scene = _make()
    scene._phase = Phase.IDENTIFY
    scene.handle_event(_key(pygame.K_SPACE))  # flag row 0
    scene.handle_event(_key(pygame.K_f))      # enter FIX
    assert scene._phase == Phase.FIX
    scene.handle_event(_key(pygame.K_RETURN))  # confirm default choice (delete)
    assert 0 in scene._fixes


def test_fix_single_item_queue_goes_to_report_after_confirm():
    scene = _make()
    scene._phase = Phase.IDENTIFY
    scene.handle_event(_key(pygame.K_SPACE))
    scene.handle_event(_key(pygame.K_f))
    scene.handle_event(_key(pygame.K_RETURN))
    assert scene._phase == Phase.REPORT


# ── REPORT → done ──────────────────────────────────────────────────────────────

def test_esc_on_report_marks_done():
    scene = _make()
    scene._phase = Phase.REPORT
    scene.handle_event(_key(pygame.K_ESCAPE))
    assert scene.is_done()


def test_enter_on_report_creates_new_scene():
    scene = _make()
    scene._phase = Phase.REPORT
    scene.handle_event(_key(pygame.K_RETURN))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), DataCleaningScene)


def test_r_on_report_replays():
    scene = _make()
    scene._phase = Phase.REPORT
    scene.handle_event(_key(pygame.K_r))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), DataCleaningScene)


# ── update ─────────────────────────────────────────────────────────────────────

def test_update_decrements_hint_timer():
    scene = _make()
    scene._hint_timer = 1000.0
    scene.update(200.0)
    assert scene._hint_timer == pytest.approx(800.0)


def test_update_does_not_go_below_zero():
    scene = _make()
    scene._hint_timer = 50.0
    scene.update(500.0)
    assert scene._hint_timer <= 0.0

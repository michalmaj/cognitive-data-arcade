# tests/test_data_cleaning_scene.py
from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine import fonts as _fonts_module
from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.games.data_cleaning.difficulty import EASY, MEDIUM, HARD
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
    _fonts_module._cache.clear()
    _fonts_module._found_name = None
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


# ── Difficulty defaults ─────────────────────────────────────────────────────────

def test_default_difficulty_is_easy():
    scene = _make()
    assert scene._difficulty == EASY


def test_hints_visible_true_when_always_mode():
    scene = _make()
    # EASY has hints_mode="always" — _hints_visible starts True
    assert scene._hints_visible is True


def test_legend_visible_starts_false():
    scene = _make()
    assert scene._legend_visible is False


# ── 1/2/3 keys set difficulty in INTRO ─────────────────────────────────────────

def test_key_1_sets_easy_in_intro():
    scene = _make()
    scene.handle_event(_key(pygame.K_1))
    assert scene._difficulty == EASY


def test_key_2_sets_medium_in_intro():
    scene = _make()
    scene.handle_event(_key(pygame.K_2))
    assert scene._difficulty == MEDIUM


def test_key_3_sets_hard_in_intro():
    scene = _make()
    scene.handle_event(_key(pygame.K_3))
    assert scene._difficulty == HARD


# ── Left/Right cycle difficulty in INTRO ────────────────────────────────────────

def test_right_arrow_cycles_to_medium():
    scene = _make()  # starts on EASY (index 0)
    scene.handle_event(_key(pygame.K_RIGHT))
    assert scene._difficulty == MEDIUM


def test_left_arrow_wraps_from_easy_to_hard():
    scene = _make()  # starts on EASY (index 0)
    scene.handle_event(_key(pygame.K_LEFT))
    assert scene._difficulty == HARD


# ── L key toggles legend ────────────────────────────────────────────────────────

def test_l_key_shows_legend_in_intro():
    scene = _make()
    scene.handle_event(_key(pygame.K_l))
    assert scene._legend_visible is True


def test_l_key_hides_legend_on_second_press():
    scene = _make()
    scene.handle_event(_key(pygame.K_l))
    scene.handle_event(_key(pygame.K_l))
    assert scene._legend_visible is False


def test_l_key_toggles_legend_in_identify():
    scene = _make()
    scene._phase = Phase.IDENTIFY
    scene.handle_event(_key(pygame.K_l))
    assert scene._legend_visible is True


# ── H key behaviour ─────────────────────────────────────────────────────────────

def test_h_key_ignored_in_always_mode():
    scene = _make()  # EASY = always
    scene._phase = Phase.IDENTIFY
    assert scene._hints_visible is True
    scene.handle_event(_key(pygame.K_h))
    assert scene._hints_visible is True  # unchanged


def test_h_key_toggles_in_toggle_mode():
    scene = DataCleaningScene(EN, _FakePM(), seed=42, difficulty=MEDIUM)
    scene._phase = Phase.IDENTIFY
    assert scene._hints_visible is False  # toggle starts False
    scene.handle_event(_key(pygame.K_h))
    assert scene._hints_visible is True
    scene.handle_event(_key(pygame.K_h))
    assert scene._hints_visible is False


def test_h_key_ignored_in_none_mode():
    scene = DataCleaningScene(EN, _FakePM(), seed=42, difficulty=HARD)
    scene._phase = Phase.IDENTIFY
    assert scene._hints_visible is False
    scene.handle_event(_key(pygame.K_h))
    assert scene._hints_visible is False


# ── ENTER in INTRO regenerates dataset with selected difficulty ─────────────────

def test_enter_generates_medium_rows():
    scene = _make()
    scene.handle_event(_key(pygame.K_2))   # select MEDIUM
    scene.handle_event(_key(pygame.K_RETURN))
    assert len(scene._session.rows) == 50
    assert scene._phase == Phase.IDENTIFY


def test_replay_preserves_difficulty():
    scene = DataCleaningScene(EN, _FakePM(), seed=42, difficulty=HARD)
    scene._phase = Phase.REPORT
    scene.handle_event(_key(pygame.K_r))
    assert scene.is_done()
    next_scene = scene.next_scene()
    assert isinstance(next_scene, DataCleaningScene)
    assert next_scene._difficulty == HARD


def _mouse(pos: tuple[int, int]) -> pygame.event.Event:
    return pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1)


def test_mouse_click_on_medium_button_sets_medium():
    scene = _make()
    surface = pygame.Surface((800, 600))
    scene.draw(surface)                              # populates _diff_rects
    assert len(scene._diff_rects) == 3
    scene.handle_event(_mouse(scene._diff_rects[1].center))
    assert scene._diff_idx == 1


def test_mouse_click_on_hard_button_sets_hard():
    scene = _make()
    surface = pygame.Surface((800, 600))
    scene.draw(surface)
    scene.handle_event(_mouse(scene._diff_rects[2].center))
    assert scene._diff_idx == 2


def test_mouse_click_outside_buttons_ignored():
    scene = _make()
    surface = pygame.Surface((800, 600))
    scene.draw(surface)
    scene.handle_event(_mouse((0, 0)))
    assert scene._diff_idx == 0   # EASY unchanged

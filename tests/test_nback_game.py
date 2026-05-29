from __future__ import annotations

from pathlib import Path

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.games.nback.config import NBackConfig, Trial
from cognitive_data_arcade.games.nback.game import NBackGame, _Phase
from cognitive_data_arcade.profile.manager import ProfileManager


def _cfg(**kw) -> NBackConfig:
    defaults = dict(
        n=1,
        trials_per_block=4,
        num_blocks=2,
        stimulus_ms=100,
        isi_ms=100,
        iti_ms=100,
        between_blocks_ms=100,
        target_rate=0.0,
    )
    defaults.update(kw)
    return NBackConfig(**defaults)


def _make(tmp_path: Path, config: NBackConfig | None = None) -> NBackGame:
    pygame.init()
    if config is None:
        config = _cfg()
    pm = ProfileManager(tmp_path / "profile.json")
    return NBackGame(config, pm, EN, "pid", "sid", tmp_path / "out.csv")


def _key(k: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="")


def _tick(game: NBackGame, ms: float) -> None:
    game.update(ms)


def test_initial_phase_is_iti(tmp_path: Path) -> None:
    game = _make(tmp_path)
    assert game._phase == _Phase.ITI


def test_iti_to_stimulus(tmp_path: Path) -> None:
    game = _make(tmp_path)
    _tick(game, 101)
    assert game._phase == _Phase.STIMULUS


def test_stimulus_to_response_window(tmp_path: Path) -> None:
    game = _make(tmp_path)
    _tick(game, 101)
    _tick(game, 101)
    assert game._phase == _Phase.RESPONSE_WINDOW


def test_response_window_commits_trial(tmp_path: Path) -> None:
    game = _make(tmp_path)
    _tick(game, 101)
    _tick(game, 101)
    _tick(game, 101)
    assert len(game._records) == 1


def test_a_key_registers_in_stimulus(tmp_path: Path) -> None:
    game = _make(tmp_path)
    _tick(game, 101)
    game.handle_event(_key(pygame.K_a))
    assert game._key_a is True


def test_l_key_registers_in_response_window(tmp_path: Path) -> None:
    game = _make(tmp_path)
    _tick(game, 101)
    _tick(game, 101)
    game.handle_event(_key(pygame.K_l))
    assert game._key_l is True


def test_key_ignored_during_iti(tmp_path: Path) -> None:
    game = _make(tmp_path)
    game.handle_event(_key(pygame.K_a))
    assert game._key_a is False


def test_pos_correct_on_hit(tmp_path: Path) -> None:
    game = _make(tmp_path)
    game._trials[1] = Trial(
        position=game._trials[0].position,
        letter=game._trials[1].letter,
        pos_match=True,
        let_match=False,
    )
    _tick(game, 101); _tick(game, 101); _tick(game, 101)
    _tick(game, 101)
    game.handle_event(_key(pygame.K_a))
    _tick(game, 101); _tick(game, 101)
    assert game._records[1].pos_correct is True


def test_false_alarm_recorded_correctly(tmp_path: Path) -> None:
    game = _make(tmp_path)
    _tick(game, 101)
    game.handle_event(_key(pygame.K_a))
    _tick(game, 101); _tick(game, 101)
    r = game._records[0]
    assert r.key_a_pressed is True
    assert r.pos_match is False
    assert r.pos_correct is False


def test_correct_rejection_recorded(tmp_path: Path) -> None:
    game = _make(tmp_path)
    _tick(game, 101); _tick(game, 101); _tick(game, 101)
    r = game._records[0]
    assert r.key_a_pressed is False
    assert r.pos_match is False
    assert r.pos_correct is True


def test_between_blocks_auto_advances(tmp_path: Path) -> None:
    game = _make(tmp_path)
    for _ in range(4):
        _tick(game, 101); _tick(game, 101); _tick(game, 101)
    assert game._phase == _Phase.BETWEEN_BLOCKS
    _tick(game, 101)
    assert game._phase == _Phase.ITI


def test_adaptive_n_increases_on_high_accuracy(tmp_path: Path) -> None:
    game = _make(tmp_path, _cfg(n=None, target_rate=0.0))
    assert game._current_n == 1
    for _ in range(4):
        _tick(game, 101); _tick(game, 101); _tick(game, 101)
    assert game._current_n == 2


def test_adaptive_n_decreases_on_low_accuracy(tmp_path: Path) -> None:
    game = _make(tmp_path, _cfg(n=None))
    game._current_n = 2
    game._trials = [Trial(0, "B", pos_match=True, let_match=True) for _ in range(4)]
    for _ in range(4):
        _tick(game, 101); _tick(game, 101); _tick(game, 101)
    assert game._current_n == 1


def test_adaptive_n_clamped_at_min(tmp_path: Path) -> None:
    game = _make(tmp_path, _cfg(n=None))
    game._current_n = 1
    game._trials = [Trial(0, "B", pos_match=True, let_match=True) for _ in range(4)]
    for _ in range(4):
        _tick(game, 101); _tick(game, 101); _tick(game, 101)
    assert game._current_n >= 1


def test_adaptive_n_clamped_at_max(tmp_path: Path) -> None:
    game = _make(tmp_path, _cfg(n=None, target_rate=0.0))
    game._current_n = 3
    for _ in range(4):
        _tick(game, 101); _tick(game, 101); _tick(game, 101)
    assert game._current_n <= 3


def test_game_done_after_all_blocks(tmp_path: Path) -> None:
    game = _make(tmp_path)
    for _ in range(8):
        _tick(game, 101); _tick(game, 101); _tick(game, 101)
        if game._phase == _Phase.BETWEEN_BLOCKS:
            _tick(game, 101)
    assert game.is_done()


def test_next_scene_none_while_running(tmp_path: Path) -> None:
    game = _make(tmp_path)
    assert game.next_scene() is None


def test_draw_without_crash(tmp_path: Path) -> None:
    pygame.init()
    surface = pygame.Surface((1024, 768))
    game = _make(tmp_path)
    game.draw(surface)
    _tick(game, 101)
    game.draw(surface)

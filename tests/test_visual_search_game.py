from __future__ import annotations

from pathlib import Path

import pygame
import pytest

from cognitive_data_arcade.engine import fonts as _fonts_module
from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.games.visual_search.config import VSConfig, TIMEOUT_MS
from cognitive_data_arcade.games.visual_search.game import (
    VisualSearchGame,
    _generate_block,
)
from cognitive_data_arcade.profile.manager import ProfileManager


@pytest.fixture(autouse=True)
def pg() -> None:
    pygame.init()
    _fonts_module._cache.clear()
    _fonts_module._found_name = None
    yield
    pygame.quit()


def _make_game(tmp_path: Path, mode: str = "letters", difficulty: str = "easy") -> VisualSearchGame:
    pm = ProfileManager(tmp_path / "profile.json")
    cfg = VSConfig(mode=mode, difficulty=difficulty)
    csv_path = tmp_path / "vs.csv"
    return VisualSearchGame(cfg, pm, PL, "pid", "sid", csv_path)


def test_generate_block_even_split() -> None:
    trials = _generate_block(8, condition="feature")
    present = [t for t in trials if t["target_present"]]
    absent  = [t for t in trials if not t["target_present"]]
    assert len(present) == 4
    assert len(absent) == 4


def test_generate_block_condition_set() -> None:
    trials = _generate_block(16, condition="conjunction")
    assert all(t["condition"] == "conjunction" for t in trials)


def test_initial_not_done(tmp_path: Path) -> None:
    assert not _make_game(tmp_path).is_done()


def test_draw_no_crash(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    surf = pygame.Surface((1024, 768))
    game.draw(surf)


def test_draw_shapes_no_crash(tmp_path: Path) -> None:
    game = _make_game(tmp_path, mode="shapes")
    surf = pygame.Surface((1024, 768))
    game.draw(surf)


def test_f_key_records_absent_response(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    # Advance through fixation (500ms) into search phase
    game.update(600.0)
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_f, "mod": 0, "unicode": "f"})
    game.handle_event(event)
    # Should now be in FEEDBACK — draw must not crash
    game.draw(pygame.Surface((1024, 768)))


def test_j_key_records_present_response(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    game.update(600.0)
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_j, "mod": 0, "unicode": "j"})
    game.handle_event(event)
    game.draw(pygame.Surface((1024, 768)))


def test_csv_written_after_response(tmp_path: Path) -> None:
    csv_path = tmp_path / "vs.csv"
    pm = ProfileManager(tmp_path / "profile.json")
    cfg = VSConfig(mode="letters", difficulty="easy")
    game = VisualSearchGame(cfg, pm, PL, "pid", "sid", csv_path)
    game.update(600.0)
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_f, "mod": 0, "unicode": "f"})
    game.handle_event(event)
    assert csv_path.exists()
    lines = csv_path.read_text().splitlines()
    assert len(lines) == 2  # header + 1 trial


def test_timeout_records_trial(tmp_path: Path) -> None:
    csv_path = tmp_path / "vs.csv"
    pm = ProfileManager(tmp_path / "profile.json")
    cfg = VSConfig(mode="letters", difficulty="easy")
    game = VisualSearchGame(cfg, pm, PL, "pid", "sid", csv_path)
    game.update(600.0)                          # advance through fixation to SEARCH
    game.update(float(TIMEOUT_MS + 100))        # advance past timeout
    game.draw(pygame.Surface((1024, 768)))      # must not crash in FEEDBACK
    assert csv_path.exists(), "CSV not written after timeout"
    lines = csv_path.read_text().splitlines()
    assert len(lines) == 2                      # header + 1 trial
    assert "timeout" in lines[1], "timeout not recorded in CSV"


def test_block_break_loads_new_trial(tmp_path: Path) -> None:
    game = _make_game(tmp_path)
    n = game._config.trials_per_block
    # Advance through all trials in block 1
    for _ in range(n):
        game.update(600.0)    # FIXATION -> SEARCH
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_f, "mod": 0, "unicode": "f"})
        game.handle_event(event)   # respond
        game.update(500.0)    # FEEDBACK -> ITI
        game.update(400.0)    # ITI -> FIXATION (ready for next)
    # Should now be in BLOCK_BREAK
    assert game._phase.value == "block_break"
    # Press ENTER to continue to block 2
    enter = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "mod": 0, "unicode": ""})
    game.handle_event(enter)
    # After pressing ENTER, _current_items should be loaded for trial index n
    assert game._trial_idx == n
    assert len(game._current_items) == game._config.set_size

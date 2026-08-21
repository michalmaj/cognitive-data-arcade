"""Beta smoke suite — end-to-end user journeys.

Each test covers a named scenario that crosses at least two components.
Tests are headless (SDL_VIDEODRIVER=dummy set in conftest.py).
"""

from __future__ import annotations

from pathlib import Path

import pygame
import pytest

from cognitive_data_arcade.engine.app_paths import AppPaths
from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.profile.manager import ProfileManager

# ── helpers ───────────────────────────────────────────────────────────────────

_SPACE = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" ")


def _make_paths(tmp_path: Path) -> AppPaths:
    return AppPaths(
        profile_dir=tmp_path,
        generated_data_dir=tmp_path / "generated",
        export_dir=tmp_path / "exports",
        asset_dir=tmp_path,
    )


def _make_pm(tmp_path: Path) -> ProfileManager:
    paths = _make_paths(tmp_path)
    return ProfileManager(tmp_path / "profile.json", app_paths=paths)


def _complete_rt_game(pm: ProfileManager, csv_path: Path) -> ReactionTimeGame:  # type: ignore[name-defined]  # noqa: F821
    """Drive a 1-trial ReactionTimeGame to completion and return it.

    Phase sequence (1 trial):
      INSTRUCTIONS -[SPACE]-> COUNTDOWN -[3100ms]-> ITI -[5000ms]-> STIMULUS
      -[SPACE]-> FEEDBACK -[700ms]-> DONE

    ITI uses 5000ms to guarantee clearing the random ITI (iti_max_ms=4000).
    """
    from cognitive_data_arcade.games.reaction_time.config import ReactionTimeConfig
    from cognitive_data_arcade.games.reaction_time.game import ReactionTimeGame

    config = ReactionTimeConfig(num_trials=1)
    game = ReactionTimeGame(config, pm, EN, "participant-smoke", "session-smoke", csv_path)

    game.handle_event(_SPACE)  # INSTRUCTIONS → COUNTDOWN
    game.update(3100.0)  # COUNTDOWN → ITI    (3 s countdown)
    game.update(5000.0)  # ITI → STIMULUS     (> iti_max_ms=4000, deterministic)
    game.handle_event(_SPACE)  # STIMULUS → FEEDBACK
    game.update(700.0)  # FEEDBACK → DONE    (feedback_duration_ms=600)

    assert game.is_done(), "game must reach DONE after driving all phases"
    return game


# ── journeys ──────────────────────────────────────────────────────────────────


@pytest.mark.smoke
def test_game_produces_csv_readable_by_dashboard(tmp_path: Path) -> None:
    """Complete game flow → CSV written → dashboard CSV loader finds it.

    Crosses: ReactionTimeGame → storage.write_trial → csv_loader.load_session_from_csv
    """
    from cognitive_data_arcade.games.cognitive_dashboard.csv_loader import (
        has_any_csv_data,
        load_session_from_csv,
    )

    pygame.init()
    try:
        pm = _make_pm(tmp_path)
        pm.load()  # initialise profile on disk
        csv_path = pm.paths.generated_data_dir / "reaction_time" / "smoke.csv"

        _complete_rt_game(pm, csv_path)

        data_root = pm.paths.generated_data_dir
        assert has_any_csv_data(data_root), "CSV must exist after game completes"
        session = load_session_from_csv(data_root)
        assert session.rt is not None, "dashboard session must have RT data after game writes CSV"
    finally:
        pygame.quit()


@pytest.mark.smoke
def test_game_completion_earns_ap_that_persists_across_reload(tmp_path: Path) -> None:
    """Completing a game awards AP that survives a fresh ProfileManager instance.

    Crosses: ReactionTimeGame._build_next_scene → ProfileManager.add_ap →
             ProfileManager.load (new instance)
    """
    pygame.init()
    try:
        pm = _make_pm(tmp_path)
        pm.load()
        csv_path = pm.paths.generated_data_dir / "reaction_time" / "smoke.csv"

        game = _complete_rt_game(pm, csv_path)
        # next_scene() awards AP as a side-effect
        next_s = game.next_scene()
        assert next_s is not None

        # Reload profile via a completely new ProfileManager instance
        pm2 = _make_pm(tmp_path)
        profile_reloaded = pm2.load()
        assert profile_reloaded.arcade_points > 0, (
            "AP earned during game must persist to a freshly loaded profile"
        )
    finally:
        pygame.quit()


@pytest.mark.smoke
def test_delete_gameplay_data_removes_csvs_preserves_profile(tmp_path: Path) -> None:
    """delete_csv_data() wipes generated CSVs but leaves profile.json intact.

    Crosses: ReactionTimeGame → storage → ProfileManager.delete_csv_data → filesystem
    """
    pygame.init()
    try:
        pm = _make_pm(tmp_path)
        pm.load()
        profile_path = tmp_path / "profile.json"
        csv_path = pm.paths.generated_data_dir / "reaction_time" / "smoke.csv"

        _complete_rt_game(pm, csv_path)
        assert csv_path.exists(), "CSV must exist before delete"
        assert profile_path.exists(), "profile must exist before delete"

        pm.delete_csv_data()

        assert not csv_path.exists(), "CSV must be gone after delete_csv_data()"
        assert not pm.paths.generated_data_dir.exists(), "generated dir must be gone"
        assert profile_path.exists(), "profile.json must survive delete_csv_data()"
    finally:
        pygame.quit()


@pytest.mark.smoke
def test_completed_game_transitions_to_summary_scene(tmp_path: Path) -> None:
    """Completed RT game produces a non-None next_scene that can be drawn.

    Crosses: ReactionTimeGame → SessionSummaryScene → draw()
    """
    import pygame

    from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

    pygame.init()
    try:
        pm = _make_pm(tmp_path)
        pm.load()
        csv_path = pm.paths.generated_data_dir / "reaction_time" / "smoke.csv"

        game = _complete_rt_game(pm, csv_path)
        summary = game.next_scene()

        assert summary is not None, "completed game must return a next scene"
        assert isinstance(summary, SessionSummaryScene)
        assert not summary.is_done(), "summary is not immediately done"

        surface = pygame.Surface((1280, 720))
        summary.draw(surface)  # must not raise
    finally:
        pygame.quit()


@pytest.mark.smoke
def test_dashboard_shows_real_data_after_game_completes(tmp_path: Path) -> None:
    """CognitiveDashboardScene opened after a completed game sees real data (no synthetic prompt).

    Crosses: ReactionTimeGame → CSV → csv_loader → CognitiveDashboardScene.show_synthetic_button()
    """
    from cognitive_data_arcade.games.cognitive_dashboard.csv_loader import load_session_from_csv
    from cognitive_data_arcade.games.cognitive_dashboard.dashboard_scene import (
        CognitiveDashboardScene,
    )

    pygame.init()
    try:
        pm = _make_pm(tmp_path)
        pm.load()
        csv_path = pm.paths.generated_data_dir / "reaction_time" / "smoke.csv"

        _complete_rt_game(pm, csv_path)

        session = load_session_from_csv(pm.paths.generated_data_dir)
        dashboard = CognitiveDashboardScene(session, EN, pm)

        # With real RT data present, the synthetic data button must be hidden
        assert not dashboard.show_synthetic_button(), (
            "synthetic data button must be hidden when real game data exists"
        )
    finally:
        pygame.quit()

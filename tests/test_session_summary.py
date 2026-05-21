from pathlib import Path

import pygame

from cognitive_data_arcade.engine.badges import SessionResult
from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import Profile, ProfileManager
from cognitive_data_arcade.ui.session_summary import SessionSummaryScene


def _make_session() -> SessionResult:
    return SessionResult(
        task_name="reaction_time",
        participant_id="p1",
        session_id="s1",
        total_trials=20,
        correct_trials=18,
        avg_reaction_time_ms=280.0,
        min_reaction_time_ms=200.0,
        max_reaction_time_ms=400.0,
        arcade_points_earned=70,
        science_points_earned=0,
    )


def _make_profile(ap: int = 0) -> Profile:
    return Profile(
        alias="tester",
        device_uuid="x",
        arcade_points=ap,
        science_points=0,
        badges=[],
        completed_lessons=[],
        language="pl",
    )


def _make_scene(
    tmp_path: Path, new_badge_ids: list[str] | None = None
) -> SessionSummaryScene:
    pygame.init()
    pm = ProfileManager(tmp_path / "profile.json")
    profile_before = _make_profile(ap=200)
    profile_after = _make_profile(ap=270)
    return SessionSummaryScene(
        session=_make_session(),
        new_badge_ids=new_badge_ids or [],
        profile_before=profile_before,
        profile_after=profile_after,
        strings=PL,
        profile_manager=pm,
    )


def test_session_summary_is_not_done_initially(tmp_path: Path) -> None:
    scene = _make_scene(tmp_path)
    assert not scene.is_done()


def test_session_summary_space_key_is_done(tmp_path: Path) -> None:
    scene = _make_scene(tmp_path)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" ")
    )
    assert scene.is_done()


def test_session_summary_esc_key_is_done(tmp_path: Path) -> None:
    scene = _make_scene(tmp_path)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )
    assert scene.is_done()


def test_session_summary_draw_does_not_crash(tmp_path: Path) -> None:
    pygame.init()
    surface = pygame.Surface((1024, 768))
    scene = _make_scene(tmp_path, new_badge_ids=["quick_reflex"])
    scene.draw(surface)


def test_session_summary_level_up_does_not_crash(tmp_path: Path) -> None:
    pygame.init()
    pm = ProfileManager(tmp_path / "profile.json")
    # before: 400 AP (Data Seedling), after: 600 AP (Data Explorer) — level changes
    profile_before = _make_profile(ap=400)
    profile_after = _make_profile(ap=600)
    scene = SessionSummaryScene(
        session=_make_session(),
        new_badge_ids=[],
        profile_before=profile_before,
        profile_after=profile_after,
        strings=PL,
        profile_manager=pm,
    )
    surface = pygame.Surface((1024, 768))
    scene.draw(surface)


def test_session_summary_next_scene_initially_none(tmp_path: Path) -> None:
    scene = _make_scene(tmp_path)
    assert scene.next_scene() is None


def test_session_summary_next_scene_after_space_is_menu(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.menu import LessonMenuScene

    scene = _make_scene(tmp_path)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" ")
    )
    assert isinstance(scene.next_scene(), LessonMenuScene)

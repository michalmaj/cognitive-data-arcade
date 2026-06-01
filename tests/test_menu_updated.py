# tests/test_menu_updated.py
from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import PL, get_strings
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.menu import LessonMenuScene
from cognitive_data_arcade.ui.profile_screen import ProfileScene


def _make_menu(tmp_path: Path) -> LessonMenuScene:
    pm = ProfileManager(tmp_path / "profile.json")
    return LessonMenuScene(pm, PL)


def test_menu_draws_without_crash(tmp_path: Path) -> None:
    pygame.init()
    surface = pygame.Surface((1024, 768))
    scene = _make_menu(tmp_path)
    scene.draw(surface)


def test_menu_p_key_transitions_to_profile(tmp_path: Path) -> None:
    scene = _make_menu(tmp_path)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p, mod=0, unicode="p")
    )
    assert scene.is_done()
    assert isinstance(scene.next_scene(), ProfileScene)


def test_menu_l_key_toggles_language_and_persists(tmp_path: Path) -> None:
    pm = ProfileManager(tmp_path / "profile.json")
    scene = LessonMenuScene(pm, PL)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_l, mod=0, unicode="l")
    )
    assert not scene.is_done()
    assert pm.load().language == "en"


def test_menu_l_key_updates_subtitle(tmp_path: Path) -> None:
    pm = ProfileManager(tmp_path / "profile.json")
    scene = LessonMenuScene(pm, PL)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_l, mod=0, unicode="l")
    )
    en_strings = get_strings("en")
    assert scene._strings.menu_subtitle == en_strings.menu_subtitle


def test_menu_esc_key_exits(tmp_path: Path) -> None:
    scene = _make_menu(tmp_path)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )
    assert scene.is_done()
    assert scene.next_scene() is None


def test_menu_enter_on_lesson_7_launches_stroop(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    pygame.init()
    scene = _make_menu(tmp_path)
    for _ in range(6):
        scene.handle_event(
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode="")
        )
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )
    assert scene.is_done()
    assert isinstance(scene.next_scene(), HowToPlayScene)


def test_menu_z_key_launches_stroop_picker(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.stroop_session_picker import StroopSessionPickerScene

    scene = _make_menu(tmp_path)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_z, mod=0, unicode="z")
    )
    assert scene.is_done()
    assert isinstance(scene.next_scene(), StroopSessionPickerScene)


def test_menu_enter_on_non_stroop_lesson_does_nothing(tmp_path: Path) -> None:
    scene = _make_menu(tmp_path)
    # Navigate to lesson 3 (index 2), which should not launch anything
    for _ in range(2):
        scene.handle_event(
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode="")
        )
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )
    assert not scene.is_done()


def test_return_on_lesson2_launches_rt_lab(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    pygame.init()
    scene = _make_menu(tmp_path)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode="")
    )
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )
    assert scene.is_done()
    assert isinstance(scene.next_scene(), HowToPlayScene)


def test_return_on_lesson1_launches_big_data_map(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    pygame.init()
    scene = _make_menu(tmp_path)
    # _selected starts at 0, which is lesson 1 in _LESSONS
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="")
    )
    assert scene.is_done()
    assert isinstance(scene.next_scene(), HowToPlayScene)


def test_return_on_lesson8_launches_flanker(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    pygame.init()
    scene = _make_menu(tmp_path)
    for _ in range(7):
        scene.handle_event(
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode="")
        )
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )
    assert scene.is_done()
    assert isinstance(scene.next_scene(), HowToPlayScene)


def test_return_on_lesson9_launches_gono(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    pygame.init()
    scene = _make_menu(tmp_path)
    for _ in range(8):
        scene.handle_event(
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode="")
        )
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )
    assert scene.is_done()
    assert isinstance(scene.next_scene(), HowToPlayScene)


def test_return_on_lesson10_launches_nback(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.nback_level_scene import NBackLevelScene

    pygame.init()
    scene = _make_menu(tmp_path)
    for _ in range(9):
        scene.handle_event(
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode="")
        )
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )
    assert scene.is_done()
    assert isinstance(scene.next_scene(), NBackLevelScene)

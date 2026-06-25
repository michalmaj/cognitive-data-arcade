"""Tests for QuizScene — checkpoint multiple-choice question."""

from pathlib import Path

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.quiz_scene import QuizScene


@pytest.fixture(autouse=True)
def _display():
    pygame.init()
    pygame.display.set_mode((1024, 640))
    yield
    pygame.quit()


def _pm(tmp_path: Path) -> ProfileManager:
    pm = ProfileManager(tmp_path / "p.json")
    pm.load()
    return pm


def _key(k: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="")


def test_quiz_initial_not_done(tmp_path: Path) -> None:
    from unittest.mock import MagicMock
    from cognitive_data_arcade.engine.scene import Scene

    back = MagicMock(spec=Scene)
    scene = QuizScene(lesson_num=2, pm=_pm(tmp_path), strings=PL, back_scene=back)
    assert not scene.is_done()


def test_quiz_key_1_selects_option_0(tmp_path: Path) -> None:
    from unittest.mock import MagicMock
    from cognitive_data_arcade.engine.scene import Scene

    back = MagicMock(spec=Scene)
    scene = QuizScene(lesson_num=2, pm=_pm(tmp_path), strings=PL, back_scene=back)
    scene.handle_event(_key(pygame.K_1))
    assert scene._selected == 0


def test_quiz_key_2_selects_option_1(tmp_path: Path) -> None:
    from unittest.mock import MagicMock
    from cognitive_data_arcade.engine.scene import Scene

    back = MagicMock(spec=Scene)
    scene = QuizScene(lesson_num=2, pm=_pm(tmp_path), strings=PL, back_scene=back)
    scene.handle_event(_key(pygame.K_2))
    assert scene._selected == 1


def test_quiz_confirm_correct_records_true(tmp_path: Path) -> None:
    from unittest.mock import MagicMock
    from cognitive_data_arcade.engine.scene import Scene

    pm = _pm(tmp_path)
    back = MagicMock(spec=Scene)
    # Lesson 2 correct answer is index 2 (K_3)
    scene = QuizScene(lesson_num=2, pm=pm, strings=PL, back_scene=back)
    scene.handle_event(_key(pygame.K_3))
    scene.handle_event(_key(pygame.K_RETURN))
    assert scene.is_done()
    assert pm.load().quiz_results.get("L2") is True


def test_quiz_confirm_wrong_records_false(tmp_path: Path) -> None:
    from unittest.mock import MagicMock
    from cognitive_data_arcade.engine.scene import Scene

    pm = _pm(tmp_path)
    back = MagicMock(spec=Scene)
    # Select option 0 (wrong for lesson 2)
    scene = QuizScene(lesson_num=2, pm=pm, strings=PL, back_scene=back)
    scene.handle_event(_key(pygame.K_1))
    scene.handle_event(_key(pygame.K_RETURN))
    assert scene.is_done()
    assert pm.load().quiz_results.get("L2") is False


def test_quiz_esc_skips_without_recording(tmp_path: Path) -> None:
    from unittest.mock import MagicMock
    from cognitive_data_arcade.engine.scene import Scene

    pm = _pm(tmp_path)
    back = MagicMock(spec=Scene)
    scene = QuizScene(lesson_num=2, pm=pm, strings=PL, back_scene=back)
    scene.handle_event(_key(pygame.K_ESCAPE))
    assert scene.is_done()
    assert "L2" not in pm.load().quiz_results


def test_quiz_draw_does_not_crash(tmp_path: Path) -> None:
    from unittest.mock import MagicMock
    from cognitive_data_arcade.engine.scene import Scene

    back = MagicMock(spec=Scene)
    scene = QuizScene(lesson_num=7, pm=_pm(tmp_path), strings=PL, back_scene=back)
    surface = pygame.display.get_surface()
    scene.draw(surface)
    scene.handle_event(_key(pygame.K_2))
    scene.draw(surface)  # with selection

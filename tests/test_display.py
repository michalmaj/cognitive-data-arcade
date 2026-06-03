from unittest.mock import patch

import pygame
import pytest

from cognitive_data_arcade.engine import display


@pytest.fixture(autouse=True)
def no_display():
    pygame.display.quit()
    yield
    pygame.display.quit()


def test_init_false_sets_not_fullscreen() -> None:
    display.init(False)
    assert display.is_fullscreen() is False


def test_init_true_sets_fullscreen() -> None:
    display.init(True)
    assert display.is_fullscreen() is True


def test_toggle_flips_state() -> None:
    display.init(False)
    display.toggle()
    assert display.is_fullscreen() is True
    display.toggle()
    assert display.is_fullscreen() is False


def test_apply_reverts_state_on_pygame_error() -> None:
    pygame.display.init()
    pygame.display.set_mode((100, 100))
    display.init(False)

    with patch("pygame.display.set_mode", side_effect=pygame.error("mode switch failed")):
        display.toggle()  # tries fullscreen, set_mode raises, should revert

    assert display.is_fullscreen() is False  # reverted back

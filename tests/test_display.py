from unittest.mock import call, patch

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


def test_apply_calls_toggle_fullscreen_when_state_differs() -> None:
    pygame.display.init()
    pygame.display.set_mode((100, 100))  # windowed, no FULLSCREEN flag
    display.init(False)  # state = windowed, surface = windowed → no toggle

    with patch("pygame.display.toggle_fullscreen") as mock_toggle:
        display.toggle()  # state → True, surface still windowed → must call toggle
        assert mock_toggle.call_count == 1

        # Mock didn't actually change the surface, so surface is still windowed.
        # _fullscreen is now True; currently is False → differs → toggle again.
        display.init(False)  # force _fullscreen=False; surface=windowed → same → no call
        assert mock_toggle.call_count == 1  # unchanged


def test_apply_skips_toggle_when_state_matches() -> None:
    pygame.display.init()
    pygame.display.set_mode((100, 100))
    display.init(False)  # windowed state, windowed surface

    with patch("pygame.display.toggle_fullscreen") as mock_toggle:
        display.init(False)  # same state as surface → no toggle
        mock_toggle.assert_not_called()

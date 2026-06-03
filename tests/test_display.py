from cognitive_data_arcade.engine import display


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

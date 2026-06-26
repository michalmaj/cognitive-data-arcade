from cognitive_data_arcade.engine.lesson_registry import lesson_available


def test_known_lesson_available():
    assert lesson_available(1) is True
    assert lesson_available(32) is True


def test_unknown_lesson_not_available():
    assert lesson_available(0) is False
    assert lesson_available(33) is False

import time
from cognitive_data_arcade.engine.timing import now_ms, elapsed_ms


def test_now_ms_returns_positive_float() -> None:
    assert now_ms() > 0.0


def test_elapsed_ms_is_positive_after_sleep() -> None:
    start = now_ms()
    time.sleep(0.01)
    assert elapsed_ms(start) > 0.0


def test_elapsed_ms_is_at_least_sleep_duration() -> None:
    start = now_ms()
    time.sleep(0.05)
    # Allow 5 ms tolerance for scheduler jitter.
    assert elapsed_ms(start) >= 45.0

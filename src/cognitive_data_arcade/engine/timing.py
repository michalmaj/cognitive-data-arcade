import time


def now_ms() -> float:
    """Return current monotonic time in milliseconds."""
    return time.perf_counter() * 1000.0


def elapsed_ms(start_ms: float) -> float:
    """Return milliseconds elapsed since start_ms."""
    return now_ms() - start_ms

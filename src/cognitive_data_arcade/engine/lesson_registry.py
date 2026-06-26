"""Nuitka-safe lesson availability check.

This module provides a simple frozenset-based approach to check if a lesson
is available. It replaces importlib.util.find_spec() which is unreliable
in Nuitka onefile compiled binaries where all modules are compiled into
a single executable.
"""

_AVAILABLE = frozenset(range(1, 33))  # lesson_01 … lesson_32 all ship with v0.9.0


def lesson_available(lesson_num: int) -> bool:
    """Check if a lesson number is available.

    Args:
        lesson_num: The lesson number to check (1-32 are available in v0.9.0).

    Returns:
        True if the lesson is available, False otherwise.
    """
    return lesson_num in _AVAILABLE

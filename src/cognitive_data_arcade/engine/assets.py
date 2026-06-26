"""Asset path resolver — returns the assets/ directory in dev and frozen (Nuitka/PyInstaller) modes."""

from __future__ import annotations

import sys
from pathlib import Path


def assets_dir() -> Path:
    """Return the ``assets/`` root directory.

    Works in three contexts:
    - ``uv run`` / development: resolves relative to this file's location.
    - Nuitka onefile standalone: ``sys.frozen`` is set; resolves relative to the executable.
    - PyInstaller: same as Nuitka.
    """
    if getattr(sys, "frozen", False):
        # Frozen binary (Nuitka --onefile or PyInstaller):
        # assets/ is extracted next to the executable.
        return Path(sys.executable).parent / "assets"
    # Development: this file lives at src/cognitive_data_arcade/engine/assets.py
    # parents: [0]=engine/, [1]=cognitive_data_arcade/, [2]=src/, [3]=project root
    return Path(__file__).parents[3] / "assets"

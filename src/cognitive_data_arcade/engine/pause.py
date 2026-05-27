from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameInfo:
    title: str
    description_lines: list[str]
    key_bindings: list[tuple[str, str]]

from __future__ import annotations

from abc import ABC, abstractmethod

import pygame


class Scene(ABC):
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None: ...

    @abstractmethod
    def update(self, dt_ms: float) -> None: ...

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...

    @abstractmethod
    def is_done(self) -> bool: ...

    def next_scene(self) -> Scene | None:
        return None

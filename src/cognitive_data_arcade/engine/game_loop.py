from __future__ import annotations

import pygame

from cognitive_data_arcade.engine import display as _display
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager


class GameLoop:
    FPS = 60

    def __init__(
        self, initial_scene: Scene, width: int = 1024, height: int = 768,
        pm: ProfileManager | None = None,
    ) -> None:
        self._scene: Scene | None = initial_scene
        self._width = width
        self._height = height
        self._pm = pm

    def run(self, fullscreen: bool = False) -> None:
        pygame.init()
        pygame.display.set_mode((self._width, self._height))
        _display.init(fullscreen)
        pygame.display.set_caption("Cognitive Data Arcade")
        pygame.mouse.set_visible(True)
        clock = pygame.time.Clock()

        while self._scene is not None:
            dt_ms = clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    _display.toggle()
                    if self._pm is not None:
                        self._pm.set_fullscreen(_display.is_fullscreen())
                else:
                    self._scene.handle_event(event)
            self._scene.update(dt_ms)
            screen = pygame.display.get_surface()
            if screen is None:
                continue
            screen.fill((26, 26, 46))
            self._scene.draw(screen)
            pygame.display.flip()
            if self._scene.is_done():
                self._scene = self._scene.next_scene()

        pygame.quit()

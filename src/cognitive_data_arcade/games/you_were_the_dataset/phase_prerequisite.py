# src/cognitive_data_arcade/games/you_were_the_dataset/phase_prerequisite.py
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pygame

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
)
from cognitive_data_arcade.engine.colors import (
    DIM as _DIM,
)
from cognitive_data_arcade.engine.colors import (
    GREEN as _GREEN,
)
from cognitive_data_arcade.engine.colors import (
    RED as _RED,
)
from cognitive_data_arcade.engine.colors import (
    WHITE as _WHITE,
)
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.you_were_the_dataset.game_state import GameState
from cognitive_data_arcade.games.you_were_the_dataset.profile_loader import (
    REQUIRED_GAMES,
    check_prerequisites,
)

_W, _H = 1024, 768
_PANEL = (18, 22, 38)
_BTN_W, _BTN_H = 160, 34


class _GameLauncher(Scene):
    """Wraps an inner game chain; when the chain ends, returns a fresh PhasePrerequisiteScene."""

    def __init__(
        self,
        inner: Scene,
        state: GameState,
        game_factories: dict[str, Callable[[], Scene]],
        data_dir: Path,
    ) -> None:
        self._current = inner
        self._state = state
        self._factories = game_factories
        self._data_dir = data_dir
        self._chain_done = False

    def handle_event(self, event: pygame.event.Event) -> None:
        self._current.handle_event(event)

    def update(self, dt_ms: float = 0.0) -> None:
        self._current.update(dt_ms)
        if self._current.is_done():
            nxt = self._current.next_scene()
            if nxt is None:
                self._chain_done = True
            elif type(nxt).__name__ == "LessonMenuScene":
                # Inner game chain returned to menu — treat as complete.
                # Using name check to avoid circular import.
                self._chain_done = True
            else:
                self._current = nxt

    def draw(self, surface: pygame.Surface) -> None:
        self._current.draw(surface)

    def is_done(self) -> bool:
        return self._chain_done

    def next_scene(self) -> Scene | None:
        return PhasePrerequisiteScene(self._state, self._factories, self._data_dir)


class PhasePrerequisiteScene(Scene):
    def __init__(
        self,
        state: GameState,
        game_factories: dict[str, Callable[[], Scene]],
        _data_dir: Path | None = None,
    ) -> None:
        self._state = state
        self._factories = game_factories
        self._data_dir = _data_dir
        self._statuses: dict[str, bool] = (
            check_prerequisites(self._data_dir) if self._data_dir else {}
        )
        self._done = False
        self._next: Scene | None = None

        # Build button rects for missing games
        self._btn_rects: dict[str, pygame.Rect] = {}
        self._all_done = all(self._statuses.values())
        if self._all_done:
            self._continue_rect = pygame.Rect(_W // 2 - 130, _H - 90, 260, 50)
        else:
            self._continue_rect = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._done:
            return
        if event.type == pygame.KEYDOWN:
            # Hidden dev shortcut: Ctrl+D loads synthetic data
            if event.key == pygame.K_d and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                from cognitive_data_arcade.games.you_were_the_dataset.phase_reveal import (
                    PhaseRevealScene,
                )
                from cognitive_data_arcade.games.you_were_the_dataset.synthetic_data import (
                    SYNTHETIC_PROFILE,
                )

                self._state.profile = SYNTHETIC_PROFILE
                self._next = PhaseRevealScene(self._state)
                self._done = True
                return
            if event.key == pygame.K_SPACE and self._all_done:
                self._advance_to_reveal()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (
                self._all_done
                and self._continue_rect
                and self._continue_rect.collidepoint(event.pos)
            ):
                self._advance_to_reveal()
            for name, rect in self._btn_rects.items():
                if rect.collidepoint(event.pos) and name in self._factories:
                    inner = self._factories[name]()
                    self._next = _GameLauncher(inner, self._state, self._factories, self._data_dir)
                    self._done = True
                    return

    def _advance_to_reveal(self) -> None:
        from cognitive_data_arcade.games.you_were_the_dataset.phase_reveal import PhaseRevealScene

        self._next = PhaseRevealScene(self._state)
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)

        # Header
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 60))
        title = get_font(26).render("You Were the Dataset", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 16))

        # Subtitle
        sub = get_font(16).render(
            "Aby zobaczyc swoj kognitywny profil, potrzebujesz danych z tych gier:",
            True,
            _DIM,
        )
        surface.blit(sub, (_W // 2 - sub.get_width() // 2, 80))

        # Game list
        list_names = list(REQUIRED_GAMES.keys())
        row_h = 52
        list_top = 120
        list_w = 600
        list_x = (_W - list_w) // 2

        self._btn_rects.clear()

        for i, name in enumerate(list_names):
            label = REQUIRED_GAMES[name]
            has_data = self._statuses.get(name, False)
            row_y = list_top + i * row_h
            row_rect = pygame.Rect(list_x, row_y, list_w, row_h - 6)

            bg = (20, 38, 24) if has_data else (38, 20, 20)
            pygame.draw.rect(surface, bg, row_rect, border_radius=6)

            border_col = _GREEN if has_data else _RED
            pygame.draw.rect(surface, border_col, row_rect, 2, border_radius=6)

            icon = get_font(18).render("+" if has_data else "x", True, border_col)
            surface.blit(icon, (list_x + 14, row_y + 14))

            lbl = get_font(16).render(label, True, _WHITE)
            surface.blit(lbl, (list_x + 42, row_y + 16))

            if has_data:
                ok_txt = get_font(13).render("data present", True, _GREEN)
                surface.blit(ok_txt, (list_x + list_w - ok_txt.get_width() - 12, row_y + 18))
            else:
                btn_rect = pygame.Rect(list_x + list_w - _BTN_W - 8, row_y + 9, _BTN_W, _BTN_H)
                pygame.draw.rect(surface, _RED, btn_rect, border_radius=5)
                btn_txt = get_font(14).render("Zagraj teraz ->", True, _WHITE)
                surface.blit(
                    btn_txt,
                    (
                        btn_rect.x + (_BTN_W - btn_txt.get_width()) // 2,
                        btn_rect.y + (_BTN_H - btn_txt.get_height()) // 2,
                    ),
                )
                self._btn_rects[name] = btn_rect

        # Footer / Continue button
        if self._all_done and self._continue_rect:
            pygame.draw.rect(surface, _GREEN, self._continue_rect, border_radius=8)
            cont = get_font(20).render("Kontynuuj  [SPACJA]", True, (0, 0, 0))
            surface.blit(
                cont,
                (
                    _W // 2 - cont.get_width() // 2,
                    self._continue_rect.y + (50 - cont.get_height()) // 2,
                ),
            )
        else:
            foot = get_font(13).render(
                "Zagraj w brakujace gry, a lista zaktualizuje się.", True, _DIM
            )
            surface.blit(foot, (_W // 2 - foot.get_width() // 2, _H - 40))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

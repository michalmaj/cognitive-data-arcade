"""ActIntroScene — full-screen narrative intro shown once per module/act."""

from __future__ import annotations

import pygame

from cognitive_data_arcade.data.act_content import ACT_INTROS
from cognitive_data_arcade.engine.colors import BG as _BG, WHITE as _WHITE
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

_ACCENT = (99, 102, 241)
_DIM = (90, 96, 144)
_SURFACE = (22, 24, 40)


class ActIntroScene(Scene):
    """Full-screen intro card shown before the first game of a module/act."""

    def __init__(
        self,
        module_idx: int,
        pm: ProfileManager,
        strings: Strings,
        back_scene: Scene,
    ) -> None:
        self._module_idx = module_idx
        self._pm = pm
        self._strings = strings
        self._back = back_scene
        self._done = False
        self._next: Scene | None = None
        self._content = ACT_INTROS[module_idx]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._confirm()
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self._next = self._back
            self._done = True
        elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
            self._confirm()

    def _confirm(self) -> None:
        self._pm.set_seen_act_intro(self._module_idx)
        self._next = self._back
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()

        # Top accent bar
        pygame.draw.rect(surface, _ACCENT, (0, 0, w, 4))

        # Act number chip
        is_pl = self._strings.language == "pl"
        act_num = get_font(16).render(
            f"AKT {self._module_idx + 1} / 6" if is_pl else f"ACT {self._module_idx + 1} / 6",
            True,
            _ACCENT,
        )
        surface.blit(act_num, (60, 24))

        # Title
        key = "title_pl" if is_pl else "title_en"
        title = get_font(36).render(self._content[key], True, _WHITE)
        surface.blit(title, (60, 56))

        # Separator
        pygame.draw.line(surface, (40, 42, 70), (60, 108), (w - 60, 108))

        # Body text (multi-line)
        text_key = "text_pl" if is_pl else "text_en"
        body_font = get_font(22)
        y = 128
        for line in self._content[text_key].split("\n"):
            if line.strip() == "":
                y += 14
                continue
            surf = body_font.render(line, True, _DIM)
            surface.blit(surf, (60, y))
            y += body_font.get_height() + 6

        # Hint at bottom
        hint_text = "SPACJA - zaczynamy" if is_pl else "SPACE - let's go"
        hint = get_font(18).render(hint_text, True, (60, 63, 110))
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 44))


def make_act_intro(
    pm: ProfileManager,
    module_idx: int,
    strings: Strings,
    back_scene: Scene,
) -> Scene:
    """Return ActIntroScene if module intro not yet seen, else back_scene directly."""
    if module_idx in pm.load().seen_act_intros:
        return back_scene
    return ActIntroScene(module_idx=module_idx, pm=pm, strings=strings, back_scene=back_scene)

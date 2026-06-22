from __future__ import annotations

import math
from typing import Callable

import pygame
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.engine.colors import BG as _BG, ORANGE as _ORANGE

from .concept_data import CONCEPT_NODES, CONCEPT_EDGES, MODULE_COLORS, MODULE_NAMES, LessonNode

_W, _H = 1024, 768
_TITLE_H = 40
_INFO_H = 60
_CX = _W // 2
_CY = _TITLE_H + (_H - _TITLE_H - _INFO_H) // 2   # = 374

_R_MODULE = 190    # radius for module name labels
_R_NODE = 270      # radius for lesson nodes
_NODE_R = 22       # node circle radius
_MODULE_ARC = 60   # degrees per module (6 x 60 = 360)
_ARC_MARGIN = 5    # degrees gap at each end of module arc

_TEXT_LIGHT = (240, 240, 240)
_TEXT_DIM = (100, 100, 140)
_LINE_COLOR = (28, 28, 55)
_LINE_ACTIVE = (70, 70, 120)
_SELECTED_RING = (255, 220, 50)


def _deg2rad(deg: float) -> float:
    return math.radians(deg)


def _polar(cx: int, cy: int, r: float, deg: float) -> tuple[int, int]:
    """Convert polar coords (degrees, 0=top, clockwise) to screen xy."""
    rad = _deg2rad(deg - 90)  # -90 so 0 degrees = top
    return (cx + int(r * math.cos(rad)), cy + int(r * math.sin(rad)))


def _lighten(color: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(min(255, c + 50) for c in color)  # type: ignore[return-value]


def _darken(color: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(max(0, c - 60) for c in color)  # type: ignore[return-value]


def _compute_positions() -> dict[int, tuple[int, int]]:
    """Returns {lesson_num: (x, y)} for all nodes."""
    positions: dict[int, tuple[int, int]] = {}
    # Group nodes by module
    by_module: dict[int, list[LessonNode]] = {}
    for node in CONCEPT_NODES:
        by_module.setdefault(node.module, []).append(node)

    for mod_idx, (mod_num, nodes) in enumerate(sorted(by_module.items())):
        arc_start = mod_idx * _MODULE_ARC
        arc_end = arc_start + _MODULE_ARC
        usable_start = arc_start + _ARC_MARGIN
        usable_end = arc_end - _ARC_MARGIN
        n = len(nodes)
        if n == 1:
            angles = [(usable_start + usable_end) / 2]
        else:
            step = (usable_end - usable_start) / (n - 1)
            angles = [usable_start + i * step for i in range(n)]
        for node, angle in zip(nodes, angles):
            positions[node.lesson_num] = _polar(_CX, _CY, _R_NODE, angle)
    return positions


class BigDataMapGame(Scene):
    def __init__(
        self,
        strings: Strings,
        profile_manager: ProfileManager,
        lesson_reader_factory: Callable[[int], Scene] | None = None,
    ) -> None:
        self._strings = strings
        self._pm = profile_manager
        self._lesson_reader_factory = lesson_reader_factory
        self._done = False
        self._next: Scene | None = None

        self._positions = _compute_positions()  # {lesson_num: (x,y)}
        self._node_by_pos: list[tuple[pygame.Rect, LessonNode]] = []  # hit rects

        self._hovered: int | None = None   # lesson_num
        self._selected: int | None = None  # lesson_num (keyboard nav)

        self._font_title = get_font(28)
        self._font_node = get_font(15)
        self._font_module = get_font(16)
        self._font_info = get_font(20)

        # Build hit rects
        for node in CONCEPT_NODES:
            x, y = self._positions[node.lesson_num]
            rect = pygame.Rect(x - _NODE_R, y - _NODE_R, _NODE_R * 2, _NODE_R * 2)
            self._node_by_pos.append((rect, node))

        # Build node lookup
        self._node_map: dict[int, LessonNode] = {n.lesson_num: n for n in CONCEPT_NODES}

        # Keyboard navigation: ordered list of lesson nums
        self._nav_order = [n.lesson_num for n in CONCEPT_NODES]
        self._nav_idx = 0
        self._selected = self._nav_order[0]

    def _navigate_to(self, lesson_num: int) -> None:
        """Open the lesson reader for the given lesson number."""
        if self._lesson_reader_factory is not None:
            audio.play_sfx("navigate")
            self._next = self._lesson_reader_factory(lesson_num)
            self._done = True

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            from cognitive_data_arcade.engine.mouse import hit
            self._hovered = None
            for rect, node in self._node_by_pos:
                if hit(rect, event.pos):
                    self._hovered = node.lesson_num
                    break
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            from cognitive_data_arcade.engine.mouse import hit
            for rect, node in self._node_by_pos:
                if hit(rect, event.pos):
                    if self._selected == node.lesson_num:
                        # Second click on already-selected node -> navigate
                        self._navigate_to(node.lesson_num)
                    else:
                        # First click -> select
                        self._selected = node.lesson_num
                        # Sync nav_idx
                        if node.lesson_num in self._nav_order:
                            self._nav_idx = self._nav_order.index(node.lesson_num)
                        audio.play_sfx("navigate")
                    break
            return

        if event.type != pygame.KEYDOWN:
            return

        key = event.key
        n = len(self._nav_order)

        if key in (pygame.K_UP, pygame.K_RIGHT):
            self._nav_idx = (self._nav_idx - 1) % n
            self._selected = self._nav_order[self._nav_idx]
            audio.play_sfx("navigate")
        elif key in (pygame.K_DOWN, pygame.K_LEFT):
            self._nav_idx = (self._nav_idx + 1) % n
            self._selected = self._nav_order[self._nav_idx]
            audio.play_sfx("navigate")
        elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            if self._selected is not None:
                self._navigate_to(self._selected)
        # K_ESCAPE is handled by PausableGame

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_title(surface)
        self._draw_module_labels(surface)
        self._draw_edges(surface)
        self._draw_nodes(surface)
        self._draw_info_bar(surface)

    def _draw_title(self, surface: pygame.Surface) -> None:
        title = "Siec Pojec - Cognitive Data Arcade"
        rendered = self._font_title.render(title, True, _ORANGE)
        surface.blit(rendered, (16, (_TITLE_H - rendered.get_height()) // 2))

    def _draw_module_labels(self, surface: pygame.Surface) -> None:
        by_module: dict[int, list[LessonNode]] = {}
        for node in CONCEPT_NODES:
            by_module.setdefault(node.module, []).append(node)

        for mod_idx, (mod_num, _nodes) in enumerate(sorted(by_module.items())):
            arc_start = mod_idx * _MODULE_ARC
            arc_mid = arc_start + _MODULE_ARC / 2
            mx, my = _polar(_CX, _CY, _R_MODULE, arc_mid)
            color = MODULE_COLORS[mod_num]
            lang = self._strings.language if hasattr(self._strings, "language") else "pl"
            name_idx = 0 if lang == "pl" else 1
            name = MODULE_NAMES[mod_num][name_idx]
            # Render short name (split long names at space)
            words = name.split()
            if len(words) > 2:
                line1 = " ".join(words[:2])
                line2 = " ".join(words[2:])
                lines = [line1, line2]
            else:
                lines = [name]
            line_h = self._font_module.get_height()
            total_h = len(lines) * line_h
            y0 = my - total_h // 2
            for line in lines:
                rendered = self._font_module.render(line, True, color)
                surface.blit(rendered, (mx - rendered.get_width() // 2, y0))
                y0 += line_h

    def _draw_edges(self, surface: pygame.Surface) -> None:
        # Build set of edges connected to selected node
        selected_edges: set[tuple[int, int]] = set()
        if self._selected is not None:
            for a, b in CONCEPT_EDGES:
                if a == self._selected or b == self._selected:
                    selected_edges.add((a, b))

        for a, b in CONCEPT_EDGES:
            pa = self._positions.get(a)
            pb = self._positions.get(b)
            if pa is None or pb is None:
                continue
            is_active = (a, b) in selected_edges
            color = _LINE_ACTIVE if is_active else _LINE_COLOR
            width = 2 if is_active else 1
            pygame.draw.line(surface, color, pa, pb, width)

    def _draw_nodes(self, surface: pygame.Surface) -> None:
        for rect, node in self._node_by_pos:
            x, y = self._positions[node.lesson_num]
            color = MODULE_COLORS[node.module]
            is_selected = (node.lesson_num == self._selected)
            is_hovered = (node.lesson_num == self._hovered)

            if is_selected:
                fill = color
                # Draw gold ring outside
                pygame.draw.circle(surface, _SELECTED_RING, (x, y), _NODE_R + 4)
                pygame.draw.circle(surface, fill, (x, y), _NODE_R)
                pygame.draw.circle(surface, _SELECTED_RING, (x, y), _NODE_R, 2)
            elif is_hovered:
                fill = _lighten(color)
                pygame.draw.circle(surface, fill, (x, y), _NODE_R)
                pygame.draw.circle(surface, color, (x, y), _NODE_R, 2)
            else:
                fill = _darken(color)
                pygame.draw.circle(surface, fill, (x, y), _NODE_R)
                pygame.draw.circle(surface, color, (x, y), _NODE_R, 1)

            # Draw label
            label = node.name_pl
            lines = label.split("\n")
            line_h = self._font_node.get_height()
            total_h = len(lines) * line_h
            ly = y - total_h // 2
            for line in lines:
                text_color = _TEXT_LIGHT if (is_selected or is_hovered) else color
                rendered = self._font_node.render(line, True, text_color)
                surface.blit(rendered, (x - rendered.get_width() // 2, ly))
                ly += line_h

    def _draw_info_bar(self, surface: pygame.Surface) -> None:
        bar_y = _H - _INFO_H
        pygame.draw.rect(surface, (8, 8, 20), (0, bar_y, _W, _INFO_H))
        pygame.draw.line(surface, (26, 26, 58), (0, bar_y), (_W, bar_y), 1)

        # Determine which node to describe: hovered takes priority, else selected
        active_num = self._hovered if self._hovered is not None else self._selected
        desc = ""
        if active_num is not None and active_num in self._node_map:
            node = self._node_map[active_num]
            lang = self._strings.language if hasattr(self._strings, "language") else "pl"
            desc = node.description_pl if lang == "pl" else node.description_en

        lang = self._strings.language if hasattr(self._strings, "language") else "pl"
        if lang == "pl":
            hint = "ENTER - otworz lekcje  |  ESC - pauza"
        else:
            hint = "ENTER - open lesson  |  ESC - pause"

        if desc:
            rendered = self._font_info.render(desc, True, _TEXT_LIGHT)
            surface.blit(rendered, (16, bar_y + 6))
        rendered_hint = self._font_info.render(hint, True, _TEXT_DIM)
        surface.blit(rendered_hint, (16, bar_y + 6 + self._font_info.get_height() + 4))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next if self._done else None

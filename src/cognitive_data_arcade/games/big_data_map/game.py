from __future__ import annotations

import math
from collections.abc import Callable

import pygame

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.colors import BG as _BG
from cognitive_data_arcade.engine.colors import ORANGE as _ORANGE
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

from .concept_data import (
    CONCEPT_EDGES,
    CONCEPT_NODES,
    DISPLAY_NUM,
    MODULE_COLORS,
    MODULE_NAMES,
    LessonNode,
    get_connected,
)

_W, _H = 1024, 768
_TITLE_H = 40
_INFO_H = 60
_CX = _W // 2
_CY = _TITLE_H + (_H - _TITLE_H - _INFO_H) // 2  # = 374

_R_MODULE = 190  # radius for module name labels
_R_NODE = 270  # radius for lesson nodes
_NODE_R = 22  # node circle radius
_MODULE_ARC = 60  # degrees per module
_ARC_MARGIN = 5  # degrees gap at each end

_ZOOM_MIN = 0.5
_ZOOM_MAX = 2.5
_ZOOM_STEP = 1.12
_LABEL_ZOOM_THRESHOLD = 1.3  # show all name labels at this zoom

_TEXT_LIGHT = (240, 240, 240)
_TEXT_DIM = (100, 100, 140)
_LINE_COLOR = (28, 28, 55)
_LINE_ACTIVE = (70, 70, 120)
_SELECTED_RING = (255, 220, 50)
_CONNECTED_RING = (120, 120, 210)  # ring for nodes connected to selected
_LABEL_GAP = 8  # px between circle edge and nearest label edge

_DOUBLE_CLICK_MS = 500


def _deg2rad(deg: float) -> float:
    return math.radians(deg)


def _polar(cx: int, cy: int, r: float, deg: float) -> tuple[int, int]:
    """Polar coords (degrees, 0=top, clockwise) -> screen xy."""
    rad = _deg2rad(deg - 90)
    return (cx + int(r * math.cos(rad)), cy + int(r * math.sin(rad)))


def _lighten(color: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(min(255, c + 50) for c in color)  # type: ignore[return-value]


def _darken(color: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(max(0, c - 60) for c in color)  # type: ignore[return-value]


def _compute_positions() -> dict[int, tuple[int, int]]:
    """Returns {lesson_num: (x, y)} for all nodes at zoom=1."""
    positions: dict[int, tuple[int, int]] = {}
    by_module: dict[int, list[LessonNode]] = {}
    for node in CONCEPT_NODES:
        by_module.setdefault(node.module, []).append(node)

    for mod_idx, (_mod_num, nodes) in enumerate(sorted(by_module.items())):
        arc_start = mod_idx * _MODULE_ARC
        usable_start = arc_start + _ARC_MARGIN
        usable_end = arc_start + _MODULE_ARC - _ARC_MARGIN
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
        concept_detail_factory: Callable[[int], Scene] | None = None,
    ) -> None:
        self._strings = strings
        self._pm = profile_manager
        self._concept_detail_factory = concept_detail_factory
        self._done = False
        self._next: Scene | None = None
        self._nodes_visited: set[int] = set()
        self._show_summary: bool = False
        self._summary_timer: float = 0.0
        self._session_start_ms: int = pygame.time.get_ticks()

        self._positions = _compute_positions()  # {lesson_num: (x,y)} at zoom=1
        self._zoom: float = 1.0

        self._hovered: int | None = None
        self._selected: int | None = None
        self._connected_nums: set[int] = set()

        # Double-click tracking
        self._last_click_num: int | None = None
        self._last_click_time: int = 0

        self._font_title = get_font(28)
        self._font_num = get_font(12)  # lesson number inside circle
        self._font_node = get_font(13)  # name label outside circle
        self._font_module = get_font(16)
        self._font_info = get_font(20)

        # Kept for test compatibility (hit rects at zoom=1)
        self._node_by_pos: list[tuple[pygame.Rect, LessonNode]] = []
        for node in CONCEPT_NODES:
            x, y = self._positions[node.lesson_num]
            rect = pygame.Rect(x - _NODE_R, y - _NODE_R, _NODE_R * 2, _NODE_R * 2)
            self._node_by_pos.append((rect, node))

        self._node_map: dict[int, LessonNode] = {n.lesson_num: n for n in CONCEPT_NODES}
        self._nav_order = [n.lesson_num for n in CONCEPT_NODES]
        self._nav_idx = 0
        self._selected = self._nav_order[0]
        self._compute_connected()

    # --- helpers ---

    def _compute_connected(self) -> None:
        if self._selected is None:
            self._connected_nums = set()
            return
        self._connected_nums = {n.lesson_num for n, _, _ in get_connected(self._selected)}

    def _spos(self, lesson_num: int) -> tuple[int, int]:
        """Screen position at current zoom (always around canvas centre _CX,_CY)."""
        bx, by = self._positions[lesson_num]
        return (
            int(_CX + (bx - _CX) * self._zoom),
            int(_CY + (by - _CY) * self._zoom),
        )

    def _spos_base(self, bx: int, by: int) -> tuple[int, int]:
        return (
            int(_CX + (bx - _CX) * self._zoom),
            int(_CY + (by - _CY) * self._zoom),
        )

    def _sr(self) -> int:
        return max(10, int(_NODE_R * self._zoom))

    def _hit_node(self, screen_pos: tuple[int, int]) -> int | None:
        sr = self._sr()
        px, py = screen_pos
        for node in CONCEPT_NODES:
            sx, sy = self._spos(node.lesson_num)
            if (px - sx) ** 2 + (py - sy) ** 2 <= sr * sr:
                return node.lesson_num
        return None

    def _navigate_to(self, lesson_num: int) -> None:
        if self._concept_detail_factory is not None:
            audio.play_sfx("navigate")
            self._next = self._concept_detail_factory(lesson_num)
            self._done = True

    # --- events ---

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._show_summary:
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                self._summary_timer = 10_001
            return

        if event.type == pygame.MOUSEWHEEL:
            factor = _ZOOM_STEP if event.y > 0 else 1.0 / _ZOOM_STEP
            self._zoom = max(_ZOOM_MIN, min(_ZOOM_MAX, self._zoom * factor))
            return

        if event.type == pygame.MOUSEMOTION:
            self._hovered = self._hit_node(event.pos)
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                hit = self._hit_node(event.pos)
                if hit is not None:
                    now = pygame.time.get_ticks()
                    if (
                        hit == self._last_click_num
                        and now - self._last_click_time <= _DOUBLE_CLICK_MS
                    ):
                        self._navigate_to(hit)
                    else:
                        self._selected = hit
                        self._nodes_visited.add(hit)
                        if hit in self._nav_order:
                            self._nav_idx = self._nav_order.index(hit)
                        self._compute_connected()
                        audio.play_sfx("navigate")
                    self._last_click_num = hit
                    self._last_click_time = now
            return

        if event.type != pygame.KEYDOWN:
            return

        key = event.key
        n = len(self._nav_order)
        if key in (pygame.K_UP, pygame.K_RIGHT):
            self._nav_idx = (self._nav_idx - 1) % n
            self._selected = self._nav_order[self._nav_idx]
            self._nodes_visited.add(self._selected)
            self._compute_connected()
            audio.play_sfx("navigate")
        elif key in (pygame.K_DOWN, pygame.K_LEFT):
            self._nav_idx = (self._nav_idx + 1) % n
            self._selected = self._nav_order[self._nav_idx]
            self._nodes_visited.add(self._selected)
            self._compute_connected()
            audio.play_sfx("navigate")
        elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            if self._selected is not None:
                self._navigate_to(self._selected)
        elif key == pygame.K_q:
            if self._concept_detail_factory is None:
                self._show_summary = True
                self._summary_timer = 0.0
        elif key == pygame.K_r:
            self._zoom = 1.0  # reset zoom to default

    # --- drawing ---

    def update(self, dt: float) -> None:
        if self._show_summary:
            self._summary_timer += dt
            if self._summary_timer >= 10_000:
                self._done = True
            return

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_title(surface)
        self._draw_module_labels(surface)
        self._draw_edges(surface)
        self._draw_node_circles(surface)  # pass 1: circles + numbers
        self._draw_node_labels(surface)  # pass 2: name labels always on top
        self._draw_info_bar(surface)
        if self._show_summary:
            self._draw_summary(surface)

    def _draw_title(self, surface: pygame.Surface) -> None:
        rendered = self._font_title.render("Siec Pojec - Cognitive Data Arcade", True, _ORANGE)
        surface.blit(rendered, (16, (_TITLE_H - rendered.get_height()) // 2))

    def _draw_module_labels(self, surface: pygame.Surface) -> None:
        by_module: dict[int, list[LessonNode]] = {}
        for node in CONCEPT_NODES:
            by_module.setdefault(node.module, []).append(node)

        lang = self._strings.language if hasattr(self._strings, "language") else "pl"
        for mod_idx, (mod_num, _nodes) in enumerate(sorted(by_module.items())):
            arc_mid = mod_idx * _MODULE_ARC + _MODULE_ARC / 2
            bx, by = _polar(_CX, _CY, _R_MODULE, arc_mid)
            mx, my = self._spos_base(bx, by)
            color = MODULE_COLORS[mod_num]
            name = MODULE_NAMES[mod_num][0 if lang == "pl" else 1]
            words = name.split()
            lines = [" ".join(words[:2]), " ".join(words[2:])] if len(words) > 2 else [name]
            line_h = self._font_module.get_height()
            y0 = my - (len(lines) * line_h) // 2
            for line in lines:
                surf = self._font_module.render(line, True, color)
                surface.blit(surf, (mx - surf.get_width() // 2, y0))
                y0 += line_h

    def _draw_edges(self, surface: pygame.Surface) -> None:
        selected_edges: set[tuple[int, int]] = set()
        if self._selected is not None:
            for a, b in CONCEPT_EDGES:
                if a == self._selected or b == self._selected:
                    selected_edges.add((a, b))

        for a, b in CONCEPT_EDGES:
            if a not in self._positions or b not in self._positions:
                continue
            is_active = (a, b) in selected_edges
            pygame.draw.line(
                surface,
                _LINE_ACTIVE if is_active else _LINE_COLOR,
                self._spos(a),
                self._spos(b),
                2 if is_active else 1,
            )

    def _draw_node_circles(self, surface: pygame.Surface) -> None:
        """Pass 1: all circles and lesson numbers, no labels."""
        sr = self._sr()
        for _rect, node in self._node_by_pos:
            sx, sy = self._spos(node.lesson_num)
            color = MODULE_COLORS[node.module]
            is_selected = node.lesson_num == self._selected
            is_hovered = node.lesson_num == self._hovered
            is_connected = node.lesson_num in self._connected_nums

            if is_selected:
                pygame.draw.circle(surface, _SELECTED_RING, (sx, sy), sr + 4)
                pygame.draw.circle(surface, color, (sx, sy), sr)
                pygame.draw.circle(surface, _SELECTED_RING, (sx, sy), sr, 2)
            elif is_hovered:
                pygame.draw.circle(surface, _lighten(color), (sx, sy), sr)
                pygame.draw.circle(surface, color, (sx, sy), sr, 2)
            elif is_connected:
                pygame.draw.circle(surface, _darken(color), (sx, sy), sr)
                pygame.draw.circle(surface, _CONNECTED_RING, (sx, sy), sr, 2)
            else:
                pygame.draw.circle(surface, _darken(color), (sx, sy), sr)
                pygame.draw.circle(surface, color, (sx, sy), sr, 1)

            display = DISPLAY_NUM.get(node.lesson_num, node.lesson_num)
            num_surf = self._font_num.render(str(display), True, _TEXT_LIGHT)
            surface.blit(
                num_surf,
                (sx - num_surf.get_width() // 2, sy - num_surf.get_height() // 2),
            )

    def _draw_node_labels(self, surface: pygame.Surface) -> None:
        """Pass 2: name labels rendered after all circles so nothing covers them."""
        sr = self._sr()
        show_all = self._zoom >= _LABEL_ZOOM_THRESHOLD
        lang = self._strings.language if hasattr(self._strings, "language") else "pl"

        for _rect, node in self._node_by_pos:
            is_selected = node.lesson_num == self._selected
            is_hovered = node.lesson_num == self._hovered
            is_connected = node.lesson_num in self._connected_nums
            if not (is_selected or is_hovered or is_connected or show_all):
                continue

            sx, sy = self._spos(node.lesson_num)
            # Outward unit vector from canvas centre
            dx, dy = sx - _CX, sy - _CY
            dist = math.hypot(dx, dy)
            ux, uy = (dx / dist, dy / dist) if dist > 0 else (0.0, 1.0)

            # Anchor point: just outside the circle edge
            ax = sx + ux * (sr + _LABEL_GAP)
            ay = sy + uy * (sr + _LABEL_GAP)

            name = node.name_pl if lang == "pl" else node.name_en
            lines = name.split("\n")
            line_h = self._font_node.get_height()
            total_h = len(lines) * line_h
            text_color = _TEXT_LIGHT if (is_selected or is_hovered) else _TEXT_DIM

            # Vertical start: anchor is top / bottom / middle of text block
            if uy > 0.3:  # lower half → anchor = top of block
                ry = int(ay)
            elif uy < -0.3:  # upper half → anchor = bottom of block
                ry = int(ay) - total_h
            else:  # sides → vertically centred on anchor
                ry = int(ay) - total_h // 2

            for line in lines:
                surf = self._font_node.render(line, True, text_color)
                # Horizontal alignment relative to anchor
                if ux > 0.3:  # right half → left-align from anchor
                    rx = int(ax)
                elif ux < -0.3:  # left half → right-align to anchor
                    rx = int(ax) - surf.get_width()
                else:  # top / bottom → horizontally centred
                    rx = int(ax) - surf.get_width() // 2
                surface.blit(surf, (rx, ry))
                ry += line_h

    def _draw_info_bar(self, surface: pygame.Surface) -> None:
        bar_y = _H - _INFO_H
        pygame.draw.rect(surface, (8, 8, 20), (0, bar_y, _W, _INFO_H))
        pygame.draw.line(surface, (26, 26, 58), (0, bar_y), (_W, bar_y), 1)

        active_num = self._hovered if self._hovered is not None else self._selected
        lang = self._strings.language if hasattr(self._strings, "language") else "pl"
        desc = ""
        if active_num is not None and active_num in self._node_map:
            node = self._node_map[active_num]
            name = (node.name_pl if lang == "pl" else node.name_en).replace("\n", " ")
            body = node.description_pl if lang == "pl" else node.description_en
            desc = f"{name} — {body}"

        if lang == "pl":
            hint = "ENTER / 2x klik - szczegoly  |  kolko myszy - zoom  |  R - reset widoku  |  ESC - pauza"
        else:
            hint = "ENTER / double-click - details  |  scroll - zoom  |  R - reset view  |  ESC - pause"

        if desc:
            surface.blit(self._font_info.render(desc, True, _TEXT_LIGHT), (16, bar_y + 6))
        surface.blit(
            self._font_info.render(hint, True, _TEXT_DIM),
            (16, bar_y + 6 + self._font_info.get_height() + 4),
        )

    def _draw_summary(self, surface: pygame.Surface) -> None:
        w, h = surface.get_width(), surface.get_height()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        panel_w, panel_h = 560, 280
        px = (w - panel_w) // 2
        py = (h - panel_h) // 2
        pygame.draw.rect(surface, (14, 14, 36), (px, py, panel_w, panel_h), border_radius=10)
        pygame.draw.rect(surface, (70, 70, 130), (px, py, panel_w, panel_h), 2, border_radius=10)

        elapsed_s = (pygame.time.get_ticks() - self._session_start_ms) // 1000
        mins, secs = divmod(elapsed_s, 60)
        visited = len(self._nodes_visited)

        font_h = get_font(24)
        font_b = get_font(20)
        font_hint = get_font(14)
        lines = [
            ("Podsumowanie sesji", font_h, (200, 200, 240)),
            (f"Czas sesji: {mins}m {secs}s", font_b, (160, 160, 200)),
            (f"Wezlow odwiedzonych: {visited} / 31", font_b, (160, 160, 200)),
            ("", font_b, (0, 0, 0)),
            ("Nacisnij dowolny klawisz lub kliknij", font_hint, (90, 90, 120)),
        ]
        y = py + 20
        for text, font, color in lines:
            if not text:
                y += 10
                continue
            s = font.render(text, True, color)
            surface.blit(s, (px + panel_w // 2 - s.get_width() // 2, y))
            y += font.get_height() + 8

    def _build_next_scene(self) -> Scene:
        from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        visited = len(self._nodes_visited)
        ap = min(100, visited * 2)
        session = SessionResult(
            task_name="big_data_map",
            participant_id=self._pm.load().device_uuid,
            session_id="map_exploration",
            total_trials=31,
            correct_trials=min(visited, 31),
            avg_reaction_time_ms=0.0,
            min_reaction_time_ms=0.0,
            max_reaction_time_ms=0.0,
            arcade_points_earned=ap,
            science_points_earned=0,
        )
        profile_before = self._pm.load()
        badge_engine = BadgeEngine()
        new_badge_ids = badge_engine.evaluate(session, profile_before)
        self._pm.add_ap(session.arcade_points_earned)
        for bid in new_badge_ids:
            self._pm.award_badge(bid)
        profile_after = self._pm.load()
        return SessionSummaryScene(
            session=session,
            new_badge_ids=new_badge_ids,
            profile_before=profile_before,
            profile_after=profile_after,
            strings=self._strings,
            profile_manager=self._pm,
        )

    def is_done(self) -> bool:
        return self._done or (self._show_summary and self._summary_timer >= 10_000)

    def next_scene(self) -> Scene | None:
        done = self.is_done()
        if done and self._next is None and self._concept_detail_factory is None:
            self._next = self._build_next_scene()
        return self._next if done else None

from __future__ import annotations

import copy
import math

import pygame
from cognitive_data_arcade.engine.fonts import get_font

from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.social_network.graph import (
    Graph,
    Node,
    generate_random,
    generate_scale_free,
    hub_node_index,
    periphery_node_index,
    sir_step,
)

_W, _H = 1024, 720
_TOP_H = 50
_BOT_H = 150
_MID_X = 512
_NET_H = _H - _TOP_H - _BOT_H   # 520
_MAX_NODES = 30
_NODE_RADIUS = 10
_HUB_RADIUS = 14
_P_INFECT = 0.4
_P_RECOVER = 0.25
_SIR_TICK_MS = 300.0
_RNG_P = 0.3

_BG       = (13, 17, 23)
_PANEL_BG = (13, 17, 23)
_DIVIDER  = (44, 62, 80)
_TOP_BG   = (26, 26, 46)
_BOT_BG   = (17, 24, 39)

_S_COLOR    = (120, 120, 140)
_I_COLOR    = (231, 76, 60)
_R_COLOR    = (39, 174, 96)
_EDGE_COLOR = (44, 62, 80)
_BTN_ACTIVE = (44, 62, 80)
_BTN_INACT  = (26, 26, 46)
_BTN_TEXT   = (200, 200, 200)
_AMBER      = (230, 126, 34)
_BLUE       = (52, 152, 219)
_GREEN_BTN  = (39, 174, 96)
_GREY_TEXT  = (100, 100, 100)

_BOT_Y = _TOP_H + _NET_H   # 570


def _node_color(state: str) -> tuple[int, int, int]:
    if state == "I":
        return _I_COLOR
    if state == "R":
        return _R_COLOR
    return _S_COLOR


class SocialNetworkScene(Scene):
    def __init__(self) -> None:
        self._left: Graph = Graph()
        self._right: Graph | None = None
        self._right_type: str = ""
        self._mode: str = "add_node"
        self._state: str = "build"
        self._selected_node: int | None = None
        self._auto_play: bool = False
        self._sir_timer: float = 0.0
        self._step_count: int = 0
        self._max_i_left: float = 0.0
        self._max_i_right: float = 0.0
        self._p_infect: float = _P_INFECT
        self._done: bool = False
        self._next: Scene | None = None

        pygame.font.init()
        self._font_sm = get_font(22)
        self._font_md = get_font(28)
        self._font_lg = get_font(36)

        _by = _BOT_Y + 15
        self._btn_add_node    = pygame.Rect(10,  10, 90, 30)
        self._btn_add_edge    = pygame.Rect(110, 10, 90, 30)
        self._btn_random      = pygame.Rect(270, 10, 80, 30)
        self._btn_scale_free  = pygame.Rect(360, 10, 100, 30)
        self._btn_clear       = pygame.Rect(530, 10, 80, 30)
        self._btn_hub         = pygame.Rect(10,  _by, 120, 36)
        self._btn_periphery   = pygame.Rect(140, _by, 150, 36)
        self._btn_step        = pygame.Rect(310, _by, 80,  36)
        self._btn_auto        = pygame.Rect(400, _by, 80,  36)
        self._btn_reset_spread= pygame.Rect(490, _by, 120, 36)
        self._slider_rect     = pygame.Rect(650, _by, 200, 30)

    # ------------------------------------------------------------------
    # Scene protocol

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    # ------------------------------------------------------------------
    # Event handling

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._on_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            self._on_key(event.key)

    def _on_click(self, pos: tuple[int, int]) -> None:
        mx, my = pos

        # Always-active top bar buttons
        if self._btn_clear.collidepoint(mx, my):
            self._clear()
            return

        if self._state == "build":
            if self._btn_add_node.collidepoint(mx, my):
                self._mode = "add_node"
                self._selected_node = None
                return
            if self._btn_add_edge.collidepoint(mx, my):
                self._mode = "add_edge"
                self._selected_node = None
                return
            if self._btn_random.collidepoint(mx, my) and self._left.nodes:
                n = len(self._left.nodes)
                self._right = generate_random(n, _RNG_P, _MID_X, _W - _MID_X)
                self._right_type = "RANDOM"
                return
            if self._btn_scale_free.collidepoint(mx, my) and self._left.nodes:
                n = len(self._left.nodes)
                self._right = generate_scale_free(n, 2, _MID_X, _W - _MID_X)
                self._right_type = "SCALE-FREE"
                return

        # Bottom bar spread buttons
        if self._btn_hub.collidepoint(mx, my) and self._state == "build":
            self._start_spread(from_hub=True)
            return
        if self._btn_periphery.collidepoint(mx, my) and self._state == "build":
            self._start_spread(from_hub=False)
            return
        if self._btn_step.collidepoint(mx, my) and self._state == "spread":
            self._do_sir_step()
            return
        if self._btn_auto.collidepoint(mx, my) and self._state == "spread":
            self._auto_play = not self._auto_play
            return
        if self._btn_reset_spread.collidepoint(mx, my) and self._state == "spread":
            self._reset_spread()
            return

        # Slider
        if self._slider_rect.collidepoint(mx, my):
            frac = (mx - self._slider_rect.x) / self._slider_rect.width
            step = round(frac * 8)
            self._p_infect = max(0.1, min(0.9, (step + 1) * 0.1))
            return

        # Left panel — build mode only
        if self._state == "build" and 0 <= mx < _MID_X and _TOP_H <= my < _TOP_H + _NET_H:
            if self._mode == "add_node":
                self._add_node(float(mx), float(my))
            elif self._mode == "add_edge":
                self._click_edge(mx, my)

    def _on_key(self, key: int) -> None:
        if key == pygame.K_LEFT:
            self._p_infect = max(0.1, round(self._p_infect - 0.1, 1))
        elif key == pygame.K_RIGHT:
            self._p_infect = min(0.9, round(self._p_infect + 0.1, 1))

    # ------------------------------------------------------------------
    # Build-mode helpers

    def _add_node(self, x: float, y: float) -> None:
        if len(self._left.nodes) >= _MAX_NODES:
            return
        self._left.nodes.append(Node(x=x, y=y))

    def _click_edge(self, mx: int, my: int) -> None:
        hit = self._nearest_node(self._left, mx, my)
        if hit is None:
            return
        if self._selected_node is None:
            self._selected_node = hit
        else:
            a, b = self._selected_node, hit
            self._selected_node = None
            if a == b:
                return
            if a > b:
                a, b = b, a
            if (a, b) not in self._left.edges:
                self._left.edges.append((a, b))
                self._left.nodes[a].degree += 1
                self._left.nodes[b].degree += 1

    def _nearest_node(self, graph: Graph, mx: int, my: int) -> int | None:
        for i, nd in enumerate(graph.nodes):
            if math.hypot(nd.x - mx, nd.y - my) <= _NODE_RADIUS + 4:
                return i
        return None

    def _clear(self) -> None:
        self._left = Graph()
        self._right = None
        self._right_type = ""
        self._mode = "add_node"
        self._state = "build"
        self._selected_node = None
        self._auto_play = False
        self._sir_timer = 0.0
        self._step_count = 0
        self._max_i_left = 0.0
        self._max_i_right = 0.0

    # ------------------------------------------------------------------
    # Spread helpers

    def _start_spread(self, from_hub: bool) -> None:
        if not self._left.nodes:
            return
        # Reset left network nodes to S, set patient zero
        self._left = copy.deepcopy(self._left)
        for nd in self._left.nodes:
            nd.state = "S"
        idx_l = hub_node_index(self._left) if from_hub else periphery_node_index(self._left)
        self._left.nodes[idx_l].state = "I"
        # Reset right network nodes to S, set patient zero
        if self._right is not None:
            self._right = copy.deepcopy(self._right)
            for nd in self._right.nodes:
                nd.state = "S"
            idx_r = hub_node_index(self._right) if from_hub else periphery_node_index(self._right)
            self._right.nodes[idx_r].state = "I"
        self._step_count = 0
        self._max_i_left = 0.0
        self._max_i_right = 0.0
        self._auto_play = False
        self._sir_timer = 0.0
        self._state = "spread"

    def _do_sir_step(self) -> None:
        self._left = sir_step(self._left, self._p_infect, _P_RECOVER)
        self._step_count += 1
        n_left = len(self._left.nodes) or 1
        i_frac_left = sum(1 for nd in self._left.nodes if nd.state == "I") / n_left * 100
        if i_frac_left > self._max_i_left:
            self._max_i_left = i_frac_left
        if self._right is not None:
            self._right = sir_step(self._right, self._p_infect, _P_RECOVER)
            n_right = len(self._right.nodes) or 1
            i_frac_right = sum(1 for nd in self._right.nodes if nd.state == "I") / n_right * 100
            if i_frac_right > self._max_i_right:
                self._max_i_right = i_frac_right

    def _reset_spread(self) -> None:
        for nd in self._left.nodes:
            nd.state = "S"
        if self._right is not None:
            for nd in self._right.nodes:
                nd.state = "S"
        self._step_count = 0
        self._max_i_left = 0.0
        self._max_i_right = 0.0
        self._auto_play = False
        self._sir_timer = 0.0
        self._state = "build"

    # ------------------------------------------------------------------
    # Update

    def update(self, dt_ms: float = 0.0) -> None:
        if self._state == "spread" and self._auto_play:
            self._sir_timer += dt_ms
            if self._sir_timer >= _SIR_TICK_MS:
                self._sir_timer -= _SIR_TICK_MS
                self._do_sir_step()

    # ------------------------------------------------------------------
    # Drawing

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_top_bar(surface)
        self._draw_left_panel(surface)
        self._draw_right_panel(surface)
        pygame.draw.line(surface, _DIVIDER, (_MID_X, _TOP_H), (_MID_X, _TOP_H + _NET_H), 2)
        self._draw_bottom_bar(surface)

    def _draw_button(self, surface: pygame.Surface, rect: pygame.Rect,
                     label: str, active: bool,
                     color: tuple[int, int, int] = _BTN_TEXT) -> None:
        bg = _BTN_ACTIVE if active else _BTN_INACT
        pygame.draw.rect(surface, bg, rect, border_radius=3)
        border = color if active else _GREY_TEXT
        pygame.draw.rect(surface, border, rect, 1, border_radius=3)
        txt = self._font_sm.render(label, True, color if active else _GREY_TEXT)
        surface.blit(txt, txt.get_rect(center=rect.center))

    def _draw_top_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _TOP_BG, (0, 0, _W, _TOP_H))
        in_build = self._state == "build"
        self._draw_button(surface, self._btn_add_node,   "+ Wezel",
                          in_build and self._mode == "add_node", _BLUE)
        self._draw_button(surface, self._btn_add_edge,   "- Krawedz",
                          in_build and self._mode == "add_edge", _BLUE)
        self._draw_button(surface, self._btn_random,     "Random",
                          in_build and bool(self._left.nodes), _AMBER)
        self._draw_button(surface, self._btn_scale_free, "Scale-free",
                          in_build and bool(self._left.nodes), _AMBER)
        self._draw_button(surface, self._btn_clear,      "Wyczysc",
                          True, (192, 57, 43))

    def _draw_network(self, surface: pygame.Surface, graph: Graph,
                      is_left: bool = True) -> None:
        hub_idx = hub_node_index(graph) if graph.nodes else -1
        for a, b in graph.edges:
            na, nb = graph.nodes[a], graph.nodes[b]
            pygame.draw.line(surface, _EDGE_COLOR,
                             (int(na.x), int(na.y)), (int(nb.x), int(nb.y)), 1)
        for i, nd in enumerate(graph.nodes):
            r = _HUB_RADIUS if i == hub_idx else _NODE_RADIUS
            color = _node_color(nd.state)
            pygame.draw.circle(surface, color, (int(nd.x), int(nd.y)), r)
            if is_left and self._selected_node == i:
                pygame.draw.circle(surface, _BLUE, (int(nd.x), int(nd.y)), r + 3, 2)

    def _draw_left_panel(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _PANEL_BG, (0, _TOP_H, _MID_X, _NET_H))
        header = self._font_sm.render(
            f"TWOJA SIEC   wezly: {len(self._left.nodes)}/{_MAX_NODES}   "
            f"krawedzie: {len(self._left.edges)}", True, _BLUE)
        surface.blit(header, (8, _TOP_H + 6))
        self._draw_network(surface, self._left, is_left=True)

    def _draw_right_panel(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _PANEL_BG, (_MID_X, _TOP_H, _MID_X, _NET_H))
        if self._right is None:
            hint = self._font_sm.render(
                "Kliknij Random lub Scale-free zeby wygenerowac siec",
                True, _GREY_TEXT)
            surface.blit(hint, hint.get_rect(
                center=(_MID_X + _MID_X // 2, _TOP_H + _NET_H // 2)))
        else:
            label = self._font_md.render(f"SIEC {self._right_type}", True, _AMBER)
            surface.blit(label, (_MID_X + 8, _TOP_H + 6))
            self._draw_network(surface, self._right, is_left=False)

    def _draw_bottom_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _BOT_BG, (0, _BOT_Y, _W, _BOT_H))
        in_build = self._state == "build"
        in_spread = self._state == "spread"
        self._draw_button(surface, self._btn_hub,       "Od huba",
                          in_build, _I_COLOR)
        self._draw_button(surface, self._btn_periphery, "Od peryferium",
                          in_build, _S_COLOR)
        self._draw_button(surface, self._btn_step,      "Krok",
                          in_spread, _GREEN_BTN)
        auto_label = "Auto [ON]" if self._auto_play else "Auto"
        self._draw_button(surface, self._btn_auto,      auto_label,
                          in_spread, _GREEN_BTN)
        self._draw_button(surface, self._btn_reset_spread, "Reset spreadu",
                          in_spread, _AMBER)

        # p_infect slider
        lbl = self._font_sm.render(f"p_infect: {self._p_infect:.1f}", True, _BTN_TEXT)
        surface.blit(lbl, (self._slider_rect.x, self._slider_rect.y - 16))
        pygame.draw.rect(surface, _BTN_ACTIVE, self._slider_rect, border_radius=3)
        fill_w = int(self._slider_rect.width * (self._p_infect - 0.1) / 0.8)
        fill_rect = pygame.Rect(self._slider_rect.x, self._slider_rect.y,
                                fill_w, self._slider_rect.height)
        pygame.draw.rect(surface, _AMBER, fill_rect, border_radius=3)

        # Metrics row
        my = _BOT_Y + 70
        n_left = len(self._left.nodes) or 1
        r_left = sum(1 for nd in self._left.nodes if nd.state == "R") / n_left * 100
        metrics_l = (f"krok: {self._step_count}   "
                     f"max I: {self._max_i_left:.0f}%   "
                     f"R: {r_left:.0f}%")
        surface.blit(self._font_sm.render(metrics_l, True, _BTN_TEXT), (10, my))

        if self._right is not None:
            n_right = len(self._right.nodes) or 1
            r_right = sum(1 for nd in self._right.nodes if nd.state == "R") / n_right * 100
            metrics_r = (f"krok: {self._step_count}   "
                         f"max I: {self._max_i_right:.0f}%   "
                         f"R: {r_right:.0f}%")
            surface.blit(self._font_sm.render(metrics_r, True, _BTN_TEXT),
                         (_MID_X + 10, my))

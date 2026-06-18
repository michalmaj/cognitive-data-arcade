from __future__ import annotations

import math

import pygame

from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.social_network.graph import (
    Graph,
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
_RED_BTN    = (192, 57, 43)
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
        self._font_sm = pygame.font.SysFont(None, 22)
        self._font_md = pygame.font.SysFont(None, 28)
        self._font_lg = pygame.font.SysFont(None, 36)

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

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def handle_event(self, event: pygame.event.Event) -> None:
        pass  # implemented in Tasks 3 & 4

    def update(self, dt_ms: float = 0.0) -> None:
        pass  # implemented in Task 4

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_top_bar(surface)
        self._draw_left_panel(surface)
        self._draw_right_panel(surface)
        pygame.draw.line(surface, _DIVIDER, (_MID_X, _TOP_H), (_MID_X, _TOP_H + _NET_H), 2)
        self._draw_bottom_bar(surface)

    def _draw_top_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _TOP_BG, (0, 0, _W, _TOP_H))

    def _draw_left_panel(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _PANEL_BG, (0, _TOP_H, _MID_X, _NET_H))

    def _draw_right_panel(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _PANEL_BG, (_MID_X, _TOP_H, _MID_X, _NET_H))

    def _draw_bottom_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _BOT_BG, (0, _BOT_Y, _W, _BOT_H))

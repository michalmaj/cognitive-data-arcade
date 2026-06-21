# src/cognitive_data_arcade/games/misinformation/phase_act.py
from __future__ import annotations

import math

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.misinformation.networks import NetworkConfig, build_graph
from cognitive_data_arcade.games.social_network.graph import hub_node_index, sir_step

_W, _H = 1024, 768
_TOP_H = 60
_BOT_H = 60
_ACT_SECS = 60.0
_SIR_MS = 1500.0
_WIN_SPREAD = 0.60
_WIN_CONTAIN = 0.20
_EARLY_BONUS = 10
_NODE_R = 12
_HUB_R = 17

_S_COLOR = (120, 120, 140)
_I_COLOR = (231, 76, 60)
_R_COLOR = (39, 174, 96)

_SPREADER_BG = (26, 10, 10)
_SPREADER_TOP = (40, 10, 10)
_SPREADER_ACCENT = (231, 76, 60)
_SPREADER_EDGE = (60, 30, 30)
_CHECKER_BG = (10, 17, 26)
_CHECKER_TOP = (10, 20, 40)
_CHECKER_ACCENT = (52, 152, 219)
_CHECKER_EDGE = (25, 45, 65)


class PhaseActScene(Scene):
    def __init__(
        self,
        cfg: NetworkConfig,
        round_idx: int,  # 0-based index into ROUNDS
        act: str,  # "spreader" | "factchecker"
        session_scores: list[int],
    ) -> None:
        self._cfg = cfg
        self._round_idx = round_idx
        self._act = act
        self._session_scores = list(session_scores)

        self._graph = build_graph(cfg)
        if act == "spreader":
            self._graph.nodes[0].state = "I"
        else:
            hub = hub_node_index(self._graph)
            self._graph.nodes[hub].state = "I"

        self._hub_idx = hub_node_index(self._graph)
        self._timer_ms = 0.0
        self._sir_timer = 0.0
        self._early_win = False
        self._done = False
        self._next: Scene | None = None

    # ------------------------------------------------------------------
    # Helpers

    def _infected_frac(self) -> float:
        total = len(self._graph.nodes)
        if total == 0:
            return 0.0
        return sum(1 for n in self._graph.nodes if n.state == "I") / total

    def _check_win(self) -> bool:
        frac = self._infected_frac()
        if self._act == "spreader" and frac >= _WIN_SPREAD:
            return True
        if self._act == "factchecker" and frac <= _WIN_CONTAIN:
            return True
        return False

    def _calc_score(self) -> int:
        frac = self._infected_frac()
        base = int(frac * 100) if self._act == "spreader" else int((1.0 - frac) * 100)
        return base + (_EARLY_BONUS if self._early_win else 0)

    def _end_act(self) -> None:
        score = self._calc_score()
        updated = self._session_scores + [score]
        from cognitive_data_arcade.games.misinformation.phase_interlude import PhaseInterludeScene

        self._next = PhaseInterludeScene(
            round_idx=self._round_idx,
            act=self._act,
            act_score=score,
            session_scores=updated,
        )
        self._done = True

    # ------------------------------------------------------------------
    # Scene interface

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._done:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for node in self._graph.nodes:
                if math.hypot(node.x - mx, node.y - my) <= _NODE_R + 4:
                    if self._act == "spreader" and node.state == "S":
                        node.state = "I"
                        break
                    if self._act == "factchecker" and node.state == "I":
                        node.state = "R"
                        break

    def update(self, dt_ms: float = 0.0) -> None:
        if self._done:
            return
        self._timer_ms += dt_ms
        self._sir_timer += dt_ms
        if self._sir_timer >= _SIR_MS:
            self._sir_timer -= _SIR_MS
            self._graph = sir_step(self._graph, p_infect=0.4, p_recover=0.15)

        if self._check_win():
            self._early_win = True
            self._end_act()
            return
        if self._timer_ms >= _ACT_SECS * 1000:
            self._end_act()

    def draw(self, surface: pygame.Surface) -> None:
        spreader = self._act == "spreader"
        bg = _SPREADER_BG if spreader else _CHECKER_BG
        top_c = _SPREADER_TOP if spreader else _CHECKER_TOP
        accent = _SPREADER_ACCENT if spreader else _CHECKER_ACCENT
        edge_c = _SPREADER_EDGE if spreader else _CHECKER_EDGE

        surface.fill(bg)

        # Top bar
        pygame.draw.rect(surface, top_c, (0, 0, _W, _TOP_H))
        role_label = "SPREADER" if spreader else "FACT-CHECKER"
        role_surf = get_font(20).render(role_label, True, accent)
        surface.blit(role_surf, (16, (_TOP_H - role_surf.get_height()) // 2))

        runda_text = f"Runda {self._round_idx + 1}/3  |  {self._cfg.label}"
        runda_surf = get_font(15).render(runda_text, True, (180, 180, 180))
        surface.blit(
            runda_surf,
            (
                _W // 2 - runda_surf.get_width() // 2,
                (_TOP_H - runda_surf.get_height()) // 2,
            ),
        )

        secs_left = max(0.0, _ACT_SECS - self._timer_ms / 1000)
        timer_surf = get_font(22).render(f"{secs_left:.0f}s", True, accent)
        surface.blit(
            timer_surf, (_W - timer_surf.get_width() - 16, (_TOP_H - timer_surf.get_height()) // 2)
        )

        # Edges
        for a, b in self._graph.edges:
            na = self._graph.nodes[a]
            nb = self._graph.nodes[b]
            pygame.draw.line(surface, edge_c, (int(na.x), int(na.y)), (int(nb.x), int(nb.y)), 1)

        # Nodes
        for i, node in enumerate(self._graph.nodes):
            color = {"S": _S_COLOR, "I": _I_COLOR, "R": _R_COLOR}[node.state]
            r = _HUB_R if i == self._hub_idx else _NODE_R
            pygame.draw.circle(surface, color, (int(node.x), int(node.y)), r)

        # Bottom bar: progress bar
        bot_y = _H - _BOT_H
        pygame.draw.rect(surface, top_c, (0, bot_y, _W, _BOT_H))
        bar_w = 600
        bar_x = (_W - bar_w) // 2
        bar_y = bot_y + 10
        bar_h = 16
        pygame.draw.rect(surface, (40, 30, 30), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        frac = self._infected_frac()
        fill = int(frac * bar_w)
        if fill > 0:
            pygame.draw.rect(surface, _I_COLOR, (bar_x, bar_y, fill, bar_h), border_radius=4)
        pct_text = f"{frac * 100:.0f}% zarazone"
        pct_surf = get_font(13).render(pct_text, True, _I_COLOR)
        surface.blit(pct_surf, (_W // 2 - pct_surf.get_width() // 2, bar_y + bar_h + 4))

        # Hint line
        if spreader:
            hint = "Klikaj szare wezly -- dezinformacja rozchodzi sie sama!"
        else:
            hint = "Klikaj czerwone wezly -- ale SIR sie nie zatrzymuje!"
        hint_surf = get_font(13).render(hint, True, (160, 140, 140))
        surface.blit(hint_surf, (_W // 2 - hint_surf.get_width() // 2, bot_y + 34))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

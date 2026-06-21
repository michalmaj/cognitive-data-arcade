from __future__ import annotations

import random

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.semantic_space.missions import Mission
from cognitive_data_arcade.games.semantic_space.word_data import CLUSTERS, SIMILARITIES, WORDS

_W, _H = 1024, 720
_TOP_H = 44
_LEFT_W = 320
_MAP_X = _LEFT_W + 8
_MAP_Y = _TOP_H + 6
_MAP_W = _W - _MAP_X - 8
_MAP_H = _H - _MAP_Y - 8
_NODE_R = 18
from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
    GREEN as _GREEN,
)

_TOP_BG = (10, 10, 28)
_LEFT_BG = (12, 12, 32)
_AMBER = (240, 165, 0)
_GREY = (60, 60, 80)

_TYPE_COLORS = {
    "neighbors": (52, 152, 219),
    "odd_one_out": (231, 76, 60),
    "bridge": (46, 204, 113),
    "analogy": (155, 89, 182),
}
_TYPE_LABELS = {
    "neighbors": "ZNAJDZ SASIADOW",
    "odd_one_out": "INTRUZ W KLASTRZE",
    "bridge": "MOST SEMANTYCZNY",
    "analogy": "ANALOGIA WEKTOROWA",
}


class PhaseMissionScene(Scene):
    def __init__(
        self,
        missions: list[Mission],
        round_idx: int,
        session_score: int,
        round_results: list[dict],
    ) -> None:
        self._missions = missions
        self._mission = missions[round_idx]
        self._round_idx = round_idx
        self._session_score = session_score
        self._round_results = round_results
        self._selected: set[str] = set()
        self._hover: str | None = None
        self._done = False
        self._next: Scene | None = None

        self._node_pos: dict[str, tuple[int, int]] = {
            key: (
                int(_MAP_X + wd["x"] * _MAP_W),
                int(_MAP_Y + wd["y"] * _MAP_H),
            )
            for key, wd in WORDS.items()
        }

        if self._mission.type == "analogy":
            opts = self._mission.answers + self._mission.distractors
            random.shuffle(opts)
            self._analogy_opts = opts
        else:
            self._analogy_opts = []

    # ── events ─────────────────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._done:
            return
        if event.type == pygame.MOUSEMOTION:
            self._hover = self._node_at(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_click(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self._can_submit():
                self._submit()

    def _node_at(self, pos: tuple[int, int]) -> str | None:
        mx, my = pos
        for key, (nx, ny) in self._node_pos.items():
            if (mx - nx) ** 2 + (my - ny) ** 2 <= _NODE_R**2:
                return key
        return None

    def _can_submit(self) -> bool:
        t = self._mission.type
        if t == "neighbors":
            return len(self._selected) >= 3
        if t == "bridge":
            return len(self._selected) >= 1
        return False

    def _handle_click(self, pos: tuple[int, int]) -> None:
        m = self._mission

        if m.type == "analogy":
            for rect, opt in self._analogy_button_rects():
                if rect.collidepoint(pos):
                    self._selected = {opt}
                    self._submit()
            return

        key = self._node_at(pos)
        if key is None:
            return

        if m.type == "odd_one_out":
            candidates = set(m.answers + m.distractors)
            if key not in candidates:
                return
            self._selected = {key}
            self._submit()
            return

        if key in self._selected:
            self._selected.discard(key)
        else:
            if m.type == "neighbors" and len(self._selected) >= 3:
                return
            self._selected.add(key)

    def _analogy_button_rects(self) -> list[tuple[pygame.Rect, str]]:
        by = 360
        rects = []
        for opt in self._analogy_opts:
            rect = pygame.Rect(16, by, _LEFT_W - 32, 40)
            rects.append((rect, opt))
            by += 48
        return rects

    # ── submit ─────────────────────────────────────────────────────────────────

    def _submit(self) -> None:
        m = self._mission
        if m.type == "neighbors":
            correct = sum(1 for k in self._selected if k in m.answers)
            wrong = sum(1 for k in self._selected if k not in m.answers)
            raw = correct * 10 + wrong * (-5)
            is_correct = correct == 3 and wrong == 0
        elif m.type == "odd_one_out":
            chosen = next(iter(self._selected))
            is_correct = chosen == m.answers[0]
            raw = 20 if is_correct else -10
        elif m.type == "bridge":
            chosen = next(iter(self._selected))
            is_correct = chosen == m.answers[0]
            raw = 25 if is_correct else -5
        else:
            chosen = next(iter(self._selected))
            is_correct = chosen == m.answers[0]
            raw = 30 if is_correct else 0

        round_score = max(0, raw)
        result = {"type": m.type, "correct": is_correct, "score": round_score}
        new_score = self._session_score + round_score
        new_results = self._round_results + [result]

        if self._round_idx < len(self._missions) - 1:
            self._next = PhaseMissionScene(
                self._missions, self._round_idx + 1, new_score, new_results
            )
        else:
            from cognitive_data_arcade.games.semantic_space.phase_result import PhaseResultScene

            self._next = PhaseResultScene(session_score=new_score, round_results=new_results)
        self._done = True

    # ── update / draw ───────────────────────────────────────────────────────────

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_top_bar(surface)
        self._draw_left_panel(surface)
        self._draw_map(surface)

    def _draw_top_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _TOP_BG, (0, 0, _W, _TOP_H))
        pygame.draw.line(surface, _GREY, (0, _TOP_H), (_W, _TOP_H))
        title = get_font(14).render(
            "SEMANTIC SPACE EXPLORER", True, _TYPE_COLORS[self._mission.type]
        )
        surface.blit(title, (16, (_TOP_H - title.get_height()) // 2))
        rnd = get_font(13).render(
            f"Misja {self._round_idx + 1} / {len(self._missions)}", True, _DIM
        )
        surface.blit(rnd, (_W // 2 - rnd.get_width() // 2, (_TOP_H - rnd.get_height()) // 2))
        score = get_font(13).render(f"Wynik: {self._session_score} pkt", True, _AMBER)
        surface.blit(score, (_W - score.get_width() - 16, (_TOP_H - score.get_height()) // 2))

    def _draw_left_panel(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _LEFT_BG, (0, _TOP_H, _LEFT_W, _H - _TOP_H))
        pygame.draw.line(surface, _GREY, (_LEFT_W, _TOP_H), (_LEFT_W, _H))
        m = self._mission
        color = _TYPE_COLORS[m.type]
        y = _TOP_H + 16

        badge = get_font(10).render(_TYPE_LABELS[m.type], True, color)
        bx = 16
        pygame.draw.rect(
            surface,
            _BG,
            (bx - 4, y - 2, badge.get_width() + 8, badge.get_height() + 4),
            border_radius=4,
        )
        pygame.draw.rect(
            surface,
            color,
            (bx - 4, y - 2, badge.get_width() + 8, badge.get_height() + 4),
            1,
            border_radius=4,
        )
        surface.blit(badge, (bx, y))
        y += badge.get_height() + 14

        if m.type == "analogy":
            self._draw_left_analogy(surface, y)
        else:
            self._draw_left_standard(surface, y)

    def _draw_left_standard(self, surface: pygame.Surface, y: int) -> None:
        m = self._mission
        color = _TYPE_COLORS[m.type]

        if m.type == "neighbors":
            desc = get_font(13).render("Kliknij 3 slowa najblizsze:", True, _DIM)
            surface.blit(desc, (16, y))
            y += 28
            box = pygame.Rect(16, y, _LEFT_W - 32, 44)
            pygame.draw.rect(surface, (20, 15, 40), box, border_radius=6)
            pygame.draw.rect(surface, color, box, 2, border_radius=6)
            target_lbl = WORDS[m.target]["label"] if m.target in WORDS else m.target
            tl = get_font(20).render(target_lbl, True, color)
            surface.blit(
                tl, (box.centerx - tl.get_width() // 2, box.centery - tl.get_height() // 2)
            )
            y += 54
            prog = get_font(11).render(f"Zaznaczono: {len(self._selected)} / 3", True, _DIM)
            surface.blit(prog, (16, y))
            y += 20
            pw = int((len(self._selected) / 3) * (_LEFT_W - 32))
            pygame.draw.rect(surface, _GREY, (16, y, _LEFT_W - 32, 6), border_radius=3)
            if pw > 0:
                pygame.draw.rect(surface, color, (16, y, pw, 6), border_radius=3)
            y += 20
            for key in self._selected:
                lbl = WORDS[key]["label"] if key in WORDS else key
                sl = get_font(12).render(f"OK {lbl}", True, _GREEN)
                surface.blit(sl, (16, y))
                y += 22
        elif m.type == "odd_one_out":
            desc = get_font(13).render("Ktory wezel nie pasuje do grupy?", True, _DIM)
            surface.blit(desc, (16, y))
            y += 28
            note = get_font(11).render("(tylko 4 wezly sa aktywne)", True, _GREY)
            surface.blit(note, (16, y))
            y += 24
        elif m.type == "bridge":
            desc = get_font(13).render("Znajdz slowo laczace dwa klastry:", True, _DIM)
            surface.blit(desc, (16, y))
            y += 28
            note = get_font(11).render("Szukaj wezla na granicy kolorow.", True, _GREY)
            surface.blit(note, (16, y))
            y += 24
            if self._selected:
                key = next(iter(self._selected))
                lbl = WORDS[key]["label"] if key in WORDS else key
                sl = get_font(13).render(f"Wybrany: {lbl}", True, _GREEN)
                surface.blit(sl, (16, y))
                y += 24

        hint_y = _H - 120
        words = self._mission.hint_pl.split()
        line, hy = "", hint_y
        for word in words:
            candidate = f"{line} {word}".strip()
            if get_font(11).size(candidate)[0] <= _LEFT_W - 32:
                line = candidate
            else:
                surf = get_font(11).render(line, True, _GREY)
                surface.blit(surf, (16, hy))
                hy += 16
                line = word
        if line:
            surf = get_font(11).render(line, True, _GREY)
            surface.blit(surf, (16, hy))

        if self._can_submit():
            btn = pygame.Rect(16, _H - 64, _LEFT_W - 32, 44)
            pygame.draw.rect(surface, (30, 30, 60), btn, border_radius=6)
            pygame.draw.rect(surface, _TYPE_COLORS[self._mission.type], btn, 2, border_radius=6)
            bl = get_font(14).render("ZATWIERDZ (SPACJA)", True, _WHITE)
            surface.blit(
                bl, (btn.centerx - bl.get_width() // 2, btn.centery - bl.get_height() // 2)
            )

    def _draw_left_analogy(self, surface: pygame.Surface, y: int) -> None:
        m = self._mission
        color = _TYPE_COLORS["analogy"]

        formula = get_font(16).render(m.formula, True, _WHITE)
        surface.blit(formula, (_LEFT_W // 2 - formula.get_width() // 2, y))
        y += 36

        note = get_font(11).render("Kliknij poprawna odpowiedz:", True, _DIM)
        surface.blit(note, (16, y))
        y += 24

        for rect, opt in self._analogy_button_rects():
            is_sel = opt in self._selected
            bg = (30, 20, 50) if is_sel else (18, 18, 38)
            border = color if is_sel else _GREY
            pygame.draw.rect(surface, bg, rect, border_radius=6)
            pygame.draw.rect(surface, border, rect, 1, border_radius=6)
            ol = get_font(14).render(opt, True, _WHITE if is_sel else _DIM)
            surface.blit(
                ol, (rect.centerx - ol.get_width() // 2, rect.centery - ol.get_height() // 2)
            )

    def _draw_map(self, surface: pygame.Surface) -> None:
        m = self._mission
        if m.type == "odd_one_out":
            active = set(m.answers + m.distractors)
        else:
            active = set(WORDS.keys())

        for key_a, neighbors in SIMILARITIES.items():
            nx_a, ny_a = self._node_pos[key_a]
            for nb, sim in neighbors[:4]:
                if nb > key_a and key_a in {k for k, _ in SIMILARITIES[nb][:4]}:
                    nx_b, ny_b = self._node_pos[nb]
                    alpha = int(40 + sim * 120)
                    thickness = max(1, int(sim * 3))
                    col = tuple(
                        min(255, int(c * (alpha / 255) + 15 * (1 - alpha / 255)))
                        for c in (80, 80, 110)
                    )
                    pygame.draw.line(surface, col, (nx_a, ny_a), (nx_b, ny_b), thickness)

        from collections import defaultdict

        cluster_pts: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for key, (nx, ny) in self._node_pos.items():
            cluster_pts[WORDS[key]["cluster"]].append((nx, ny))
        for cname, pts in cluster_pts.items():
            cx = sum(x for x, _ in pts) // len(pts)
            cy = sum(y for _, y in pts) // len(pts)
            cl_color = CLUSTERS[cname]["color"]
            cl_lbl = get_font(9).render(
                CLUSTERS[cname]["label"].upper(), True, tuple(min(255, c + 40) for c in cl_color)
            )
            surface.blit(cl_lbl, (cx - cl_lbl.get_width() // 2, cy - cl_lbl.get_height() // 2))

        target_key = m.target if m.target in WORDS else None
        for key, (nx, ny) in self._node_pos.items():
            wd = WORDS[key]
            cl_color = CLUSTERS[wd["cluster"]]["color"]
            is_selected = key in self._selected
            is_target = key == target_key and m.type != "bridge"
            is_hover = key == self._hover
            is_active = key in active

            if not is_active:
                dim_col = tuple(c // 4 for c in cl_color)
                pygame.draw.circle(surface, dim_col, (nx, ny), _NODE_R)
                continue

            fill = cl_color if not is_selected else _GREEN
            pygame.draw.circle(surface, fill, (nx, ny), _NODE_R)

            if is_target:
                pygame.draw.circle(surface, _AMBER, (nx, ny), _NODE_R + 3, 2)
            elif is_selected:
                pygame.draw.circle(surface, _GREEN, (nx, ny), _NODE_R + 2, 2)
            elif is_hover:
                pygame.draw.circle(surface, _WHITE, (nx, ny), _NODE_R + 1, 1)
            elif m.type == "odd_one_out":
                pygame.draw.circle(surface, _WHITE, (nx, ny), _NODE_R + 2, 1)

            label = wd["label"]
            lbl = get_font(9).render(label, True, _WHITE)
            surface.blit(lbl, (nx - lbl.get_width() // 2, ny + _NODE_R + 2))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

from __future__ import annotations

import random

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.topic_detective.missions import Mission
from cognitive_data_arcade.games.topic_detective.topic_data import TOPICS

_W, _H = 1024, 720
_TOP_H = 44
_LEFT_W = 320
_BG = (15, 15, 35)
_TOP_BG = (10, 10, 28)
_LEFT_BG = (12, 12, 32)
_RIGHT_BG = (12, 12, 30)
_WHITE = (240, 240, 240)
_DIM = (100, 100, 140)
_AMBER = (240, 165, 0)
_GREEN = (39, 174, 96)
_RED = (231, 76, 60)
_GREY = (60, 60, 80)

_TYPE_LABELS = {
    "name_topic": "NAZWIJ TEMAT",
    "assign_doc": "PRZYPISZ DOKUMENT",
    "intruder": "INTRUZ W TEMACIE",
}
_TYPE_COLORS = {
    "name_topic": (240, 165, 0),
    "assign_doc": (52, 152, 219),
    "intruder": (231, 76, 60),
}

_BUTTONS_Y = _TOP_H + 220


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
        self._answered = False
        self._is_correct = False
        self._reveal_timer = 0.0
        self._pending_score = session_score
        self._pending_results = list(round_results)
        self._done = False
        self._next: Scene | None = None

        if self._mission.type == "intruder":
            words = list(self._mission.payload["all_words"])
            random.shuffle(words)
            self._intruder_words = words
        else:
            self._intruder_words = []

    # -- events -----------------------------------------------------------------

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._done:
            return
        if self._answered and self._mission.type == "assign_doc":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._advance_to_next(self._pending_score, self._pending_results)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._advance_to_next(self._pending_score, self._pending_results)
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_click(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self._mission.type == "intruder" and self._selected:
                self._submit()

    def _handle_click(self, pos: tuple[int, int]) -> None:
        m = self._mission
        if m.type in ("name_topic", "assign_doc"):
            for rect, topic_key in self._topic_button_rects():
                if rect.collidepoint(pos):
                    self._selected = {topic_key}
                    self._submit()
                    return
        elif m.type == "intruder":
            for rect, word in self._chip_rects():
                if rect.collidepoint(pos):
                    self._selected = {word}
                    return

    def _topic_button_rects(self) -> list[tuple[pygame.Rect, str]]:
        y = _BUTTONS_Y
        rects = []
        for tk in TOPICS:
            rect = pygame.Rect(16, y, _LEFT_W - 32, 36)
            rects.append((rect, tk))
            y += 44
        return rects

    def _chip_rects(self) -> list[tuple[pygame.Rect, str]]:
        rects = []
        x, y = 16, _TOP_H + 130
        for word in self._intruder_words:
            w = get_font(13).size(word)[0] + 20
            if x + w > _LEFT_W - 8:
                x = 16
                y += 36
            rect = pygame.Rect(x, y, w, 30)
            rects.append((rect, word))
            x += w + 6
        return rects

    # -- submit -----------------------------------------------------------------

    def _submit(self) -> None:
        m = self._mission
        chosen = next(iter(self._selected))
        if m.type == "name_topic":
            self._is_correct = chosen == m.answer
            self._finish(15 if self._is_correct else -5)
        elif m.type == "assign_doc":
            self._is_correct = chosen == m.answer
            raw = 20 if self._is_correct else -5
            round_score = max(0, raw)
            result = {"type": m.type, "correct": self._is_correct, "score": round_score}
            self._pending_score = self._session_score + round_score
            self._pending_results = self._round_results + [result]
            self._answered = True
            self._reveal_timer = 1500.0
        elif m.type == "intruder":
            self._is_correct = chosen == m.answer
            self._finish(25 if self._is_correct else -10)

    def _finish(self, raw: int) -> None:
        m = self._mission
        round_score = max(0, raw)
        result = {"type": m.type, "correct": self._is_correct, "score": round_score}
        self._advance_to_next(
            self._session_score + round_score,
            self._round_results + [result],
        )

    def _advance_to_next(self, new_score: int, new_results: list[dict]) -> None:
        if self._round_idx < len(self._missions) - 1:
            self._next = PhaseMissionScene(
                self._missions, self._round_idx + 1, new_score, new_results
            )
        else:
            from cognitive_data_arcade.games.topic_detective.phase_result import PhaseResultScene

            self._next = PhaseResultScene(session_score=new_score, round_results=new_results)
        self._done = True

    # -- update -----------------------------------------------------------------

    def update(self, dt_ms: float = 0.0) -> None:
        if self._answered and self._mission.type == "assign_doc" and not self._done:
            self._reveal_timer -= dt_ms
            if self._reveal_timer <= 0:
                self._advance_to_next(self._pending_score, self._pending_results)

    # -- draw -------------------------------------------------------------------

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_top_bar(surface)
        self._draw_left_panel(surface)
        self._draw_right_panel(surface)

    def _draw_top_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _TOP_BG, (0, 0, _W, _TOP_H))
        pygame.draw.line(surface, _GREY, (0, _TOP_H), (_W, _TOP_H))
        color = _TYPE_COLORS[self._mission.type]
        title = get_font(14).render("TOPIC DETECTIVE", True, color)
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
        y = _TOP_H + 14

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
        y += badge.get_height() + 12

        if m.type == "name_topic":
            self._draw_left_name_topic(surface, y)
        elif m.type == "assign_doc":
            self._draw_left_assign_doc(surface, y)
        elif m.type == "intruder":
            self._draw_left_intruder(surface, y)

    def _draw_left_name_topic(self, surface: pygame.Surface, y: int) -> None:
        m = self._mission
        desc = get_font(13).render("Ktory temat pasuje do tych slow?", True, _DIM)
        surface.blit(desc, (16, y))
        y += 26

        for word in m.payload["top5_words"]:
            cs = get_font(14).render(word, True, _AMBER)
            cx = _LEFT_W // 2 - cs.get_width() // 2
            pygame.draw.rect(
                surface,
                (28, 20, 10),
                (cx - 8, y - 2, cs.get_width() + 16, cs.get_height() + 4),
                border_radius=4,
            )
            surface.blit(cs, (cx, y))
            y += 28

        for rect, tk in self._topic_button_rects():
            td = TOPICS[tk]
            is_sel = tk in self._selected
            bg = (
                tuple(c // 2 for c in td["color"]) if is_sel else tuple(c // 4 for c in td["color"])
            )
            pygame.draw.rect(surface, bg, rect, border_radius=6)
            pygame.draw.rect(surface, td["color"], rect, 2 if is_sel else 1, border_radius=6)
            lbl = get_font(13).render(td["label_pl"], True, _WHITE if is_sel else _DIM)
            surface.blit(
                lbl, (rect.centerx - lbl.get_width() // 2, rect.centery - lbl.get_height() // 2)
            )

    def _draw_left_assign_doc(self, surface: pygame.Surface, y: int) -> None:
        m = self._mission
        desc = get_font(12).render("Ktory temat dominuje w tym tekscie?", True, _DIM)
        surface.blit(desc, (16, y))
        y += 22

        words = m.payload["text_pl"].split()
        line_buf = ""
        for word in words:
            candidate = f"{line_buf} {word}".strip()
            if get_font(12).size(candidate)[0] <= _LEFT_W - 32:
                line_buf = candidate
            else:
                surf = get_font(12).render(line_buf, True, _WHITE)
                surface.blit(surf, (16, y))
                y += 18
                line_buf = word
        if line_buf:
            surf = get_font(12).render(line_buf, True, _WHITE)
            surface.blit(surf, (16, y))
            y += 18
        y += 8

        if not self._answered:
            for rect, tk in self._topic_button_rects():
                td = TOPICS[tk]
                pygame.draw.rect(surface, tuple(c // 4 for c in td["color"]), rect, border_radius=6)
                pygame.draw.rect(surface, td["color"], rect, 1, border_radius=6)
                lbl = get_font(13).render(td["label_pl"], True, _DIM)
                surface.blit(
                    lbl, (rect.centerx - lbl.get_width() // 2, rect.centery - lbl.get_height() // 2)
                )
        else:
            res_color = _GREEN if self._is_correct else _RED
            res_text = (
                "Poprawnie!"
                if self._is_correct
                else f"Blad -- dominuje: {TOPICS[m.answer]['label_pl']}"
            )
            res_surf = get_font(13).render(res_text, True, res_color)
            surface.blit(res_surf, (16, _BUTTONS_Y))
            hint = get_font(11).render("Spacja = dalej", True, _GREY)
            surface.blit(hint, (16, _BUTTONS_Y + 24))

    def _draw_left_intruder(self, surface: pygame.Surface, y: int) -> None:
        m = self._mission
        topic_label = TOPICS[m.payload["topic_key"]]["label_pl"]
        desc = get_font(12).render(f"Temat: {topic_label} -- kliknij intruza!", True, _DIM)
        surface.blit(desc, (16, y))
        y += 22

        for rect, word in self._chip_rects():
            is_sel = word in self._selected
            topic_color = TOPICS[m.payload["topic_key"]]["color"]
            bg = tuple(c // 2 for c in topic_color) if is_sel else (25, 20, 35)
            border = _WHITE if is_sel else _GREY
            pygame.draw.rect(surface, bg, rect, border_radius=4)
            pygame.draw.rect(surface, border, rect, 1, border_radius=4)
            cl = get_font(13).render(word, True, _WHITE if is_sel else _DIM)
            surface.blit(
                cl, (rect.centerx - cl.get_width() // 2, rect.centery - cl.get_height() // 2)
            )

        if self._selected:
            btn = pygame.Rect(16, _H - 64, _LEFT_W - 32, 44)
            pygame.draw.rect(surface, (30, 10, 10), btn, border_radius=6)
            pygame.draw.rect(surface, _RED, btn, 2, border_radius=6)
            bl = get_font(14).render("ZATWIERDZ (SPACJA)", True, _WHITE)
            surface.blit(
                bl, (btn.centerx - bl.get_width() // 2, btn.centery - bl.get_height() // 2)
            )

    def _draw_right_panel(self, surface: pygame.Surface) -> None:
        m = self._mission
        rx = _LEFT_W + 8
        rw = _W - rx - 8
        pygame.draw.rect(surface, _RIGHT_BG, (rx, _TOP_H, rw, _H - _TOP_H))

        if m.type == "intruder":
            self._draw_right_intruder(surface, rx, rw)
        else:
            self._draw_right_fingerprints(surface, rx, rw)
            if m.type == "assign_doc" and self._answered:
                self._draw_probability_bars(surface, rx, rw)

    def _draw_right_fingerprints(self, surface: pygame.Surface, rx: int, rw: int) -> None:
        hdr = get_font(10).render("ODCISKI PALCOW TEMATOW", True, _GREY)
        surface.blit(hdr, (rx + (rw - hdr.get_width()) // 2, _TOP_H + 6))

        card_h, card_gap = 80, 6
        start_y = _TOP_H + 22
        for tk in TOPICS:
            td = TOPICS[tk]
            cy = start_y
            cx = rx + 8
            cw = rw - 16
            color = td["color"]
            pygame.draw.rect(
                surface, tuple(c // 4 for c in color), (cx, cy, cw, card_h), border_radius=6
            )
            pygame.draw.rect(surface, color, (cx, cy, cw, card_h), 1, border_radius=6)
            label = get_font(11).render(td["label_pl"].upper(), True, color)
            surface.blit(label, (cx + 8, cy + 5))
            words_str = "  ".join(td["words"][:5])
            wl = get_font(10).render(words_str, True, _DIM)
            surface.blit(wl, (cx + 8, cy + 22))
            start_y += card_h + card_gap

    def _draw_probability_bars(self, surface: pygame.Surface, rx: int, rw: int) -> None:
        m = self._mission
        weights = m.payload["weights"]
        bar_y = _TOP_H + 22 + 5 * (80 + 6) + 10
        hdr = get_font(10).render("ROZKLAD LDA (odkryty):", True, _AMBER)
        surface.blit(hdr, (rx + 8, bar_y))
        bar_y += 16
        for tk, weight in sorted(weights.items(), key=lambda x: -x[1]):
            td = TOPICS[tk]
            bar_w = int((rw - 32) * weight)
            color = td["color"]
            pygame.draw.rect(
                surface, tuple(c // 4 for c in color), (rx + 8, bar_y, rw - 32, 14), border_radius=3
            )
            if bar_w > 0:
                pygame.draw.rect(surface, color, (rx + 8, bar_y, bar_w, 14), border_radius=3)
            pct_lbl = get_font(9).render(f"{td['label_pl']}: {int(weight * 100)}%", True, _DIM)
            surface.blit(pct_lbl, (rx + rw - pct_lbl.get_width() - 8, bar_y))
            bar_y += 18

    def _draw_right_intruder(self, surface: pygame.Surface, rx: int, rw: int) -> None:
        m = self._mission
        tk = m.payload["topic_key"]
        td = TOPICS[tk]
        color = td["color"]
        hdr = get_font(11).render(f"Slowa tematu: {td['label_pl']}", True, color)
        surface.blit(hdr, (rx + 8, _TOP_H + 10))
        y = _TOP_H + 32
        for word in td["words"]:
            wl = get_font(12).render(f"  {word}", True, _DIM)
            surface.blit(wl, (rx + 8, y))
            y += 22

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

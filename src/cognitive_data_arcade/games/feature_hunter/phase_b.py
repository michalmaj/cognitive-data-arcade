from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.feature_hunter.config import DifficultyConfig
from cognitive_data_arcade.games.feature_hunter.features import draw_features, Feature
from cognitive_data_arcade.games.feature_hunter.simulator import compute_accuracy_delta
from cognitive_data_arcade.games.feature_hunter.widgets import (
    FeatureCard, render_card, grid_layout,
)

_BG    = (15, 15, 35)
_PANEL = (18, 18, 42)
_WHITE = (240, 240, 240)
_DIM   = (120, 120, 160)
_ORANGE = (243, 156, 18)
_GREEN = (39, 174, 96)
_RED   = (231, 76, 60)
_BLUE  = (52, 152, 219)

_W, _H    = 1024, 720
_TOP_H    = 64
_BIN_W    = 160
_CZONE_X  = _BIN_W                      # 160
_CZONE_W  = _W - 2 * _BIN_W            # 704
_CZONE_Y  = _TOP_H                      # 64
_CZONE_H  = _H - _TOP_H - 50           # 606
_CONFIRM_Y = _H - 46
_TOTAL_ROUNDS = 5


def compute_round_score(
    correct: int, total: int, timer_remaining: float, difficulty: DifficultyConfig
) -> int:
    base = correct * 10
    perfect_bonus = 20 if correct == total else 0
    time_bonus = int(timer_remaining // 5) * difficulty.time_bonus_per_5s
    return base + perfect_bonus + time_bonus


class PhaseBScene(Scene):
    def __init__(self, difficulty: DifficultyConfig, session_seed: int = 0) -> None:
        self._difficulty = difficulty
        self._session_seed = session_seed
        self._round_idx = 0
        self._session_score = 0
        self._round_results: list[tuple[int, int, int]] = []  # (correct, total, score)
        self._cards: list[FeatureCard] = []
        self._dragging: FeatureCard | None = None
        self._drag_offset: tuple[int, int] = (0, 0)
        self._timer_remaining: float = 0.0
        self._hint_card: FeatureCard | None = None
        self._state = "playing"
        self._round_score = 0
        self._done = False
        self._next: Scene | None = None
        self._load_round()

    def _load_round(self) -> None:
        diff = self._difficulty
        features = draw_features(diff, self._session_seed, self._round_idx)
        n = diff.card_count
        cols, rows = grid_layout(n)
        cell_w = _CZONE_W // cols
        cell_h = _CZONE_H // rows
        card_w = cell_w - 12
        card_h = cell_h - 12

        self._cards = []
        for i, feat in enumerate(features):
            col = i % cols
            row = i // cols
            x = _CZONE_X + col * cell_w + 6
            y = _CZONE_Y + row * cell_h + 6
            seed = self._session_seed * 1000 + self._round_idx * 100 + i
            surf = render_card(feat, card_w, card_h, seed)
            home = pygame.Rect(x, y, card_w, card_h)
            self._cards.append(
                FeatureCard(feature=feat, surface=surf, home_rect=home, rect=home.copy())
            )

        self._timer_remaining = diff.timer_s if diff.timer_s is not None else 0.0
        self._state = "playing"
        self._hint_card = None

    def _all_assigned(self) -> bool:
        return all(c.assigned is not None for c in self._cards)

    def _confirm(self) -> None:
        correct = sum(
            1 for c in self._cards
            if (c.assigned == "useful") == c.feature.is_signal
        )
        total = len(self._cards)
        score = compute_round_score(
            correct, total,
            max(0.0, self._timer_remaining),
            self._difficulty,
        )
        self._round_score = score
        self._session_score += score
        self._round_results.append((correct, total, score))
        self._state = "revealed"

    def _advance(self) -> None:
        self._round_idx += 1
        if self._round_idx >= _TOTAL_ROUNDS:
            from cognitive_data_arcade.games.feature_hunter.phase_c import PhaseCScene
            self._done = True
            self._next = PhaseCScene(self._session_score, self._round_results)
        else:
            self._load_round()

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._state == "playing":
            self._handle_playing_event(event)
        elif self._state == "revealed":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                btn = pygame.Rect(_W - 220, _CONFIRM_Y, 208, 36)
                if btn.collidepoint(event.pos):
                    self._advance()

    def _handle_playing_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self._all_assigned():
                    btn = pygame.Rect(_W // 2 - 100, _CONFIRM_Y, 200, 36)
                    if btn.collidepoint(event.pos):
                        self._confirm()
                        return
                for card in reversed(self._cards):
                    if card.assigned is None and card.rect.collidepoint(event.pos):
                        self._dragging = card
                        ox = event.pos[0] - card.rect.left
                        oy = event.pos[1] - card.rect.top
                        self._drag_offset = (ox, oy)
                        break
            elif event.button == 3 and self._difficulty.hints != "none":
                self._hint_card = None
                for card in reversed(self._cards):
                    if card.assigned is None and card.rect.collidepoint(event.pos):
                        self._hint_card = card
                        break

        elif event.type == pygame.MOUSEMOTION:
            if self._dragging:
                ox, oy = self._drag_offset
                self._dragging.rect.topleft = (event.pos[0] - ox, event.pos[1] - oy)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._dragging:
                cx = self._dragging.rect.centerx
                if cx < _CZONE_X:
                    self._dragging.assigned = "noise"
                elif cx > _CZONE_X + _CZONE_W:
                    self._dragging.assigned = "useful"
                else:
                    self._dragging.rect = self._dragging.home_rect.copy()
                self._dragging = None

    def update(self, dt_ms: float = 0.0) -> None:
        if self._state == "playing" and self._difficulty.timer_s is not None:
            self._timer_remaining -= dt_ms / 1000.0
            if self._timer_remaining <= 0.0:
                self._timer_remaining = 0.0
                for c in self._cards:
                    if c.assigned is None:
                        c.assigned = "noise"
                self._confirm()

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_top_bar(surface)
        self._draw_bins(surface)
        self._draw_cards(surface)
        if self._state == "playing":
            self._draw_confirm_button(surface)
            if self._hint_card is not None:
                self._draw_hint_popup(surface)
        elif self._state == "revealed":
            self._draw_reveal_overlays(surface)
            self._draw_reveal_summary(surface)
            self._draw_next_round_button(surface)

    def _draw_top_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, _TOP_H))
        font_sm = get_font(13)
        font_lg = get_font(20)
        surface.blit(font_sm.render(f"Runda {self._round_idx + 1} / {_TOTAL_ROUNDS}", True, _ORANGE), (12, 6))
        surface.blit(font_lg.render(self._difficulty.name_pl, True, _WHITE), (12, 24))
        score_txt = f"Wynik: {self._session_score}"
        sw = get_font(16).size(score_txt)[0]
        surface.blit(get_font(16).render(score_txt, True, _DIM), (_W - sw - 12, 24))

        if self._difficulty.timer_s is not None and self._state == "playing":
            max_t = self._difficulty.timer_s
            ratio = max(0.0, self._timer_remaining / max_t)
            bar_w = int(200 * ratio)
            col = _RED if self._timer_remaining < 10 else _ORANGE
            if bar_w > 0:
                pygame.draw.rect(surface, col, (_W // 2 - 100, 18, bar_w, 24), border_radius=4)
            t_surf = get_font(18).render(f"{int(self._timer_remaining)}s", True, _WHITE)
            surface.blit(t_surf, (_W // 2 - t_surf.get_width() // 2, 20))

    def _draw_bins(self, surface: pygame.Surface) -> None:
        # Left bin — Szum
        pygame.draw.rect(surface, (30, 10, 10), (0, _CZONE_Y, _BIN_W, _CZONE_H))
        pygame.draw.rect(surface, _RED, (0, _CZONE_Y, _BIN_W, _CZONE_H), 2)
        lbl = get_font(15).render("SZUM", True, _RED)
        surface.blit(lbl, (_BIN_W // 2 - lbl.get_width() // 2, _CZONE_Y + 10))
        arrow = get_font(18).render("<--", True, _RED)
        surface.blit(arrow, (_BIN_W // 2 - arrow.get_width() // 2, _CZONE_Y + 32))
        y_off = _CZONE_Y + 60
        for c in self._cards:
            if c.assigned == "noise":
                nm = get_font(11).render(c.feature.name_pl, True, _RED)
                surface.blit(nm, (4, y_off))
                y_off += 18

        # Right bin — Przydatne
        pygame.draw.rect(surface, (10, 30, 10), (_W - _BIN_W, _CZONE_Y, _BIN_W, _CZONE_H))
        pygame.draw.rect(surface, _GREEN, (_W - _BIN_W, _CZONE_Y, _BIN_W, _CZONE_H), 2)
        lbl = get_font(13).render("PRZYDATNE", True, _GREEN)
        surface.blit(lbl, (_W - _BIN_W + (_BIN_W - lbl.get_width()) // 2, _CZONE_Y + 10))
        arrow = get_font(18).render("-->", True, _GREEN)
        surface.blit(arrow, (_W - _BIN_W + (_BIN_W - arrow.get_width()) // 2, _CZONE_Y + 32))
        y_off = _CZONE_Y + 60
        for c in self._cards:
            if c.assigned == "useful":
                nm = get_font(11).render(c.feature.name_pl, True, _GREEN)
                surface.blit(nm, (_W - _BIN_W + 4, y_off))
                y_off += 18

    def _draw_cards(self, surface: pygame.Surface) -> None:
        for card in self._cards:
            if card.assigned is None and card is not self._dragging:
                surface.blit(card.surface, card.rect)
                pygame.draw.rect(surface, _DIM, card.rect, 1, border_radius=4)
        if self._dragging is not None:
            surface.blit(self._dragging.surface, self._dragging.rect)
            pygame.draw.rect(surface, _ORANGE, self._dragging.rect, 2, border_radius=4)

    def _draw_confirm_button(self, surface: pygame.Surface) -> None:
        all_done = self._all_assigned()
        col = _GREEN if all_done else _DIM
        btn = pygame.Rect(_W // 2 - 100, _CONFIRM_Y, 200, 36)
        pygame.draw.rect(surface, _PANEL, btn, border_radius=4)
        pygame.draw.rect(surface, col, btn, 2, border_radius=4)
        lbl = get_font(16).render("Zatwierdź", True, col)
        surface.blit(lbl, (_W // 2 - lbl.get_width() // 2, _CONFIRM_Y + 8))

    def _draw_hint_popup(self, surface: pygame.Surface) -> None:
        card = self._hint_card
        if card is None:
            return
        popup_w, popup_h = 150, 58
        px = min(card.rect.right + 6, _W - popup_w - 2)
        py = card.rect.top
        pygame.draw.rect(surface, _PANEL, (px, py, popup_w, popup_h), border_radius=4)
        pygame.draw.rect(surface, _DIM, (px, py, popup_w, popup_h), 1, border_radius=4)
        if self._difficulty.hints == "full":
            r_val = card.feature.correlation
            r_surf = get_font(13).render(f"r = {r_val:.2f}", True, _ORANGE)
            surface.blit(r_surf, (px + 6, py + 8))
            direction = "wzrost" if r_val > 0 else "spadek"
            d_surf = get_font(11).render(f"Trend: {direction}", True, _DIM)
            surface.blit(d_surf, (px + 6, py + 30))
        else:
            s = get_font(11).render("Sprawdź wykres uważnie", True, _DIM)
            surface.blit(s, (px + 6, py + 20))

    def _draw_reveal_overlays(self, surface: pygame.Surface) -> None:
        for card in self._cards:
            correct = (card.assigned == "useful") == card.feature.is_signal
            col = _GREEN if correct else _RED
            symbol = "OK" if correct else "X"
            pygame.draw.rect(surface, col, card.home_rect, 3, border_radius=4)
            sym_surf = get_font(14).render(symbol, True, col)
            surface.blit(sym_surf, (card.home_rect.x + 4, card.home_rect.y + 4))
            surface.blit(card.surface, card.home_rect)
            pygame.draw.rect(surface, col, card.home_rect, 3, border_radius=4)

            acc_with, acc_without = compute_accuracy_delta(card.feature, seed=42)
            delta_pp = int((acc_with - acc_without) * 100)
            sign = "+" if delta_pp >= 0 else ""
            dt_surf = get_font(11).render(f"{sign}{delta_pp}pp", True, _ORANGE)
            surface.blit(dt_surf, (card.home_rect.x + 4, card.home_rect.bottom - 20))

            if self._difficulty.hints != "none":
                r_txt = get_font(10).render(f"r={card.feature.correlation:.2f}", True, _DIM)
                surface.blit(r_txt, (card.home_rect.right - r_txt.get_width() - 4, card.home_rect.bottom - 18))

    def _draw_reveal_summary(self, surface: pygame.Surface) -> None:
        if not self._round_results:
            return
        correct, total, score = self._round_results[-1]
        col = _GREEN if correct == total else (_ORANGE if correct >= total - 1 else _RED)
        txt = f"{correct}/{total} poprawnie! +{score} pkt"
        lbl = get_font(18).render(txt, True, col)
        surface.blit(lbl, (12, _CONFIRM_Y + 4))

    def _draw_next_round_button(self, surface: pygame.Surface) -> None:
        is_last = self._round_idx >= _TOTAL_ROUNDS - 1
        txt = "Wyniki sesji" if is_last else "Następna runda"
        btn = pygame.Rect(_W - 220, _CONFIRM_Y, 208, 36)
        pygame.draw.rect(surface, _PANEL, btn, border_radius=4)
        pygame.draw.rect(surface, _BLUE, btn, 2, border_radius=4)
        lbl = get_font(16).render(txt, True, _BLUE)
        surface.blit(lbl, (_W - 220 + (208 - lbl.get_width()) // 2, _CONFIRM_Y + 8))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

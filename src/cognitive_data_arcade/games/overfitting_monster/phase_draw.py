# src/cognitive_data_arcade/games/overfitting_monster/phase_draw.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.overfitting_monster.classifier import (
    compute_gap_stars, compute_round_score, knn_accuracies, split_data,
)
from cognitive_data_arcade.games.overfitting_monster.scenarios import Scenario, generate_data
from cognitive_data_arcade.games.overfitting_monster.widgets import SliderWidget

_BG     = (15, 15, 35)
_PANEL  = (18, 18, 42)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_GREEN  = (39, 174, 96)
_RED    = (231, 76, 60)
_BLUE   = (52, 152, 219)
_YELLOW = (243, 156, 18)
_ORANGE = (230, 126, 34)

_W, _H   = 1024, 720
_TOP_H   = 56
_SCATTER = pygame.Rect(12, _TOP_H + 4, 680, _H - _TOP_H - 8)
_PANEL_R = pygame.Rect(704, _TOP_H + 4, 308, _H - _TOP_H - 8)
_DOT_R   = 5
_POPUP_W, _POPUP_H = 290, 160
_TOTAL_ROUNDS = 5

# Slider rects (within right panel)
_SPLIT_SLIDER = pygame.Rect(712, 130, 292, 20)
_K_SLIDER     = pygame.Rect(712, 220, 292, 20)
_BTN_CONFIRM  = pygame.Rect(754, _H - 68, 220, 44)


def _wrap_text(text: str, font: pygame.font.Font, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class PhaseDrawScene(Scene):
    def __init__(
        self,
        scenario: Scenario,
        round_idx: int,
        session_seed: int,
        session_score: int,
        round_results: list[dict],
        scenario_order: list[int],
    ) -> None:
        self._scenario = scenario
        self._round_idx = round_idx
        self._session_seed = session_seed
        self._session_score = session_score
        self._round_results = round_results
        self._scenario_order = scenario_order

        self._seed = session_seed * 10 + round_idx
        self._X, self._y = generate_data(scenario, self._seed)

        self._split_slider = SliderWidget(_SPLIT_SLIDER, min_val=50, max_val=80, value=70)
        self._k_slider = SliderWidget(_K_SLIDER, min_val=1, max_val=15, value=5)

        self._train_acc: float = 0.0
        self._test_acc: float = 0.0
        self._recompute()

        self._popup_visible = False
        self._popup_pos: tuple[int, int] = (0, 0)
        self._done = False
        self._next: Scene | None = None

    def _recompute(self) -> None:
        X_tr, y_tr, X_te, y_te = split_data(
            self._X, self._y, self._split_slider.value, self._seed
        )
        accs = knn_accuracies(X_tr, y_tr, X_te, y_te, self._k_slider.value)
        self._train_acc = accs["train"]
        self._test_acc = accs["test"]

    def handle_event(self, event: pygame.event.Event) -> None:
        prev_split = self._split_slider.value
        prev_k = self._k_slider.value

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._popup_visible = False
                if _BTN_CONFIRM.collidepoint(event.pos):
                    self._confirm()
                    return
            elif event.button == 3:
                if _SCATTER.collidepoint(event.pos) or _PANEL_R.collidepoint(event.pos):
                    self._popup_visible = not self._popup_visible
                    self._popup_pos = event.pos
                    return
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._popup_visible = False

        self._split_slider.handle_event(event)
        self._k_slider.handle_event(event)
        if self._split_slider.value != prev_split or self._k_slider.value != prev_k:
            self._recompute()

    def _confirm(self) -> None:
        X_tr, y_tr, X_te, y_te = split_data(
            self._X, self._y, self._split_slider.value, self._seed
        )
        stars = compute_gap_stars(self._train_acc, self._test_acc)
        score = compute_round_score(self._test_acc, stars)

        result = {
            "round_idx": self._round_idx,
            "scenario_name": self._scenario.name_pl,
            "k": self._k_slider.value,
            "split_pct": self._split_slider.value,
            "train_acc": self._train_acc,
            "test_acc": self._test_acc,
            "gap": (self._train_acc - self._test_acc) * 100,
            "stars": stars,
            "score": score,
        }

        from cognitive_data_arcade.games.overfitting_monster.phase_round_result import (
            PhaseRoundResultScene, RoundDisplay,
        )
        display = RoundDisplay(
            scenario=self._scenario,
            k=self._k_slider.value,
            split_pct=self._split_slider.value,
            X_train=X_tr,
            y_train=y_tr,
            X_test=X_te,
            y_test=y_te,
            train_acc=self._train_acc,
            test_acc=self._test_acc,
            stars=stars,
            score=score,
        )
        self._next = PhaseRoundResultScene(
            display=display,
            round_idx=self._round_idx,
            session_seed=self._session_seed,
            session_score=self._session_score + score,
            round_results=self._round_results + [result],
            scenario_order=self._scenario_order,
        )
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        # Top strip
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, _TOP_H))
        title = get_font(20).render(
            f"Runda {self._round_idx + 1}/{_TOTAL_ROUNDS}  -  {self._scenario.name_pl}",
            True, _WHITE,
        )
        surface.blit(title, (20, 16))
        instr = get_font(13).render(
            "Ustaw k i podzial  |  PPM = podpowiedz  |  zatwierdz gdy gotowy",
            True, _DIM,
        )
        surface.blit(instr, (_W - instr.get_width() - 16, 20))

        # Scatter
        self._draw_scatter(surface)
        # Right panel
        pygame.draw.rect(surface, _PANEL, _PANEL_R, border_radius=4)
        self._draw_right_panel(surface)
        # Confirm button
        pygame.draw.rect(surface, _PANEL, _BTN_CONFIRM, border_radius=6)
        pygame.draw.rect(surface, _GREEN, _BTN_CONFIRM, 2, border_radius=6)
        lbl = get_font(18).render("Potwierdz", True, _GREEN)
        surface.blit(lbl, (
            _BTN_CONFIRM.centerx - lbl.get_width() // 2,
            _BTN_CONFIRM.centery - lbl.get_height() // 2,
        ))
        if self._popup_visible:
            self._draw_popup(surface)

    def _draw_scatter(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _BG, _SCATTER)
        pygame.draw.rect(surface, (40, 40, 80), _SCATTER, 1)
        split_pct = self._split_slider.value
        X_tr, y_tr, X_te, y_te = split_data(self._X, self._y, split_pct, self._seed)
        tr_set = set(map(tuple, X_tr.tolist()))
        for i, (x, y_val) in enumerate(self._X):
            cx = int(_SCATTER.x + x * _SCATTER.w)
            cy = int(_SCATTER.y + y_val * _SCATTER.h)
            color = _RED if self._y[i] == 0 else _BLUE
            if tuple(self._X[i].tolist()) in tr_set:
                pygame.draw.circle(surface, color, (cx, cy), _DOT_R)
            else:
                pygame.draw.rect(surface, color,
                                  pygame.Rect(cx - _DOT_R, cy - _DOT_R, _DOT_R * 2, _DOT_R * 2))
                pygame.draw.rect(surface, _WHITE,
                                  pygame.Rect(cx - _DOT_R, cy - _DOT_R, _DOT_R * 2, _DOT_R * 2), 1)

        legend_y = _SCATTER.bottom - 24
        pygame.draw.circle(surface, _DIM, (_SCATTER.x + 12, legend_y), 5)
        surface.blit(get_font(10).render("trening", True, _DIM), (_SCATTER.x + 20, legend_y - 6))
        pygame.draw.rect(surface, _DIM, pygame.Rect(_SCATTER.x + 72, legend_y - 5, 10, 10))
        surface.blit(get_font(10).render("test", True, _DIM), (_SCATTER.x + 84, legend_y - 6))

    def _draw_right_panel(self, surface: pygame.Surface) -> None:
        rx, ry = _PANEL_R.x + 8, _PANEL_R.y + 12

        # Split slider
        surface.blit(get_font(13).render("Podzial trening / test:", True, _DIM), (rx, ry))
        ry += 18
        self._split_slider.draw(
            surface,
            label="trening",
            value_text=f"{self._split_slider.value}% / {100 - self._split_slider.value}%",
            color=_GREEN,
        )
        ry += 50

        # k slider
        surface.blit(get_font(13).render("Liczba sasiadow KNN (k):", True, _DIM), (rx, ry))
        ry += 18
        self._k_slider.draw(
            surface,
            label="k=1 (overfit)",
            value_text=f"k = {self._k_slider.value}",
            color=_BLUE,
        )
        ry += 60

        # Live preview
        pygame.draw.line(surface, (40, 40, 80), (rx, ry), (rx + _PANEL_R.w - 16, ry))
        ry += 10
        surface.blit(get_font(13).render("Podglad na zywo:", True, _DIM), (rx, ry))
        ry += 22

        bar_max = _PANEL_R.w - 90
        gap = (self._train_acc - self._test_acc) * 100
        for label, acc, color in [
            ("Trening", self._train_acc, _GREEN),
            ("Test", self._test_acc, _RED),
        ]:
            lbl = get_font(13).render(label, True, color)
            surface.blit(lbl, (rx, ry))
            bw = int(bar_max * acc)
            if bw > 0:
                pygame.draw.rect(surface, color, pygame.Rect(rx + 64, ry + 2, bw, 14), border_radius=3)
            pct = get_font(12).render(f"{acc:.0%}", True, color)
            surface.blit(pct, (rx + 66 + bar_max, ry + 1))
            ry += 26

        gap_color = _GREEN if gap < 5 else (_ORANGE if gap < 15 else _RED)
        gap_lbl = get_font(13).render(f"Gap: {gap:.1f} pp", True, gap_color)
        surface.blit(gap_lbl, (rx, ry))
        ry += 28

        # Star preview
        stars = compute_gap_stars(self._train_acc, self._test_acc)
        star_str = ("xxx" if stars == 3 else "xx." if stars == 2 else "x..")
        bonus = {3: "+20 pkt", 2: "+10 pkt", 1: "+0 pkt"}[stars]
        star_surf = get_font(18).render(star_str, True, _YELLOW)
        bonus_surf = get_font(12).render(bonus, True, _YELLOW)
        surface.blit(star_surf, (rx, ry))
        surface.blit(bonus_surf, (rx + star_surf.get_width() + 6, ry + 4))
        ry += 36

        pygame.draw.line(surface, (40, 40, 80), (rx, ry), (rx + _PANEL_R.w - 16, ry))
        ry += 10
        hint = get_font(11).render("PPM = podpowiedz o scenariuszu", True, _DIM)
        surface.blit(hint, (rx, ry))

    def _draw_popup(self, surface: pygame.Surface) -> None:
        mx, my = self._popup_pos
        px = min(mx + 8, _W - _POPUP_W - 4)
        py = min(my + 8, _H - _POPUP_H - 4)
        popup = pygame.Rect(px, py, _POPUP_W, _POPUP_H)

        bg = pygame.Surface((_POPUP_W, _POPUP_H), pygame.SRCALPHA)
        bg.fill((20, 20, 50, 230))
        surface.blit(bg, popup.topleft)
        pygame.draw.rect(surface, _YELLOW, popup, 1, border_radius=4)

        title = get_font(15).render(self._scenario.name_pl, True, _YELLOW)
        surface.blit(title, (px + 8, py + 8))
        pygame.draw.line(surface, _DIM, (px + 8, py + 30), (px + _POPUP_W - 8, py + 30))

        font = get_font(11)
        lines = _wrap_text(self._scenario.hint_pl, font, _POPUP_W - 16)
        for i, line in enumerate(lines[:7]):
            lbl = font.render(line, True, _WHITE)
            surface.blit(lbl, (px + 8, py + 36 + i * 16))

        close = get_font(10).render("[PPM] zamknij", True, _DIM)
        surface.blit(close, (px + 8, py + _POPUP_H - 16))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

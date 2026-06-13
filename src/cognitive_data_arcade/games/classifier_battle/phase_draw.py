from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.classifier_battle.classifier import (
    classifier_accuracies, compute_round_score, player_accuracy,
)
from cognitive_data_arcade.games.classifier_battle.scenarios import SCENARIOS, Scenario, generate_data
from cognitive_data_arcade.games.classifier_battle.widgets import DrawCanvas

_BG    = (15, 15, 35)
_PANEL = (18, 18, 42)
_WHITE = (240, 240, 240)
_DIM   = (120, 120, 160)
_YELLOW = (243, 156, 18)
_GREEN  = (39, 174, 96)
_RED    = (231, 76, 60)
_BLUE   = (52, 152, 219)

_W, _H = 1024, 720
_TOP_H = 56
_CANVAS_RECT = pygame.Rect(12, _TOP_H + 4, 750, _H - _TOP_H - 4 - 60)
_BTN_CLEAR   = pygame.Rect(778, 650, 110, 40)
_BTN_CONFIRM = pygame.Rect(900, 650, 112, 40)

_POPUP_W, _POPUP_H = 290, 150
_TOTAL_ROUNDS = 5


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
    ) -> None:
        self._scenario = scenario
        self._round_idx = round_idx
        self._session_seed = session_seed
        self._session_score = session_score
        self._round_results = round_results

        seed = session_seed * 10 + round_idx
        self._X, self._y = generate_data(scenario, seed)
        self._clf_accs = classifier_accuracies(self._X, self._y, seed=seed)

        self._canvas = DrawCanvas(_CANVAS_RECT)
        self._canvas.load_data(self._X, self._y)

        self._popup_visible = False
        self._popup_pos: tuple[int, int] = (0, 0)

        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._popup_visible = False
                if _BTN_CLEAR.collidepoint(event.pos):
                    self._canvas.clear()
                    return
                if _BTN_CONFIRM.collidepoint(event.pos) and self._canvas.is_valid():
                    self._confirm()
                    return
                self._canvas.handle_event(event)
            elif event.button == 3:
                if self._canvas.rect.collidepoint(event.pos):
                    self._popup_visible = not self._popup_visible
                    self._popup_pos = event.pos
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._popup_visible = False
        else:
            self._canvas.handle_event(event)

    def _confirm(self) -> None:
        poly_norm = self._canvas.polyline_normalised
        acc = player_accuracy(poly_norm, self._X, self._y)
        score = compute_round_score(acc, self._clf_accs)

        result = {
            "round_idx": self._round_idx,
            "scenario_name": self._scenario.name_pl,
            "player_acc": acc,
            "clf_accs": self._clf_accs,
            "score": score,
        }
        new_results = self._round_results + [result]

        from cognitive_data_arcade.games.classifier_battle.phase_round_result import (
            PhaseRoundResultScene, RoundDisplay,
        )
        display = RoundDisplay(
            scenario=self._scenario,
            player_acc=acc,
            clf_accs=self._clf_accs,
            score=score,
            polyline_norm=poly_norm,
            X=self._X,
            y=self._y,
        )
        self._next = PhaseRoundResultScene(
            display=display,
            round_idx=self._round_idx,
            session_seed=self._session_seed,
            session_score=self._session_score + score,
            round_results=new_results,
        )
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)

        # Top strip
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, _TOP_H))
        title = get_font(20).render(
            f"Runda {self._round_idx + 1}/{_TOTAL_ROUNDS}  —  {self._scenario.name_pl}",
            True, _WHITE,
        )
        surface.blit(title, (20, 16))
        instr = get_font(13).render(
            "Narysuj granicę  |  PPM = podpowiedź  |  potwierdź gdy linia przechodzi przez cały ekran",
            True, _DIM,
        )
        surface.blit(instr, (_W - instr.get_width() - 16, 20))

        # Canvas
        self._canvas.draw(surface)

        # Right panel
        self._draw_right_panel(surface)

        # Buttons
        self._draw_button(surface, _BTN_CLEAR, "Wyczyść", _RED)
        confirm_col = _GREEN if self._canvas.is_valid() else _DIM
        self._draw_button(surface, _BTN_CONFIRM, "Potwierdź", confirm_col)

        # Popup
        if self._popup_visible:
            self._draw_popup(surface)

    def _draw_right_panel(self, surface: pygame.Surface) -> None:
        panel = pygame.Rect(778, _TOP_H + 4, 234, 580)
        pygame.draw.rect(surface, _PANEL, panel, border_radius=4)
        font = get_font(13)
        hint = font.render("PPM na ekranie = podpowiedź", True, _DIM)
        surface.blit(hint, (panel.x + 8, panel.y + 12))

        if not self._canvas.is_valid() and len(self._canvas.polyline) >= 2:
            msg = get_font(12).render("Narysuj od góry do dołu!", True, _RED)
            surface.blit(msg, (panel.x + 8, panel.y + 40))

    def _draw_button(self, surface: pygame.Surface, rect: pygame.Rect,
                     label: str, color: tuple) -> None:
        pygame.draw.rect(surface, _PANEL, rect, border_radius=6)
        pygame.draw.rect(surface, color, rect, 2, border_radius=6)
        lbl = get_font(16).render(label, True, color)
        surface.blit(lbl, (rect.centerx - lbl.get_width() // 2,
                            rect.centery - lbl.get_height() // 2))

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
        for i, line in enumerate(lines[:6]):
            lbl = font.render(line, True, _WHITE)
            surface.blit(lbl, (px + 8, py + 36 + i * 16))

        close = get_font(10).render("[PPM] zamknij", True, _DIM)
        surface.blit(close, (px + 8, py + _POPUP_H - 16))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

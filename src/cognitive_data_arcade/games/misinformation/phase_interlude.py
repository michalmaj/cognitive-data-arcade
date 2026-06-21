# src/cognitive_data_arcade/games/misinformation/phase_interlude.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.misinformation.networks import ROUNDS

from cognitive_data_arcade.engine.colors import BG as _BG

_W, _H = 1024, 720


class PhaseInterludeScene(Scene):
    def __init__(
        self,
        round_idx: int,  # 0-based index into ROUNDS
        act: str,  # "spreader" | "factchecker" (the act that just ended)
        act_score: int,
        session_scores: list[int],  # already includes act_score as last element
    ) -> None:
        self._round_idx = round_idx
        self._act = act
        self._act_score = act_score
        self._session_scores = list(session_scores)
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._advance()

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def _advance(self) -> None:
        if self._done:
            return
        self._done = True
        from cognitive_data_arcade.games.misinformation.phase_act import PhaseActScene
        from cognitive_data_arcade.games.misinformation.phase_result import PhaseResultScene

        if self._act == "spreader":
            # always: after spreader -> factchecker on same round
            self._next = PhaseActScene(
                cfg=ROUNDS[self._round_idx],
                round_idx=self._round_idx,
                act="factchecker",
                session_scores=self._session_scores,
            )
        elif self._round_idx < 2:
            # after factchecker, more rounds remain -> next round's spreader
            self._next = PhaseActScene(
                cfg=ROUNDS[self._round_idx + 1],
                round_idx=self._round_idx + 1,
                act="spreader",
                session_scores=self._session_scores,
            )
        else:
            # after factchecker on round 3 -> result screen
            self._next = PhaseResultScene(self._session_scores)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        lines: list[tuple[str, tuple[int, int, int]]] = []

        if self._act == "spreader":
            cel_met = self._act_score >= 60
            met_txt = "CEL OSIAGNIETY!" if cel_met else "cel nie osiagniety"
            lines = [
                (f"Zaraziles {self._act_score}% sieci!", (231, 76, 60)),
                (f"[cel >=60%:  {met_txt}]", (180, 180, 180)),
                ("", (0, 0, 0)),
                ("Teraz sprobuj to zatrzymac...", (52, 152, 219)),
            ]
        else:
            # last two scores: spreader was session_scores[-2], factchecker = act_score
            spread_score = self._session_scores[-2] if len(self._session_scores) >= 2 else 0
            lines = [
                (f"Runda {self._round_idx + 1} zakonczona.", (240, 240, 240)),
                (
                    f"Spreader: {spread_score}%     Fact-Checker: {self._act_score}%",
                    (180, 180, 180),
                ),
            ]
            if self._round_idx < 2:
                lines.append(("", (0, 0, 0)))
                lines.append(("Nastepna runda...", (200, 160, 60)))

        y = _H // 2 - len(lines) * 24
        for text, color in lines:
            if text:
                surf = get_font(22).render(text, True, color)
                surface.blit(surf, (_W // 2 - surf.get_width() // 2, y))
            y += 48

        hint = get_font(13).render("SPACJA aby kontynuowac", True, (80, 80, 100))
        surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 54))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

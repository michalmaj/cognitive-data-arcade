# src/cognitive_data_arcade/games/anomaly_alert/phase_intro.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

_W, _H = 1024, 720
_BG = (15, 15, 35)
_PANEL = (18, 18, 42)
_WHITE = (240, 240, 240)
_DIM = (120, 120, 160)
_BLUE = (52, 152, 219)

_LINES = [
    "Wykrywanie anomalii w danych to kluczowa umiejetnosc analityczna.",
    "W kazdej z 6 rund zobaczysz inny typ wykresu.",
    "",
    "Kliknij lewym przyciskiem na punkty, ktore wygladaja podejrzanie.",
    "Kliknij ponownie, aby odznaczac. Zatwierdz wybor przyciskiem.",
    "",
    "Prawa mysz (PPM) na wykresie otwiera podpowiedz.",
    "Za kazde trafione 20 pkt, za falszywy alarm -5 pkt.",
    "Bonus +10 pkt za ukonczenie rundy w mniej niz 45 sekund.",
]


class PhaseIntroScene(Scene):
    def __init__(self) -> None:
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            self._advance()

    def _advance(self) -> None:
        from cognitive_data_arcade.games.anomaly_alert.phase_round import PhaseRoundScene
        from cognitive_data_arcade.games.anomaly_alert.scenarios import SCENARIOS

        self._next = PhaseRoundScene(
            scenario=SCENARIOS[0],
            round_idx=0,
            round_results=[],
        )
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(28).render("Anomaly Alert", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        y = 140
        for line in _LINES:
            if line:
                surf = get_font(16).render(line, True, _DIM)
                surface.blit(surf, (_W // 2 - surf.get_width() // 2, y))
            y += 34

        btn = pygame.Rect(_W // 2 - 130, _H - 90, 260, 50)
        pygame.draw.rect(surface, _PANEL, btn, border_radius=8)
        pygame.draw.rect(surface, _BLUE, btn, 2, border_radius=8)
        lbl = get_font(20).render("Zacznij gre", True, _BLUE)
        surface.blit(lbl, (_W // 2 - lbl.get_width() // 2, _H - 74))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

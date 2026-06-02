from __future__ import annotations

import math
from dataclasses import dataclass

import pygame

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

_BG = (13, 13, 30)
_LINE_COLOR = (42, 42, 80)
_ORANGE = (243, 156, 18)
_GOLD = _ORANGE  # same hue — is_game nodes use gold border, currently matches orange
_TEXT_LIGHT = (240, 240, 240)
_TEXT_DIM = (112, 112, 160)

_W, _H = 1024, 768
_TITLE_H = 40
_INFO_H = 60
_NET_TOP = _TITLE_H
_NET_H = _H - _TITLE_H - _INFO_H
_CX = _W // 2
_CY = _NET_TOP + _NET_H // 2

_R_L1 = 240  # orbit radius for L1 nodes
_R_L2 = 200  # orbit radius for L2 nodes
_CENTRE_R = 70
_L1_R = 60
_L2_R = 50


@dataclass(frozen=True)
class _Node:
    label: str  # display text — use "\n" for two lines
    description: str  # shown in info bar (1–2 sentences)
    color: tuple[int, int, int]
    is_game: bool = False  # True → gold border


_L1_NODES: list[_Node] = [
    _Node("fMRI\nEEG", "Neuroobrazowanie i sygnały elektryczne mózgu.", (39, 174, 96)),
    _Node("Czasy\nreakcji", "Pomiar prędkości procesów poznawczych.", (155, 89, 182)),
    _Node(
        "Eye\ntracking", "Śledzenie ruchu oczu ujawnia procesy uwagi.", (231, 76, 60)
    ),
    _Node("Mowa\nNLP", "Języki naturalne jako dane kognitywistyczne.", (26, 188, 156)),
    _Node(
        "Big Data\nkliniczna", "Medyczne zbiory danych na dużą skalę.", (230, 126, 34)
    ),
    _Node(
        "Digital\nphenotyp.",
        "Smartfon jako czujnik stanu psychicznego.",
        (52, 152, 219),
    ),
]

_L2_NODES: dict[str, list[_Node]] = {
    "fMRI\nEEG": [
        _Node(
            "Human\nConnectome",
            "Mapowanie połączeń między obszarami mózgu u 1200 osób; jeden z największych zbiorów danych neuroobrazowania.",
            (39, 174, 96),
        ),
        _Node(
            "OpenNeuro\n.org",
            "Otwarta platforma z tysiącami zestawów danych fMRI i EEG; dostępna bezpłatnie dla badaczy.",
            (39, 174, 96),
        ),
        _Node(
            "Brain-\nComputer",
            "Urządzenia odczytujące sygnały EEG w czasie rzeczywistym; zastosowania w medycynie i grach.",
            (39, 174, 96),
        ),
        _Node(
            "EEGLAB",
            "Środowisko do analizy sygnałów EEG; przetworzyło miliony godzin nagrań.",
            (39, 174, 96),
        ),
    ],
    "Czasy\nreakcji": [
        _Node(
            "Donders\n1868",
            "Pierwsze pomiary prędkości myślenia. Odejmowanie czasów reakcji wykazało, że decyzja zajmuje mózgowi wymierzalny czas.",
            (155, 89, 182),
        ),
        _Node(
            "Mental\nChronometry",
            "Dział psychologii mierzący czas procesów poznawczych; podstawa eksperymentalnej psychologii poznawczej.",
            (155, 89, 182),
        ),
        _Node(
            "Hick's\nLaw",
            "Im więcej opcji wyboru, tym dłuższy czas reakcji. Zależność logarytmiczna odkryta w 1952 roku.",
            (155, 89, 182),
        ),
        _Node(
            "RT Lab",
            "Aplikacja do pomiaru czasu prostej reakcji. Dostępna w menu jako lekcja 02.",
            (155, 89, 182),
            is_game=True,
        ),
        _Node(
            "Stroop\nChallenge",
            "Zadanie Stroopa mierzy czas reakcji w warunkach konfliktu poznawczego. Dostępne w menu jako lekcja 07.",
            (155, 89, 182),
            is_game=True,
        ),
    ],
    "Eye\ntracking": [
        _Node(
            "Tobii\nResearch",
            "Urządzenia do śledzenia ruchu oczu używane w badaniach uwagi wzrokowej i czytelnictwa.",
            (231, 76, 60),
        ),
        _Node(
            "Saccades &\nFixations",
            "Ruchy sakadyczne i fiksacje ujawniają, co i kiedy przyciąga uwagę. Typowy zapis to ~250 punktów/sekundę.",
            (231, 76, 60),
        ),
        _Node(
            "Visual\nSearch",
            "Badania przeszukiwania wzrokowego mierzą, jak szybko wykrywamy cel wśród dystraktorów.",
            (231, 76, 60),
        ),
        _Node(
            "Reading\nResearch",
            "Śledzenie oczu podczas czytania dostarcza danych o przetwarzaniu języka i trudności tekstów.",
            (231, 76, 60),
        ),
    ],
    "Mowa\nNLP": [
        _Node(
            "CHILDES\nCorpus",
            "Zbiór nagrań mowy dzieci z całego świata; podstawa badań nad przyswajaniem języka.",
            (26, 188, 156),
        ),
        _Node(
            "Common\nVoice",
            "Otwarty zbiór nagrań głosowych Mozilli; ponad 20 000 godzin w dziesiątkach języków.",
            (26, 188, 156),
        ),
        _Node(
            "Psycho-\nlingwistyka",
            "Bada, jak mózg przetwarza język; łączy eksperymenty behawioralne z analizą korpusów.",
            (26, 188, 156),
        ),
        _Node(
            "NKJP",
            "Narodowy Korpus Języka Polskiego; 1,8 miliarda słów z tekstów polskojęzycznych.",
            (26, 188, 156),
        ),
    ],
    "Big Data\nkliniczna": [
        _Node(
            "UK\nBiobank",
            "Dane medyczne i genetyczne 500 000 uczestników zbierane od 2006 roku w Wielkiej Brytanii.",
            (230, 126, 34),
        ),
        _Node(
            "ABCD\nStudy",
            "Największe długoterminowe badanie rozwoju mózgu u dzieci w USA; 11 800 uczestników.",
            (230, 126, 34),
        ),
        _Node(
            "Electronic\nHealth Rec.",
            "Elektroniczne rekordy medyczne zawierają miliardy wpisów; źródło danych dla epidemiologii poznawczej.",
            (230, 126, 34),
        ),
        _Node(
            "Longitudinal\nStudies",
            "Badania podłużne śledzą te same osoby przez lata; niezbędne do rozróżnienia zmian rozwojowych od chorobowych.",
            (230, 126, 34),
        ),
    ],
    "Digital\nphenotyp.": [
        _Node(
            "GPS &\nAccelerometer",
            "Smartfon rejestruje lokalizację i ruch; wzorce aktywności korelują ze stanem psychicznym.",
            (52, 152, 219),
        ),
        _Node(
            "Social Media\nPatterns",
            "Częstotliwość i treść wpisów w mediach społecznościowych jako wskaźnik nastroju i zachowania.",
            (52, 152, 219),
        ),
        _Node(
            "Keystroke\nDynamics",
            "Rytm pisania na klawiaturze pozwala wykryć zmęczenie poznawcze i zmiany nastroju.",
            (52, 152, 219),
        ),
        _Node(
            "Sleep\nPatterns",
            "Dane z czujników ruchu dokumentują jakość snu; powiązane z pamięcią i regulacją emocji.",
            (52, 152, 219),
        ),
    ],
}


def _node_positions(n: int, r: int) -> list[tuple[int, int]]:
    """n evenly-spaced positions on a circle of radius r centred at (_CX, _CY), starting at top."""
    positions = []
    for i in range(n):
        angle = math.pi / 2 + 2 * math.pi * i / n
        x = _CX + int(r * math.cos(angle))
        y = _CY - int(r * math.sin(angle))
        positions.append((x, y))
    return positions


def _lighten(color: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(min(255, c + 40) for c in color)  # type: ignore[return-value]


def _darken(color: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(max(0, c - 60) for c in color)  # type: ignore[return-value]


class BigDataMapGame(Scene):
    def __init__(self, strings: Strings, profile_manager: ProfileManager) -> None:
        self._strings = strings  # accepted for API consistency; unused in MVP
        self._pm = profile_manager
        self._in_l2: bool = False
        self._l1_idx: int = 0
        self._l2_idx: int = 0
        self._font_title = pygame.font.SysFont(None, 32)
        self._font_node = pygame.font.SysFont(None, 18)
        self._font_info = pygame.font.SysFont(None, 22)
        self._node_rects: list[pygame.Rect] = []

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            from cognitive_data_arcade.engine.mouse import hit
            for i, rect in enumerate(self._node_rects):
                if hit(rect, event.pos):
                    if self._in_l2:
                        self._l2_idx = i
                    else:
                        self._l1_idx = i
                    break
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            from cognitive_data_arcade.engine.mouse import hit
            for i, rect in enumerate(self._node_rects):
                if hit(rect, event.pos):
                    if self._in_l2:
                        self._l2_idx = i
                    else:
                        self._l1_idx = i
                        self._in_l2 = True
                        self._l2_idx = 0
                        audio.play_sfx("navigate")
                    break
            return
        if event.type != pygame.KEYDOWN:
            return
        key = event.key
        if self._in_l2:
            l2_nodes = _L2_NODES[_L1_NODES[self._l1_idx].label]
            n = len(l2_nodes)
            if key in (pygame.K_UP, pygame.K_RIGHT):
                self._l2_idx = (self._l2_idx - 1) % n
            elif key in (pygame.K_DOWN, pygame.K_LEFT):
                self._l2_idx = (self._l2_idx + 1) % n
            elif key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_BACKSPACE):
                self._in_l2 = False
                audio.play_sfx("navigate")
        else:
            n = len(_L1_NODES)
            if key in (pygame.K_UP, pygame.K_RIGHT):
                self._l1_idx = (self._l1_idx - 1) % n
            elif key in (pygame.K_DOWN, pygame.K_LEFT):
                self._l1_idx = (self._l1_idx + 1) % n
            elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._in_l2 = True
                self._l2_idx = 0
                audio.play_sfx("navigate")

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_title(surface)
        if self._in_l2:
            self._draw_l2_network(surface)
        else:
            self._draw_l1_network(surface)
        self._draw_info_bar(surface)

    def _draw_title(self, surface: pygame.Surface) -> None:
        rendered = self._font_title.render("Big Data w Kognitywistyce", True, _ORANGE)
        surface.blit(rendered, (16, (_TITLE_H - rendered.get_height()) // 2))

    def _draw_l1_network(self, surface: pygame.Surface) -> None:
        positions = _node_positions(len(_L1_NODES), _R_L1)
        self._node_rects = [
            pygame.Rect(x - _L1_R, y - _L1_R, _L1_R * 2, _L1_R * 2)
            for x, y in positions
        ]
        for pos in positions:
            pygame.draw.line(surface, _LINE_COLOR, (_CX, _CY), pos, 2)
        self._draw_circle_node(
            surface,
            (_CX, _CY),
            _CENTRE_R,
            _ORANGE,
            "Big Data\nw nauce",
            highlighted=False,
            is_game=False,
        )
        for i, (node, pos) in enumerate(zip(_L1_NODES, positions)):
            self._draw_circle_node(
                surface,
                pos,
                _L1_R,
                node.color,
                node.label,
                highlighted=(i == self._l1_idx),
                is_game=node.is_game,
            )

    def _draw_l2_network(self, surface: pygame.Surface) -> None:
        l1_node = _L1_NODES[self._l1_idx]
        l2_nodes = _L2_NODES[l1_node.label]
        positions = _node_positions(len(l2_nodes), _R_L2)
        self._node_rects = [
            pygame.Rect(x - _L2_R, y - _L2_R, _L2_R * 2, _L2_R * 2)
            for x, y in positions
        ]
        for pos in positions:
            pygame.draw.line(surface, _LINE_COLOR, (_CX, _CY), pos, 2)
        self._draw_circle_node(
            surface,
            (_CX, _CY),
            _CENTRE_R,
            l1_node.color,
            l1_node.label,
            highlighted=False,
            is_game=False,
        )
        for i, (node, pos) in enumerate(zip(l2_nodes, positions)):
            self._draw_circle_node(
                surface,
                pos,
                _L2_R,
                node.color,
                node.label,
                highlighted=(i == self._l2_idx),
                is_game=node.is_game,
            )

    def _draw_circle_node(
        self,
        surface: pygame.Surface,
        center: tuple[int, int],
        radius: int,
        color: tuple[int, int, int],
        label: str,
        *,
        highlighted: bool,
        is_game: bool,
    ) -> None:
        fill = _lighten(color) if highlighted else _darken(color)
        border = _GOLD if is_game else color
        border_w = 3 if is_game else 2
        pygame.draw.circle(surface, fill, center, radius)
        pygame.draw.circle(surface, border, center, radius, border_w)
        lines = label.split("\n")
        line_h = self._font_node.get_height() + 1
        y = center[1] - (len(lines) * line_h) // 2
        for line in lines:
            text_color = (255, 255, 255) if highlighted else color
            rendered = self._font_node.render(line, True, text_color)
            surface.blit(rendered, (center[0] - rendered.get_width() // 2, y))
            y += line_h

    def _draw_info_bar(self, surface: pygame.Surface) -> None:
        bar_y = _H - _INFO_H
        pygame.draw.rect(surface, (8, 8, 20), (0, bar_y, _W, _INFO_H))
        pygame.draw.line(surface, (26, 26, 58), (0, bar_y), (_W, bar_y), 1)
        if self._in_l2:
            node = _L2_NODES[_L1_NODES[self._l1_idx].label][self._l2_idx]
            hint = "ENTER / BACKSPACE — wróć  |  ESC — pauza"
        else:
            node = _L1_NODES[self._l1_idx]
            hint = "ENTER — rozwiń  |  ESC — pauza"
        rendered = self._font_info.render(node.description, True, _TEXT_LIGHT)
        surface.blit(rendered, (16, bar_y + 8))
        rendered_hint = self._font_info.render(hint, True, _TEXT_DIM)
        surface.blit(rendered_hint, (16, bar_y + 8 + self._font_info.get_height() + 4))

    def is_done(self) -> bool:
        return False

    def next_scene(self) -> Scene | None:
        return None

from __future__ import annotations

import math  # noqa: F401 # used by _node_positions in Task 2
from dataclasses import dataclass

import pygame  # noqa: F401

from cognitive_data_arcade.engine.i18n import Strings  # noqa: F401
from cognitive_data_arcade.engine.scene import Scene  # noqa: F401
from cognitive_data_arcade.profile.manager import ProfileManager  # noqa: F401

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

_R_L1 = 240   # orbit radius for L1 nodes
_R_L2 = 200   # orbit radius for L2 nodes
_CENTRE_R = 70
_L1_R = 60
_L2_R = 50


@dataclass(frozen=True)
class _Node:
    label: str            # display text — use "\n" for two lines
    description: str      # shown in info bar (1–2 sentences)
    color: tuple[int, int, int]
    is_game: bool = False  # True → gold border


_L1_NODES: list[_Node] = [
    _Node("fMRI\nEEG", "Neuroobrazowanie i sygnały elektryczne mózgu.", (39, 174, 96)),
    _Node("Czasy\nreakcji", "Pomiar prędkości procesów poznawczych.", (155, 89, 182)),
    _Node("Eye\ntracking", "Śledzenie ruchu oczu ujawnia procesy uwagi.", (231, 76, 60)),
    _Node("Mowa\nNLP", "Języki naturalne jako dane kognitywistyczne.", (26, 188, 156)),
    _Node("Big Data\nkliniczna", "Medyczne zbiory danych na dużą skalę.", (230, 126, 34)),
    _Node("Digital\nphenotyp.", "Smartfon jako czujnik stanu psychicznego.", (52, 152, 219)),
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

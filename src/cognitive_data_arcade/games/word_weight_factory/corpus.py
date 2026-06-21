from __future__ import annotations
from dataclasses import dataclass

PRESET_STROOP_PL = (
    "Efekt Stroopa: czas reakcji wzrasta gdy kolor czcionki nie zgadza sie "
    "z nazwa koloru. Interferencja kolorow spowalnia przetwarzanie informacji. "
    "Czas reakcji jest kluczowym wskaznikiem w psychologii poznawczej. "
    "Badania pokazuja ze roznica wynosi okolo 100 do 200 milisekund. "
    "Efekt ten demonstruje automatyczne przetwarzanie slow przez mozg."
)
PRESET_NBACK_EN = (
    "The N-back task measures working memory capacity. Participants monitor "
    "a sequence of stimuli and respond when the current stimulus matches the one "
    "presented N steps earlier. Reaction time increases with higher N levels. "
    "Working memory capacity predicts fluid intelligence and cognitive performance. "
    "The task is widely used in cognitive neuroscience research."
)
PRESET_FLANKER_PL = (
    "Efekt Flankera: czas reakcji wzrasta gdy flankery sa niezgodne z bodzcem "
    "centralnym. Hamowanie odpowiedzi to kluczowy mechanizm kontroli poznawczej. "
    "Czas reakcji jest szybszy dla bodzcow kongruentnych niz niekongruentnych. "
    "Roznica w czasie reakcji wynosi typowo 50 do 100 milisekund. "
    "Efekt Flankera mierzy zdolnosc do selektywnej uwagi."
)
PRESET_MEMORY_EN = (
    "Memory encoding depends on depth of processing. Semantic encoding produces "
    "stronger memory traces than shallow encoding. Working memory capacity limits "
    "the amount of information held in mind at one time. "
    "Deep processing involves meaning and context rather than surface features. "
    "Retrieval success depends on the match between encoding and retrieval conditions."
)

# (title, text, lang) — lang used for stop-word removal
_PRESETS: list[tuple[str, str, str]] = [
    ("Stroop PL", PRESET_STROOP_PL, "pl"),
    ("N-Back EN", PRESET_NBACK_EN, "en"),
    ("Flanker PL", PRESET_FLANKER_PL, "pl"),
    ("Memory EN", PRESET_MEMORY_EN, "en"),
]


@dataclass
class CorpusState:
    selected_idx: int = 0  # which doc row is highlighted
    custom_text: str = ""
    lang: str = "pl"  # PL/EN toggle (custom mode) + stop-word lang
    lowercase: bool = True
    rm_punct: bool = True
    rm_stops: bool = False

    def active_docs(self) -> list[tuple[str, str]]:
        """Return (title, text) for all active documents."""
        result = [(title, text) for title, text, _ in _PRESETS]
        if self.custom_text.strip():
            result.append(("Wlasny", self.custom_text))
        return result

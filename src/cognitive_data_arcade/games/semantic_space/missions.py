from __future__ import annotations

from dataclasses import dataclass, field

from cognitive_data_arcade.games.semantic_space.word_data import ANALOGIES, BRIDGE_WORDS


@dataclass
class Mission:
    type: str               # "neighbors" | "odd_one_out" | "bridge" | "analogy"
    target: str             # WORDS key; "" for analogy
    answers: list[str]      # correct word key(s); display string for analogy
    distractors: list[str]  # wrong options: WORDS keys or display strings
    hint_pl: str
    hint_en: str
    difficulty: int         # 1=easy, 2=medium, 3=hard
    formula: str = field(default="")  # "A – B + C = ?" for analogy missions only


def build_session() -> list[Mission]:
    """Return fixed sequence of 8 missions, difficulty 1->3."""
    return [
        # 1. neighbors easy — radosc, 3 closest in emocje
        Mission(
            type="neighbors",
            target="radosc",
            answers=["szczescie", "milosc", "nadzieja"],
            distractors=[],
            hint_pl="Slowa blisko siebie w przestrzeni = podobne znaczenie.",
            hint_en="Words close in space = similar meaning.",
            difficulty=1,
        ),
        # 2. odd_one_out easy — 3 emocje + 1 zwierzeta
        Mission(
            type="odd_one_out",
            target="",
            answers=["kot"],
            distractors=["radosc", "smutek", "gniew"],
            hint_pl="Jedno slowo pochodzi z zupelnie innej kategorii.",
            hint_en="One word belongs to a completely different category.",
            difficulty=1,
        ),
        # 3. neighbors medium — mecz, boundary of sport/nauka
        Mission(
            type="neighbors",
            target="mecz",
            answers=["druzyna", "zwyciestwo", "tenis"],
            distractors=[],
            hint_pl="Na granicy klastra — szukaj slow w podobnym kontekscie uzycia.",
            hint_en="Near a cluster boundary — look for words used in similar contexts.",
            difficulty=2,
        ),
        # 4. odd_one_out medium — 3 sport + 1 jedzenie (both concrete)
        Mission(
            type="odd_one_out",
            target="",
            answers=["chleb"],
            distractors=["pilka", "mecz", "tenis"],
            hint_pl="Trzy slowa z tej samej dziedziny — czwarte jest intruzem.",
            hint_en="Three words from the same domain — one is an intruder.",
            difficulty=2,
        ),
        # 5. bridge medium — wynik (sport + nauka)
        Mission(
            type="bridge",
            target=BRIDGE_WORDS[0][0],   # "wynik"
            answers=[BRIDGE_WORDS[0][0]],
            distractors=[],
            hint_pl="Szukaj slowa, ktore pasuje do dwoch roznych klastrow jednoczesnie.",
            hint_en="Find a word that fits two different clusters at once.",
            difficulty=2,
        ),
        # 6. bridge hard — druzyna (sport + emocje)
        Mission(
            type="bridge",
            target=BRIDGE_WORDS[3][0],   # "druzyna"
            answers=[BRIDGE_WORDS[3][0]],
            distractors=[],
            hint_pl="To slowo laczy dyscypline sportu z dynamika emocji grupowych.",
            hint_en="This word connects sport with group emotion dynamics.",
            difficulty=3,
        ),
        # 7. analogy medium — pies:szczenie = kot:kotek
        Mission(
            type="analogy",
            target="",
            answers=[ANALOGIES[1][3]],      # "kotek"
            distractors=list(ANALOGIES[1][4]),
            hint_pl=ANALOGIES[1][5],
            hint_en=ANALOGIES[1][6],
            difficulty=2,
            formula=f"{ANALOGIES[1][0]} – {ANALOGIES[1][1]} + {ANALOGIES[1][2]} = ?",
        ),
        # 8. analogy hard — radosc:szczescie = smutek:zal
        Mission(
            type="analogy",
            target="",
            answers=[ANALOGIES[3][3]],      # "zal"
            distractors=list(ANALOGIES[3][4]),
            hint_pl=ANALOGIES[3][5],
            hint_en=ANALOGIES[3][6],
            difficulty=3,
            formula=f"{ANALOGIES[3][0]} – {ANALOGIES[3][1]} + {ANALOGIES[3][2]} = ?",
        ),
    ]

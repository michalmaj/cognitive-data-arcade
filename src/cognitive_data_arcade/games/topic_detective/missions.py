from __future__ import annotations

from dataclasses import dataclass

from cognitive_data_arcade.games.topic_detective.topic_data import DOCUMENTS, INTRUDER_SETS, TOPICS


@dataclass
class Mission:
    type: str  # "name_topic" | "assign_doc" | "intruder"
    answer: str  # correct topic key (name_topic/assign_doc) or intruder word (intruder)
    payload: dict[str, object]
    hint_pl: str
    hint_en: str
    difficulty: int


def build_session() -> list[Mission]:
    """Return 8 missions: 3 name_topic + 3 assign_doc + 2 intruder, difficulty 1->3."""
    return [
        # name_topic x 3 (difficulty 1, 1, 2)
        Mission(
            type="name_topic",
            answer="sport",
            payload={"top5_words": TOPICS["sport"]["words"][:5], "topic_key": "sport"},
            hint_pl="Slowa zwiazane z rywalizacja, zawodami i rekordami -- to ten temat.",
            hint_en="Words related to competition, events, and records -- that's this topic.",
            difficulty=1,
        ),
        Mission(
            type="name_topic",
            answer="zdrowie",
            payload={"top5_words": TOPICS["zdrowie"]["words"][:5], "topic_key": "zdrowie"},
            hint_pl="Cialo, medycyna i profilaktyka -- odcisk palca tego tematu jest jasny.",
            hint_en="Body, medicine, and prevention -- this topic's fingerprint is clear.",
            difficulty=1,
        ),
        Mission(
            type="name_topic",
            answer="tech",
            payload={"top5_words": TOPICS["tech"]["words"][:5], "topic_key": "tech"},
            hint_pl="Ten temat lezy blisko Nauki -- porownaj odciski palcow w panelu bocznym.",
            hint_en="This topic sits close to Science -- compare fingerprints in the side panel.",
            difficulty=2,
        ),
        # assign_doc x 3 (difficulty 1, 2, 2)
        Mission(
            type="assign_doc",
            answer=DOCUMENTS[0]["dominant"],
            payload={
                "text_pl": DOCUMENTS[0]["text_pl"],
                "weights": DOCUMENTS[0]["weights"],
                "dominant": DOCUMENTS[0]["dominant"],
            },
            hint_pl="Szukaj slow kluczowych pasujacych do odciskow palcow w panelu.",
            hint_en="Look for key words matching the fingerprints in the side panel.",
            difficulty=1,
        ),
        Mission(
            type="assign_doc",
            answer=DOCUMENTS[3]["dominant"],
            payload={
                "text_pl": DOCUMENTS[3]["text_pl"],
                "weights": DOCUMENTS[3]["weights"],
                "dominant": DOCUMENTS[3]["dominant"],
            },
            hint_pl="Dokument moze zawierac slowa z wielu tematow -- wybierz dominujacy.",
            hint_en="A document may contain words from many topics -- pick the dominant one.",
            difficulty=2,
        ),
        Mission(
            type="assign_doc",
            answer=DOCUMENTS[12]["dominant"],
            payload={
                "text_pl": DOCUMENTS[12]["text_pl"],
                "weights": DOCUMENTS[12]["weights"],
                "dominant": DOCUMENTS[12]["dominant"],
            },
            hint_pl="Sztuczna inteligencja i nauka to bliskie tematy. Porownaj odciski palcow.",
            hint_en="AI and science are close topics. Compare their fingerprints carefully.",
            difficulty=2,
        ),
        # intruder x 2 (difficulty 2, 3)
        Mission(
            type="intruder",
            answer=INTRUDER_SETS[0]["intruder"],
            payload={
                "topic_key": INTRUDER_SETS[0]["topic"],
                "all_words": INTRUDER_SETS[0]["words"] + [INTRUDER_SETS[0]["intruder"]],
            },
            hint_pl="Jedno slowo pochodzi z innego tematu. Porownaj z odciskiem w panelu.",
            hint_en="One word belongs to a different topic. Compare with the fingerprint panel.",
            difficulty=2,
        ),
        Mission(
            type="intruder",
            answer=INTRUDER_SETS[2]["intruder"],
            payload={
                "topic_key": INTRUDER_SETS[2]["topic"],
                "all_words": INTRUDER_SETS[2]["words"] + [INTRUDER_SETS[2]["intruder"]],
            },
            hint_pl="Nauka i polityka -- nie tak odlegle jak myslisz. Szukaj slowa bez kontekstu naukowego.",
            hint_en="Science and politics -- not as distant as you'd think. Find the word out of scientific context.",
            difficulty=3,
        ),
    ]

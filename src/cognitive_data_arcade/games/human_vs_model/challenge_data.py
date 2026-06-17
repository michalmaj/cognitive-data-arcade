from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ClassifyChallenge:
    text: str
    options: list[str]
    answer: str
    model_answer: str
    explanation: str
    difficulty: int


@dataclass
class DetectChallenge:
    human_text: str
    ai_text: str
    explanation: str
    difficulty: int


@dataclass
class CompleteChallenge:
    stem: str
    options: list[str]
    answer: str
    model_answer: str
    explanation: str
    difficulty: int


CLASSIFY_CHALLENGES: list[ClassifyChallenge] = [
    ClassifyChallenge(
        text="To nie byl zly film.",
        options=["Pozytywny", "Negatywny", "Neutralny"],
        answer="Pozytywny",
        model_answer="Negatywny",
        explanation="AI myli sie na negacji: 'nie byl zly' znaczy 'byl dobry'.",
        difficulty=1,
    ),
    ClassifyChallenge(
        text="No jasne, wszyscy to uwielbiaja...",
        options=["Pozytywny", "Negatywny", "Neutralny"],
        answer="Negatywny",
        model_answer="Pozytywny",
        explanation="AI nie wykrywa sarkazmu -- 'wszyscy uwielbiaja' to ironiczne narzekanie.",
        difficulty=1,
    ),
    ClassifyChallenge(
        text="Mimo kilku bledow projekt byl naprawde udany.",
        options=["Pozytywny", "Negatywny", "Neutralny"],
        answer="Pozytywny",
        model_answer="Pozytywny",
        explanation="AI i czlowiek zgadzaja sie -- 'naprawde udany' to wyrazny sygnal pozytywny.",
        difficulty=1,
    ),
]

DETECT_CHALLENGES: list[DetectChallenge] = [
    DetectChallenge(
        human_text="Wczoraj totalnie olalem egzamin bo zasnalem. Klasyka. Nie wiem co mi odbilo.",
        ai_text="Nieobecnosc na egzaminie moze wynikac z roznych przyczyn, takich jak choroba lub nieprzewidziane zdarzenia.",
        explanation="Czlowiek: slang, osobisty ton, krotkie zdania. AI: formalne, ogolne, brak kontekstu.",
        difficulty=2,
    ),
    DetectChallenge(
        human_text="Ten film byl okropny, wyszlam po pol godziny i nie zaluje. Zmarnowane kase.",
        ai_text="Film nie spelnil oczekiwan widzow pod wzgledem scenariusza i realizacji technicznej.",
        explanation="Czlowiek: emocje, osobiste doswiadczenie, jezyk potoczny. AI: neutralny, brak emocji.",
        difficulty=2,
    ),
    DetectChallenge(
        human_text="Chyba nie da sie bardziej spac na wykladzie? A ty co -- notatki piszesz??",
        ai_text="Aktywne uczestnictwo w zajeciach akademickich pozytywnie wplywa na wyniki nauczania.",
        explanation="Czlowiek: pytanie retoryczne, sarkazm wobec znajomego. AI: ogolna prawda, brak osoby.",
        difficulty=2,
    ),
]

COMPLETE_CHALLENGES: list[CompleteChallenge] = [
    CompleteChallenge(
        stem="Po dlugim maratonie zawodnik byl tak zmeczony, ze...",
        options=[
            "zasnal przy mecie",
            "zjadl kolacje",
            "pobiegl dalej",
            "zadzwonil do mamy",
        ],
        answer="zasnal przy mecie",
        model_answer="zjadl kolacje",
        explanation="AI wybiera przewidywalne 'zjadl kolacje'. Czlowiek wybiera humorystyczne 'zasnal przy mecie'.",
        difficulty=3,
    ),
    CompleteChallenge(
        stem="Kiedy powiedzialem mu prawde, on...",
        options=[
            "wyszedl jak burza",
            "uslyszal moje slowa",
            "odpowiedzial ze spokojem",
            "przetworzy informacje",
        ],
        answer="wyszedl jak burza",
        model_answer="odpowiedzial ze spokojem",
        explanation="AI pomija idiom 'wyszedl jak burza'. Czlowiek rozumie ze to naturalne dramatyczne zakonczenie.",
        difficulty=3,
    ),
    CompleteChallenge(
        stem="Na weselu cioci Haliny wszyscy tancowali, tylko stryj Heniek...",
        options=[
            "siedzial przy barze",
            "uczestniczyl w uroczystosci",
            "wyrabal figury",
            "poruszal sie rytmicznie",
        ],
        answer="siedzial przy barze",
        model_answer="uczestniczyl w uroczystosci",
        explanation="AI nie zna polskiego kontekstu weselnego. 'Siedzial przy barze' to obrazek z zycia.",
        difficulty=3,
    ),
]

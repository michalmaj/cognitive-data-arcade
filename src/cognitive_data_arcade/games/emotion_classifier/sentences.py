# src/cognitive_data_arcade/games/emotion_classifier/sentences.py
from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Sentence:
    text: str
    trap: str          # "clear_pos"|"clear_neg"|"negation"|"intensity"|"irony"|"mixed"
    word_scores: dict[str, int]   # lexicon scores for words in THIS sentence
    truth: str         # "positive"|"negative"|"neutral"|"mixed"
    explanation: str   # shown in PhaseRoundResult


SENTENCE_BANK: list[Sentence] = [
    # ── clear_pos ──────────────────────────────────────────────────────────────
    Sentence(
        "Wyniki testu były znakomite i wszyscy byli zadowoleni.",
        "clear_pos", {"znakomite": 2, "zadowoleni": 1}, "positive",
        "Leksykon trafnie wykrył dwa pozytywne słowa. To łatwy przypadek.",
    ),
    Sentence(
        "Eksperyment zakończył się sukcesem i wyniki były doskonale.",
        "clear_pos", {"sukcesem": 2, "doskonale": 2}, "positive",
        "Dwa silnie pozytywne słowa. Klasyfikator nie miał problemów.",
    ),
    Sentence(
        "Metoda okazała się rewelacyjna i przyniosła doskonale rezultaty.",
        "clear_pos", {"rewelacyjna": 2, "doskonale": 2}, "positive",
        "Leksykon ma oba słowa i poprawnie ocenia sentyment.",
    ),
    Sentence(
        "Uczestnicy wykonali zadanie szybko i poprawnie.",
        "clear_pos", {"szybko": 1, "poprawnie": 1}, "positive",
        "Dwa łagodnie pozytywne słowa. Suma wag = +2.",
    ),
    Sentence(
        "Wyniki są pozytywne i potwierdzają nasze hipotezy.",
        "clear_pos", {"pozytywne": 1}, "positive",
        "Jedno kluczowe słowo wystarczy dla poprawnej klasyfikacji.",
    ),
    Sentence(
        "Czas reakcji był dobry a dokładność była wysoka.",
        "clear_pos", {"dobry": 1}, "positive",
        "Słowo 'dobry' wskazuje na pozytywny sentyment.",
    ),
    Sentence(
        "Badani byli zadowoleni z przebiegu eksperymentu.",
        "clear_pos", {"zadowoleni": 1}, "positive",
        "Jedno pozytywne słowo wystarczyło leksykonowi.",
    ),
    Sentence(
        "Wynik jest fantastyczny -- rekord pobity.",
        "clear_pos", {"fantastyczny": 2}, "positive",
        "Silnie pozytywne słowo. Leksykon nie mógł się pomylić.",
    ),
    Sentence(
        "Nowe podejście okazało się trafne i użyteczne.",
        "clear_pos", {"trafne": 1, "użyteczne": 1}, "positive",
        "Dwa umiarkowanie pozytywne słowa. Suma = +2.",
    ),
    Sentence(
        "Model działa świetnie na danych testowych.",
        "clear_pos", {"świetnie": 2}, "positive",
        "Jedno silnie pozytywne słowo. Klasyfikacja oczywista.",
    ),
    # ── clear_neg ──────────────────────────────────────────────────────────────
    Sentence(
        "Eksperyment zakończył się porażka i wyniki były fatalne.",
        "clear_neg", {"porażka": -2, "fatalne": -2}, "negative",
        "Dwa silnie negatywne słowa. Leksykon nie miał problemów.",
    ),
    Sentence(
        "Czas reakcji był powolny i popełniono wiele błędów.",
        "clear_neg", {"powolny": -1, "błędów": -1}, "negative",
        "Dwa łagodnie negatywne słowa. Suma = -2.",
    ),
    Sentence(
        "Wyniki są koszmarnie słabe i nie nadają się do analizy.",
        "clear_neg", {"koszmarnie": -2, "słabe": -1}, "negative",
        "Silne i łagodne ujemne słowo. Leksykon to widzi.",
    ),
    Sentence(
        "Metoda okazała się bezużyteczna w tym kontekście.",
        "clear_neg", {"bezużyteczna": -2}, "negative",
        "Jedno mocno negatywne słowo. Klasyfikacja oczywista.",
    ),
    Sentence(
        "Badanie zakończyło się klapa -- hipoteza obalona.",
        "clear_neg", {"klapa": -2}, "negative",
        "Słowo 'klapa' to silny sygnał negatywny.",
    ),
    Sentence(
        "Uczestnicy byli rozczarowani wynikami sesji.",
        "clear_neg", {"rozczarowani": -1}, "negative",
        "Jedno negatywne słowo. Leksykon rozpoznał nastrój.",
    ),
    Sentence(
        "Algorytm działa tragicznie i błędna klasyfikacja w każdej próbie.",
        "clear_neg", {"tragicznie": -2, "błędna": -1}, "negative",
        "Dwa negatywne słowa. Suma = -3.",
    ),
    Sentence(
        "Wyniki są fatalne i wymagają poważnych poprawek.",
        "clear_neg", {"fatalne": -2}, "negative",
        "Jedno silnie negatywne słowo. Jasny przypadek.",
    ),
    Sentence(
        "Eksperyment był trudny i zakończył się porażka.",
        "clear_neg", {"trudny": -1, "porażka": -2}, "negative",
        "Dwa negatywne słowa. Leksykon sklasyfikował poprawnie.",
    ),
    Sentence(
        "Próbki były słabe jakościowo i przysparzały problemów.",
        "clear_neg", {"słabe": -1, "problemów": -1}, "negative",
        "Dwa łagodnie negatywne słowa. Suma = -2.",
    ),
    # ── negation ───────────────────────────────────────────────────────────────
    Sentence(
        "Badani nie wyrazili zadowolenia z przebiegu sesji.",
        "negation", {"zadowolenia": 1}, "negative",
        "Leksykon widzi 'zadowolenia' (+1) i mówi POZYTYWNY. Ale 'nie' odwraca sens.",
    ),
    Sentence(
        "Wyniki nie były fatalne, ale pozostawiły wiele do życzenia.",
        "negation", {"fatalne": -2}, "negative",
        "Leksykon widzi 'fatalne' (-2) i mówi NEGATYWNY. Ale 'nie fatalne' to coś innego.",
    ),
    Sentence(
        "Metoda nie okazała się tak użyteczna jak oczekiwano.",
        "negation", {"użyteczna": 1}, "negative",
        "Leksykon widzi 'użyteczna' (+1) = POZYTYWNY. 'Nie tak użyteczna' to ograniczenie.",
    ),
    Sentence(
        "Nikt nie powiedział, że wyniki są pozytywne.",
        "negation", {"pozytywne": 1}, "negative",
        "Leksykon wykrywa 'pozytywne' i mówi POZYTYWNY. Całość obraca sens.",
    ),
    Sentence(
        "Uczestnicy nie wskazywali na trudności w zadaniu.",
        "negation", {"trudności": -1}, "positive",
        "Leksykon widzi 'trudności' (-1) = NEGATYWNY. 'Nie wskazywali na trudności' to dobra wiadomość.",
    ),
    Sentence(
        "Eksperyment nie skończył się sukcesem.",
        "negation", {"sukcesem": 2}, "negative",
        "Leksykon wykrywa 'sukcesem' (+2) = POZYTYWNY. Ale to opis porażki.",
    ),
    Sentence(
        "Wyniki nie są tak doskonale jak prezentowano.",
        "negation", {"doskonale": 2}, "negative",
        "Leksykon widzi 'doskonale' (+2) = POZYTYWNY. To krytyka, nie chwała.",
    ),
    Sentence(
        "Nie popełniono żadnych błędów podczas sesji.",
        "negation", {"błędów": -1}, "positive",
        "Leksykon widzi 'błędów' (-1) = NEGATYWNY. 'Nie popełniono błędów' = dobry wynik.",
    ),
    Sentence(
        "Dane nie wykazują żadnych problemów z jakością.",
        "negation", {"problemów": -1}, "positive",
        "Leksykon wykrywa 'problemów' (-1). Ale brak problemów to dobra wiadomość.",
    ),
    Sentence(
        "Model nie wypadł słabo na zbiorze testowym.",
        "negation", {"słabo": -1}, "positive",
        "Leksykon widzi 'słabo' (-1) = NEGATYWNY. 'Nie wypadł słabo' = wypadł dobrze.",
    ),
    Sentence(
        "Hipoteza nie została potwierdzona -- wyniki są rozczarowujące.",
        "negation", {"rozczarowujące": -1}, "negative",
        "Tu 'nie' dotyczy hipotezy, a 'rozczarowujące' potwierdza negatywny sentyment.",
    ),
    Sentence(
        "Czas reakcji był dobry, choć nie idealny.",
        "negation", {"dobry": 1}, "neutral",
        "Leksykon widzi 'dobry' (+1) = POZYTYWNY. 'Nie idealny' sugeruje ograniczenia.",
    ),
    # ── intensity ──────────────────────────────────────────────────────────────
    Sentence(
        "Wyniki są nieźle, ale mogłoby być lepiej.",
        "intensity", {"nieźle": 1}, "neutral",
        "Leksykon mówi POZYTYWNY za 'nieźle'. Ale 'mogłoby być lepiej' sygnalizuje średniość.",
    ),
    Sentence(
        "Dokładność modelu jest poprawna, choć nie imponujące.",
        "intensity", {"poprawna": 1, "imponujące": 2}, "neutral",
        "Leksykon sumuje +1+2 = POZYTYWNY. Ale 'nie imponujące' to korekta w dół.",
    ),
    Sentence(
        "Wydajność systemu jest dobra, lecz świetna nie jest.",
        "intensity", {"dobra": 1, "świetna": 2}, "neutral",
        "Leksykon sumuje +1+2 = POZYTYWNY. Ale 'świetna nie jest' to negacja intensywności.",
    ),
    Sentence(
        "Rezultaty są pozytywne, ale nie spektakularne.",
        "intensity", {"pozytywne": 1}, "neutral",
        "Leksykon mówi POZYTYWNY. Ale 'nie spektakularne' silnie obniża ocenę.",
    ),
    Sentence(
        "Sesja przebiegła w miarę sprawnie, z drobnymi błędami.",
        "intensity", {"błędami": -1}, "neutral",
        "'Drobnymi błędami' to łagodna krytyka. Leksykon widzi tylko 'błędami' (-1).",
    ),
    Sentence(
        "Wyniki są w porządku, choć doskonale to nie jest.",
        "intensity", {"doskonale": 2}, "neutral",
        "Leksykon widzi 'doskonale' (+2) = POZYTYWNY. 'Doskonale to nie jest' obniża ocenę.",
    ),
    Sentence(
        "Eksperyment przebiegł ani doskonale ani fatalnie.",
        "intensity", {"doskonale": 2, "fatalnie": -2}, "neutral",
        "Leksykon sumuje 2+(-2) = 0 = NEUTRALNY. Trafił -- ale to zbieg okoliczności.",
    ),
    Sentence(
        "Model jest nieźły, zdecydowanie nie genialny.",
        "intensity", {"nieźły": 1, "genialny": 2}, "neutral",
        "Leksykon sumuje +1+2 = POZYTYWNY. 'Nie genialny' to wyraźna korekta w dół.",
    ),
    Sentence(
        "Uczestnicy wyrazili łagodne zadowolenie z zadania.",
        "intensity", {"zadowolenie": 1}, "positive",
        "Słowo 'łagodne' obniża intensywność zadowolenia. Leksykon nie rozumie stopniowania.",
    ),
    Sentence(
        "Czas reakcji był dobry, choć nie doskonały.",
        "intensity", {"dobry": 1, "doskonały": 2}, "positive",
        "Leksykon sumuje +1+2 = POZYTYWNY. Ale 'nie doskonały' opisuje ograniczenie.",
    ),
    # ── irony ──────────────────────────────────────────────────────────────────
    Sentence(
        "Świetna robota -- kolejny błąd w danych, brawo.",
        "irony", {"świetna": 2, "błąd": -1, "brawo": 1}, "negative",
        "Leksykon widzi 'świetna' (+2), 'błąd' (-1), 'brawo' (+1) = +2 = POZYTYWNY. To ironia -- sens jest negatywny.",
    ),
    Sentence(
        "No brawo, znowu zepsuliśmy eksperyment przez nieuwagę.",
        "irony", {"brawo": 1}, "negative",
        "Leksykon wykrywa 'brawo' (+1) = POZYTYWNY. To sarkastyczna krytyka.",
    ),
    Sentence(
        "Doskonały wynik -- pomyliliśmy grupę kontrolną i eksperymentalną.",
        "irony", {"doskonały": 2}, "negative",
        "Leksykon mówi POZYTYWNY. W rzeczywistości to błąd metodologiczny.",
    ),
    Sentence(
        "Genialne podejście -- użyto nieodpowiedniego testu statystycznego.",
        "irony", {"genialne": 2}, "negative",
        "Leksykon raduje się 'genialne' (+2). To sarkazm -- sens jest negatywny.",
    ),
    Sentence(
        "Świetnie -- 90 procent danych utracono przez awarię dysku.",
        "irony", {"świetnie": 2}, "negative",
        "Leksykon widzi 'świetnie' i klaszcze. To ironia wobec katastrofy.",
    ),
    Sentence(
        "Fantastyczna precyzja -- pomiar z błędem trzykrotnie przekraczającym wartość.",
        "irony", {"fantastyczna": 2}, "negative",
        "Leksykon wykrywa 'fantastyczna' (+2) = POZYTYWNY. Sarkastyczny komentarz do błędu.",
    ),
    Sentence(
        "Imponujące tempo -- projekt opóźniony o pół roku.",
        "irony", {"imponujące": 2}, "negative",
        "Leksykon widzi 'imponujące' (+2). Kontekst: opóźnienie projektu. To ironia.",
    ),
    Sentence(
        "Rewelacyjny wynik -- p-value wynosi 0,7.",
        "irony", {"rewelacyjny": 2}, "negative",
        "Leksykon klaszcze w 'rewelacyjny' (+2). p=0.7 to wynik bez znaczenia.",
    ),
    Sentence(
        "No to pozytywnie -- hipoteza odrzucona po pięciu miesiącach badań.",
        "irony", {"pozytywnie": 1}, "negative",
        "Leksykon widzi 'pozytywnie' (+1). Kontekst wskazuje na rozczarowanie.",
    ),
    Sentence(
        "Super -- kolejna runda poprawek zamiast publikacji.",
        "irony", {"super": 2}, "negative",
        "Leksykon widzi 'super' (+2) = POZYTYWNY. Ironiczny komentarz na temat problemów.",
    ),
    # ── mixed ──────────────────────────────────────────────────────────────────
    Sentence(
        "Wyniki są pozytywne, ale nie tak doskonale jak planowałem.",
        "mixed", {"pozytywne": 1, "doskonale": 2}, "neutral",
        "Leksykon sumuje +3 = POZYTYWNY. Ale negacja+intensywność 'nie doskonale' obniżają ocenę.",
    ),
    Sentence(
        "Czas reakcji był dobry, ale popełniono wiele błędów.",
        "mixed", {"dobry": 1, "błędów": -1}, "neutral",
        "Leksykon sumuje +1+(-1) = 0 = NEUTRALNY. Trafił -- ale z innych powodów.",
    ),
    Sentence(
        "Eksperyment był trudny, ale zakończył się sukcesem.",
        "mixed", {"trudny": -1, "sukcesem": 2}, "positive",
        "Leksykon sumuje -1+2 = +1 = POZYTYWNY. Tu trafił. 'Trudny' to kontekst, nie ocena.",
    ),
    Sentence(
        "Model jest świetny do małych zbiorów, ale fatalny przy dużych.",
        "mixed", {"świetny": 2, "fatalny": -2}, "neutral",
        "Leksykon sumuje +2+(-2) = 0 = NEUTRALNY. Przypadkowo trafił.",
    ),
    Sentence(
        "Badanie było trudne i nie przyniosło spektakularnych wyników.",
        "mixed", {"trudne": -1}, "negative",
        "Leksykon widzi 'trudne' (-1) = NEGATYWNY. Trafił, ale brakuje kontekstu o słabych wynikach.",
    ),
    Sentence(
        "Czas reakcji był nieźły, jednak uczestnicy byli rozczarowani procedurą.",
        "mixed", {"nieźły": 1, "rozczarowani": -1}, "neutral",
        "Leksykon sumuje +1+(-1) = 0 = NEUTRALNY. Trafił -- mieszane sygnały w zdaniu.",
    ),
    Sentence(
        "Świetna metodologia, fatalnie wykonana.",
        "mixed", {"świetna": 2, "fatalnie": -2}, "negative",
        "Leksykon sumuje 0 = NEUTRALNY. Ale prawdziwy sens jest negatywny.",
    ),
    Sentence(
        "Wyniki nie są doskonale, lecz są lepsze niż oczekiwano.",
        "mixed", {"doskonale": 2}, "positive",
        "Negacja 'nie doskonale' powinna obniżyć ocenę. Leksykon widzi +2 = POZYTYWNY. Tu trafił, ale z błędnego powodu.",
    ),
]


def draw_session(bank: list[Sentence]) -> list[Sentence]:
    """Return 8 sentences. First = clear_pos, second = clear_neg, rest random."""
    clear_pos = [s for s in bank if s.trap == "clear_pos"]
    clear_neg = [s for s in bank if s.trap == "clear_neg"]
    rest = [s for s in bank if s.trap not in ("clear_pos", "clear_neg")]
    warm_up = [random.choice(clear_pos), random.choice(clear_neg)]
    remaining = random.sample(rest, min(6, len(rest)))
    return warm_up + remaining

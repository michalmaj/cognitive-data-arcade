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
    explanation: str   # ASCII-safe, shown in PhaseRoundResult


SENTENCE_BANK: list[Sentence] = [
    # ── clear_pos ──────────────────────────────────────────────────────────────
    Sentence(
        "Wyniki testu byly znakomite i wszyscy byli zadowoleni.",
        "clear_pos", {"znakomite": 2, "zadowoleni": 1}, "positive",
        "Leksykon trafnie wykryl dwa pozytywne slowa. To latwy przypadek.",
    ),
    Sentence(
        "Eksperyment zakonczyl sie sukcesem i wyniki byly doskonale.",
        "clear_pos", {"sukcesem": 2, "doskonale": 2}, "positive",
        "Dwa silnie pozytywne slowa. Klasyfikator nie mial problemow.",
    ),
    Sentence(
        "Metoda okazala sie rewelacyjna i przyniosla doskonale rezultaty.",
        "clear_pos", {"rewelacyjna": 2, "doskonale": 2}, "positive",
        "Leksykon ma oba slowa i poprawnie ocenia sentyment.",
    ),
    Sentence(
        "Uczestnicy wykonali zadanie szybko i poprawnie.",
        "clear_pos", {"szybko": 1, "poprawnie": 1}, "positive",
        "Dwa lagodnie pozytywne slowa. Suma wag = +2.",
    ),
    Sentence(
        "Wyniki sa pozytywne i potwierdzaja nasze hipotezy.",
        "clear_pos", {"pozytywne": 1}, "positive",
        "Jedno kluczowe slowo wystarczy dla poprawnej klasyfikacji.",
    ),
    Sentence(
        "Czas reakcji byl dobry a dokladnosc byla wysoka.",
        "clear_pos", {"dobry": 1}, "positive",
        "Slowo 'dobry' wskazuje na pozytywny sentyment.",
    ),
    Sentence(
        "Badani byli zadowoleni z przebiegu eksperymentu.",
        "clear_pos", {"zadowoleni": 1}, "positive",
        "Jedno pozytywne slowo wystarczylo leksykonowi.",
    ),
    Sentence(
        "Wynik jest fantastyczny -- rekord pobity.",
        "clear_pos", {"fantastyczny": 2}, "positive",
        "Silnie pozytywne slowo. Leksykon nie mogl sie pomylic.",
    ),
    Sentence(
        "Nowe podejscie okazalo sie trafne i uzyteczne.",
        "clear_pos", {"trafne": 1, "uzyteczne": 1}, "positive",
        "Dwa umiarkowanie pozytywne slowa. Suma = +2.",
    ),
    Sentence(
        "Model dziala swietnie na danych testowych.",
        "clear_pos", {"swietnie": 2}, "positive",
        "Jedno silnie pozytywne slowo. Klasyfikacja oczywista.",
    ),
    # ── clear_neg ──────────────────────────────────────────────────────────────
    Sentence(
        "Eksperyment zakonczyl sie porazka i wyniki byly fatalne.",
        "clear_neg", {"porazka": -2, "fatalne": -2}, "negative",
        "Dwa silnie negatywne slowa. Leksykon nie mial problemow.",
    ),
    Sentence(
        "Czas reakcji byl powolny i popelniono wiele bledow.",
        "clear_neg", {"powolny": -1, "bledow": -1}, "negative",
        "Dwa lagodnie negatywne slowa. Suma = -2.",
    ),
    Sentence(
        "Wyniki sa koszmarnie slabe i nie nadaja sie do analizy.",
        "clear_neg", {"koszmarnie": -2, "slabe": -1}, "negative",
        "Silne i lagodne ujemne slowo. Leksykon to widzi.",
    ),
    Sentence(
        "Metoda okazala sie bezuzyteczna w tym kontekscie.",
        "clear_neg", {"bezuzyteczna": -2}, "negative",
        "Jedno mocno negatywne slowo. Klasyfikacja oczywista.",
    ),
    Sentence(
        "Badanie zakonczylo sie klapa -- hipoteza obalona.",
        "clear_neg", {"klapa": -2}, "negative",
        "Slowo 'klapa' to silny sygnal negatywny.",
    ),
    Sentence(
        "Uczestnicy byli rozczarowani wynikami sesji.",
        "clear_neg", {"rozczarowani": -1}, "negative",
        "Jedno negatywne slowo. Leksykon rozpoznal nastroj.",
    ),
    Sentence(
        "Algorytm dziala tragicznie i bledna klasyfikacja w kazdej probie.",
        "clear_neg", {"tragicznie": -2, "bledna": -1}, "negative",
        "Dwa negatywne slowa. Suma = -3.",
    ),
    Sentence(
        "Wyniki sa fatalne i wymagaja powaznych poprawek.",
        "clear_neg", {"fatalne": -2}, "negative",
        "Jedno silnie negatywne slowo. Jasny przypadek.",
    ),
    Sentence(
        "Eksperyment byl trudny i zakonczyl sie porazka.",
        "clear_neg", {"trudny": -1, "porazka": -2}, "negative",
        "Dwa negatywne slowa. Leksykon sklasyfikowal poprawnie.",
    ),
    Sentence(
        "Probki byly slabe jakosciowo i przysporzaly problemow.",
        "clear_neg", {"slabe": -1, "problemow": -1}, "negative",
        "Dwa lagodnie negatywne slowa. Suma = -2.",
    ),
    # ── negation ───────────────────────────────────────────────────────────────
    Sentence(
        "Badani nie wyrazili zadowolenia z przebiegu sesji.",
        "negation", {"zadowolenia": 1}, "negative",
        "Leksykon widzi 'zadowolenia' (+1) i mowi POZYTYWNY. Ale 'nie' odwraca sens.",
    ),
    Sentence(
        "Wyniki nie byly fatalne, ale pozostawily wiele do zyczenia.",
        "negation", {"fatalne": -2}, "negative",
        "Leksykon widzi 'fatalne' (-2) i mowi NEGATYWNY. Ale 'nie fatalne' to cos innego.",
    ),
    Sentence(
        "Metoda nie okazala sie tak uzyteczna jak oczekiwano.",
        "negation", {"uzyteczna": 1}, "negative",
        "Leksykon widzi 'uzyteczna' (+1) = POZYTYWNY. 'Nie tak uzyteczna' to ograniczenie.",
    ),
    Sentence(
        "Nikt nie powiedzial, ze wyniki sa pozytywne.",
        "negation", {"pozytywne": 1}, "negative",
        "Leksykon wykrywa 'pozytywne' i mowi POZYTYWNY. Calosc obraca sens.",
    ),
    Sentence(
        "Uczestnicy nie wskazywali na trudnosci w zadaniu.",
        "negation", {"trudnosci": -1}, "positive",
        "Leksykon widzi 'trudnosci' (-1) = NEGATYWNY. 'Nie wskazywali na trudnosci' to dobra wiadomosc.",
    ),
    Sentence(
        "Eksperyment nie skonczyl sie sukcesem.",
        "negation", {"sukcesem": 2}, "negative",
        "Leksykon wykrywa 'sukcesem' (+2) = POZYTYWNY. Ale to opis porazki.",
    ),
    Sentence(
        "Wyniki nie sa tak doskonale jak prezentowano.",
        "negation", {"doskonale": 2}, "negative",
        "Leksykon widzi 'doskonale' (+2) = POZYTYWNY. To krytyka, nie chwala.",
    ),
    Sentence(
        "Nie popelniono zadnych bledow podczas sesji.",
        "negation", {"bledow": -1}, "positive",
        "Leksykon widzi 'bledow' (-1) = NEGATYWNY. 'Nie popelniono bledow' = dobry wynik.",
    ),
    Sentence(
        "Dane nie wykazuja zadnych problemow z jakoscia.",
        "negation", {"problemow": -1}, "positive",
        "Leksykon wykrywa 'problemow' (-1). Ale brak problemow to dobra wiadomosc.",
    ),
    Sentence(
        "Model nie wypadl slabo na zbiorze testowym.",
        "negation", {"slabo": -1}, "positive",
        "Leksykon widzi 'slabo' (-1) = NEGATYWNY. 'Nie wypadl slabo' = wypadl dobrze.",
    ),
    Sentence(
        "Hipoteza nie zostala potwierdzona -- wyniki sa rozczarowujace.",
        "negation", {"rozczarowujace": -1}, "negative",
        "Tu 'nie' dotyczy hipotezy, a 'rozczarowujace' potwierdza negatywny sentyment.",
    ),
    Sentence(
        "Czas reakcji byl dobry, choc nie idealny.",
        "negation", {"dobry": 1}, "neutral",
        "Leksykon widzi 'dobry' (+1) = POZYTYWNY. 'Nie idealny' sugeruje ograniczenia.",
    ),
    # ── intensity ──────────────────────────────────────────────────────────────
    Sentence(
        "Wyniki sa niezle, ale moglby byc lepsze.",
        "intensity", {"niezle": 1}, "neutral",
        "Leksykon mowi POZYTYWNY za 'niezle'. Ale 'mogloby byc lepiej' sygnalizuje sredniosc.",
    ),
    Sentence(
        "Dokladnosc modelu jest poprawna, choc nie imponujace.",
        "intensity", {"poprawna": 1, "imponujace": 2}, "neutral",
        "Leksykon sumuje +1+2 = POZYTYWNY. Ale 'nie imponujace' to korekta w dol.",
    ),
    Sentence(
        "Wydajnosc systemu jest dobra, lecz daleka od swietnej.",
        "intensity", {"dobra": 1, "swietna": 2}, "neutral",
        "Leksykon sumuje +1+2 = +3 = POZYTYWNY. Ale 'daleka od swietnej' to krytyka.",
    ),
    Sentence(
        "Rezultaty sa pozytywne, ale nie spektakularne.",
        "intensity", {"pozytywne": 1}, "neutral",
        "Leksykon mowi POZYTYWNY. Ale 'nie spektakularne' silnie obniza ocene.",
    ),
    Sentence(
        "Sesja przebiegla w miare sprawnie, z drobnymi bledami.",
        "intensity", {"bledami": -1}, "neutral",
        "'Drobnymi bledami' to lagodna krytyka. Leksykon widzi tylko 'bledami' (-1).",
    ),
    Sentence(
        "Wyniki sa w porzadku, choc doskonale to nie jest.",
        "intensity", {"doskonale": 2}, "neutral",
        "Leksykon widzi 'doskonale' (+2) = POZYTYWNY. 'Doskonale to nie jest' obniza ocene.",
    ),
    Sentence(
        "Eksperyment przebiegl ani doskonale ani fatalnie.",
        "intensity", {"doskonale": 2, "fatalnie": -2}, "neutral",
        "Leksykon sumuje 2+(-2) = 0 = NEUTRALNY. Trafil -- ale to zbieg okolicznosci.",
    ),
    Sentence(
        "Model jest niezly, zdecydowanie nie genialny.",
        "intensity", {"niezly": 1, "genialny": 2}, "neutral",
        "Leksykon sumuje +1+2 = POZYTYWNY. 'Nie genialny' to wyrazna korekta w dol.",
    ),
    Sentence(
        "Uczestnicy wrazili lagodne zadowolenie z zadania.",
        "intensity", {"zadowolenie": 1}, "positive",
        "Slowo 'lagodne' obniza intensywnosc zadowolenia. Leksykon nie rozumie stopniowania.",
    ),
    Sentence(
        "Czas reakcji byl dobry, choc nie doskonaly.",
        "intensity", {"dobry": 1, "doskonaly": 2}, "positive",
        "Leksykon sumuje +1+2 = POZYTYWNY. Ale 'nie doskonaly' opisuje ograniczenie.",
    ),
    # ── irony ──────────────────────────────────────────────────────────────────
    Sentence(
        "Swietna robota -- kolejny blad w danych, brawo.",
        "irony", {"swietna": 2, "brawo": 1}, "negative",
        "Leksykon widzi 'swietna' (+2) i 'brawo' (+1) = POZYTYWNY. To ironia -- sens jest negatywny.",
    ),
    Sentence(
        "No brawo, znowu zepsulismy eksperyment przez nieuwage.",
        "irony", {"brawo": 1}, "negative",
        "Leksykon wykrywa 'brawo' (+1) = POZYTYWNY. To sarkastyczna krytyka.",
    ),
    Sentence(
        "Doskonaly wynik -- pomylilismy grupy kontrolna i eksperymentalna.",
        "irony", {"doskonaly": 2}, "negative",
        "Leksykon mowi POZYTYWNY. W rzeczywistosci to blad metodologiczny.",
    ),
    Sentence(
        "Genialne podejscie -- uzyto nieodpowiedniego testu statystycznego.",
        "irony", {"genialne": 2}, "negative",
        "Leksykon raduje sie 'genialne' (+2). To sarkazm -- sens jest negatywny.",
    ),
    Sentence(
        "Swietnie -- 90 procent danych utracono przez awarie dysku.",
        "irony", {"swietnie": 2}, "negative",
        "Leksykon widzi 'swietnie' i klaskuje. To ironia wobec katastrofy.",
    ),
    Sentence(
        "Fantastyczna precyzja -- pomiar z bledem trzykrotnie przekraczajacym wartosc.",
        "irony", {"fantastyczna": 2}, "negative",
        "Leksykon wykrywa 'fantastyczna' (+2) = POZYTYWNY. Sarkastyczny komentarz do bledu.",
    ),
    Sentence(
        "Imponujace tempo -- projekt opozniony o pol roku.",
        "irony", {"imponujace": 2}, "negative",
        "Leksykon widzi 'imponujace' (+2). Kontekst: opoznienie projektu. To ironia.",
    ),
    Sentence(
        "Rewelacyjny wynik -- p-value wynosi 0,7.",
        "irony", {"rewelacyjny": 2}, "negative",
        "Leksykon klaskuje w 'rewelacyjny' (+2). p=0.7 to wynik bez znaczenia.",
    ),
    Sentence(
        "No to pozytywnie -- hipoteza odrzucona po pieciu miesiacach badan.",
        "irony", {"pozytywnie": 1}, "negative",
        "Leksykon widzi 'pozytywnie' (+1). Kontekst wskazuje na rozczarowanie.",
    ),
    Sentence(
        "Super -- kolejna runda poprawek zamiast publikacji.",
        "irony", {"super": 2}, "negative",
        "Leksykon widzi 'super' (+2) = POZYTYWNY. Ironiczny komentarz na temat problemow.",
    ),
    # ── mixed ──────────────────────────────────────────────────────────────────
    Sentence(
        "Wyniki sa pozytywne, ale nie tak doskonale jak planowalem.",
        "mixed", {"pozytywne": 1, "doskonale": 2}, "neutral",
        "Leksykon sumuje +3 = POZYTYWNY. Ale negacja+intensywnosc 'nie doskonale' obnizaja ocene.",
    ),
    Sentence(
        "Czas reakcji byl dobry, ale popelniono wiele bledow.",
        "mixed", {"dobry": 1, "bledow": -1}, "neutral",
        "Leksykon sumuje +1+(-1) = 0 = NEUTRALNY. Trafil -- ale z innych powodow.",
    ),
    Sentence(
        "Eksperyment byl trudny, ale zakonczyl sie sukcesem.",
        "mixed", {"trudny": -1, "sukcesem": 2}, "positive",
        "Leksykon sumuje -1+2 = +1 = POZYTYWNY. Tu trafil. 'Trudny' to kontekst, nie ocena.",
    ),
    Sentence(
        "Model jest swietny do malych zbiorow, ale fatalny przy duzych.",
        "mixed", {"swietny": 2, "fatalny": -2}, "neutral",
        "Leksykon sumuje +2+(-2) = 0 = NEUTRALNY. Przypadkowo trafil.",
    ),
    Sentence(
        "Badanie bylo trudne i nie przynioslo spektakularnych wynikow.",
        "mixed", {"trudne": -1}, "negative",
        "Leksykon widzi 'trudne' (-1) = NEGATYWNY. Trafil, ale brakuje kontekstu o slabych wynikach.",
    ),
    Sentence(
        "Czas reakcji byl niezly, jednak uczestnicy byli rozczarowani procedura.",
        "mixed", {"niezly": 1, "rozczarowani": -1}, "neutral",
        "Leksykon sumuje +1+(-1) = 0 = NEUTRALNY. Trafil -- mieszane sygnaly w zdaniu.",
    ),
    Sentence(
        "Swietna metodologia, fatalnie wykonana.",
        "mixed", {"swietna": 2, "fatalnie": -2}, "negative",
        "Leksykon sumuje 0 = NEUTRALNY. Ale prawdziwy sens jest negatywny.",
    ),
    Sentence(
        "Wyniki nie sa doskonale, lecz sa lepsze niz oczekiwano.",
        "mixed", {"doskonale": 2}, "positive",
        "Negacja 'nie doskonale' powinna obnizyc ocene. Leksykon widzi +2 = POZYTYWNY. Tu trafil, ale z blednego powodu.",
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

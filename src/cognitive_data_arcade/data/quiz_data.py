"""Checkpoint quiz questions — one question per lesson.

Keys are lesson_num (int). Note: lesson 5 does not exist (merged into lesson 4).
Lesson nums follow _MODULE_LESSONS in engine/badges.py:
  Module 1: 1,2,3,4,6  | Module 2: 7-12  | Module 3: 13-16
  Module 4: 17-20       | Module 5: 21-26 | Module 6: 27-32

options_pl/en: list of 3 strings. correct: index 0/1/2.
ASCII only in option text (rendered via pygame font).
"""

from __future__ import annotations

QUIZ_QUESTIONS: dict[int, dict] = {
    1: {
        "q_pl": "Co oznacza termin 'big data' w nauce kognitywnej?",
        "q_en": "What does 'big data' mean in cognitive science?",
        "options_pl": [
            "Dane z bardzo duzych plikow komputerowych",
            "Dane od wielu uczestnikow pozwalajace wykryc wzorce niemozliwe w malych probach",
            "Dane zbierane przez wiele lat bez przerwy",
        ],
        "options_en": [
            "Data stored in very large computer files",
            "Data from many participants enabling patterns impossible to find in small samples",
            "Data collected continuously over many years",
        ],
        "correct": 1,
    },
    2: {
        "q_pl": "Co mierzy czas reakcji w eksperymentach psychologicznych?",
        "q_en": "What does reaction time measure in psychological experiments?",
        "options_pl": [
            "Dokladnosc percepcji wzrokowej",
            "Pojemnosc pamieci krotkotrwalej",
            "Czas od pojawienia sie bodzca do odpowiedzi ukladu motorycznego",
        ],
        "options_en": [
            "Accuracy of visual perception",
            "Short-term memory capacity",
            "Time from stimulus onset to motor response",
        ],
        "correct": 2,
    },
    3: {
        "q_pl": "Dlaczego logi zdarzen sa wazne w zbieraniu danych?",
        "q_en": "Why are event logs important in data collection?",
        "options_pl": [
            "Zastepuja ankiety poeksperymentalne",
            "Rejestruja kazde dzialanie uczestnika z dokladnym znacznikiem czasu",
            "Mierza aktywnosc mozgu w czasie rzeczywistym",
        ],
        "options_en": [
            "They replace post-experiment questionnaires",
            "They record every participant action with a precise timestamp",
            "They measure brain activity in real time",
        ],
        "correct": 1,
    },
    4: {
        "q_pl": "Co to jest wartosc odstajaca (outlier)?",
        "q_en": "What is an outlier?",
        "options_pl": [
            "Brak danych w rekordzie",
            "Duplikat wiersza w zbiorze danych",
            "Obserwacja znacznie odbiegajaca od reszty, mogaca wskazywac na blad lub rzadkie zdarzenie",
        ],
        "options_en": [
            "A missing value in a record",
            "A duplicate row in the dataset",
            "An observation far from the rest, possibly indicating an error or rare event",
        ],
        "correct": 2,
    },
    6: {
        "q_pl": "Jaki jest glowny cel eksploracyjnej analizy danych (EDA)?",
        "q_en": "What is the main goal of Exploratory Data Analysis (EDA)?",
        "options_pl": [
            "Budowa finalnego modelu predykcyjnego",
            "Zbieranie nowych danych eksperymentalnych",
            "Zrozumienie struktury, rozkladow i relacji w danych przed modelowaniem",
        ],
        "options_en": [
            "Building the final predictive model",
            "Collecting new experimental data",
            "Understanding structure, distributions and relationships before modelling",
        ],
        "correct": 2,
    },
    7: {
        "q_pl": "Czego uczy efekt Stroopa?",
        "q_en": "What does the Stroop effect demonstrate?",
        "options_pl": [
            "Ze kolory sa przetwarzane szybciej niz slowa",
            "Ze automatyczne procesy (czytanie) moga interferowac z kontrolowanymi (nazywanie koloru)",
            "Ze pamiec krotkotrwala jest ograniczona do 7 elementow",
        ],
        "options_en": [
            "That colours are processed faster than words",
            "That automatic processes (reading) can interfere with controlled ones (naming colour)",
            "That short-term memory is limited to 7 items",
        ],
        "correct": 1,
    },
    8: {
        "q_pl": "Co mierzy zadanie Flankera?",
        "q_en": "What does the Flanker task measure?",
        "options_pl": [
            "Szybkosc percepcji wzrokowej",
            "Zdolnosc ignorowania irrelewantnych bodzcow otaczajacych cel",
            "Pojemnosc pamieci roboczej",
        ],
        "options_en": [
            "Speed of visual perception",
            "Ability to ignore irrelevant stimuli surrounding a target",
            "Working memory capacity",
        ],
        "correct": 1,
    },
    9: {
        "q_pl": "Co bada zadanie Go/No-Go?",
        "q_en": "What does the Go/No-Go task study?",
        "options_pl": [
            "Szybkosc uczenia sie sekwencji ruchowych",
            "Rozroznianie kolorow pod presja czasu",
            "Hamowanie odpowiedzi — zdolnosc do powstrzymania automatycznej reakcji",
        ],
        "options_en": [
            "Speed of learning motor sequences",
            "Colour discrimination under time pressure",
            "Response inhibition — ability to suppress an automatic reaction",
        ],
        "correct": 2,
    },
    10: {
        "q_pl": "Co mierzy zadanie N-back?",
        "q_en": "What does the N-back task measure?",
        "options_pl": [
            "Pojemnosc i aktualizowanie pamieci roboczej",
            "Czas reakcji na bodziec sluchowy",
            "Rozpoznawanie wzorcow wzrokowych",
        ],
        "options_en": [
            "Capacity and updating of working memory",
            "Reaction time to auditory stimuli",
            "Visual pattern recognition",
        ],
        "correct": 0,
    },
    11: {
        "q_pl": "Co to jest efekt pop-out w wyszukiwaniu wzrokowym?",
        "q_en": "What is the pop-out effect in visual search?",
        "options_pl": [
            "Wyszukiwanie trwa krocej gdy jest wiecej obiektow",
            "Wzrok musi omiatac caly ekran po kolei",
            "Natychmiastowe wykrycie celu gdy rozni sie jedna wyrazna cecha od dystraktorow",
        ],
        "options_en": [
            "Search is shorter when there are more objects",
            "The eye must scan the whole screen sequentially",
            "Instant detection of a target that differs by one salient feature from distractors",
        ],
        "correct": 2,
    },
    12: {
        "q_pl": "Dlaczego agregacja wielu miar kognitywnych jest wartosciowsza niz jedna miara?",
        "q_en": "Why is aggregating multiple cognitive measures more valuable than one?",
        "options_pl": [
            "Jeden test wystarczy jesli jest odpowiednio dlugi",
            "Srednia arytmetyczna wszystkich wynikow to najlepsza miara",
            "Rozne testy mierza rozne aspekty poznania i razem daja pelniejszy profil",
        ],
        "options_en": [
            "One test is enough if it is long enough",
            "The arithmetic mean of all scores is the best measure",
            "Different tests measure different aspects of cognition and together give a fuller profile",
        ],
        "correct": 2,
    },
    13: {
        "q_pl": "Co opisuje rozklad normalny?",
        "q_en": "What does a normal distribution describe?",
        "options_pl": [
            "Rozklad w ktorym wszystkie wartosci sa jednakowo prawdopodobne",
            "Rozklad z wieloma szczytami odpowiadajacymi roznym grupom",
            "Symetryczny rozklad gdzie srednia, mediana i moda sa rowne",
        ],
        "options_en": [
            "A distribution where all values are equally probable",
            "A distribution with multiple peaks corresponding to different groups",
            "A symmetric distribution where mean, median and mode are equal",
        ],
        "correct": 2,
    },
    14: {
        "q_pl": "Dlaczego korelacja nie oznacza przyczynowosci?",
        "q_en": "Why does correlation not imply causation?",
        "options_pl": [
            "Korelacja mierzy tylko liniowe zaleznosci, a zwiazki sa zawsze nieliniowe",
            "Obie zmienne moga zalezec od trzeciej lub wspolwystepowanie moze byc przypadkowe",
            "Zbyt malo danych zawsze powoduje korelacje pozorna",
        ],
        "options_en": [
            "Correlation only measures linear relationships, which are always non-linear",
            "Both variables may depend on a third, or co-occurrence may be coincidental",
            "Too little data always causes spurious correlation",
        ],
        "correct": 1,
    },
    15: {
        "q_pl": "Co oznacza p < 0.05 w testowaniu hipotez?",
        "q_en": "What does p < 0.05 mean in hypothesis testing?",
        "options_pl": [
            "Hipoteza alternatywna jest prawdziwa z 95% pewnoscia",
            "Wynik jest praktycznie istotny i ma duzy efekt",
            "Szansa uzyskania takich wynikow przez przypadek (gdy H0 prawdziwa) jest < 5%",
        ],
        "options_en": [
            "The alternative hypothesis is true with 95% certainty",
            "The result is practically significant and has a large effect",
            "The chance of obtaining such results by chance (when H0 is true) is < 5%",
        ],
        "correct": 2,
    },
    16: {
        "q_pl": "Czym rozni sie regresja od klasyfikacji?",
        "q_en": "How does regression differ from classification?",
        "options_pl": [
            "Regresja dziala tylko na danych czasowych, klasyfikacja na statycznych",
            "Regresja przewiduje wartosc ciagla (np. temperature), klasyfikacja przypisuje do kategorii",
            "Klasyfikacja wymaga zawsze wiecej danych treningowych niz regresja",
        ],
        "options_en": [
            "Regression works only on time-series data, classification on static data",
            "Regression predicts a continuous value (e.g. temperature), classification assigns categories",
            "Classification always requires more training data than regression",
        ],
        "correct": 1,
    },
    17: {
        "q_pl": "Dlaczego dobor cech (feature selection) jest wazny w ML?",
        "q_en": "Why is feature selection important in ML?",
        "options_pl": [
            "Wieksza liczba cech zawsze poprawia dokladnosc modelu",
            "Cechy sa dobierane przez algorytm automatycznie bez ingerencji",
            "Nieistotne cechy zwiekszaja szum, czas obliczen i ryzyko przeuczenia",
        ],
        "options_en": [
            "More features always improve model accuracy",
            "Features are selected automatically by the algorithm without input",
            "Irrelevant features increase noise, computation time and overfitting risk",
        ],
        "correct": 2,
    },
    18: {
        "q_pl": "Co to jest dokladnosc (accuracy) klasyfikatora?",
        "q_en": "What is classifier accuracy?",
        "options_pl": [
            "Prawdopodobienstwo poprawnej klasyfikacji przykladu pozytywnego",
            "Udzial poprawnie sklasyfikowanych przykladow sposrod wszystkich przykladow",
            "Sredni czas klasyfikacji jednego przykladu testowego",
        ],
        "options_en": [
            "Probability of correctly classifying a positive example",
            "Proportion of correctly classified examples out of all examples",
            "Average time to classify one test example",
        ],
        "correct": 1,
    },
    19: {
        "q_pl": "Co to jest przeuczenie (overfitting)?",
        "q_en": "What is overfitting?",
        "options_pl": [
            "Model ktory trenuje zbyt dlugo i zaczyna sie przegrzewac",
            "Model z za duza liczba warstw jak w glebokiej sieci neuronowej",
            "Model zbyt dobrze dopasowany do danych treningowych, slabo generalizujacy na nowe dane",
        ],
        "options_en": [
            "A model that trains too long and starts to overheat",
            "A model with too many layers like a deep neural network",
            "A model over-fitted to training data that generalizes poorly to new data",
        ],
        "correct": 2,
    },
    20: {
        "q_pl": "Czym rozni sie anomalia od szumu w danych?",
        "q_en": "How does an anomaly differ from noise in data?",
        "options_pl": [
            "Anomalie to zawsze bledy pomiarowe wymagajace korekcji",
            "Szum pojawia sie tylko w danych dzwiekowych i wideo",
            "Anomalia to rzadkie zdarzenie o potencjalnym znaczeniu, szum to losowe odchylenia bez znaczenia",
        ],
        "options_en": [
            "Anomalies are always measurement errors requiring correction",
            "Noise appears only in audio and video data",
            "An anomaly is a rare event of potential interest; noise is random meaningless deviation",
        ],
        "correct": 2,
    },
    21: {
        "q_pl": "Co to jest tokenizacja tekstu?",
        "q_en": "What is text tokenization?",
        "options_pl": [
            "Tlumaczenie tekstu na wektor liczb zmiennoprzecinkowych",
            "Usuwanie slow stopu z tekstu przed analiza",
            "Podzial tekstu na mniejsze jednostki takie jak slowa lub znaki interpunkcyjne",
        ],
        "options_en": [
            "Translating text into a vector of floating-point numbers",
            "Removing stop words from text before analysis",
            "Splitting text into smaller units such as words or punctuation marks",
        ],
        "correct": 2,
    },
    22: {
        "q_pl": "Co mierzy miara TF-IDF?",
        "q_en": "What does TF-IDF measure?",
        "options_pl": [
            "Liczbe wystapien slowa w calym zbiorze dokumentow",
            "Waznosc slowa w dokumencie wzgledem calego zbioru — czeste tu, rzadkie globalnie",
            "Semantyczne podobienstwo dwoch slow na podstawie kontekstu",
        ],
        "options_en": [
            "Number of occurrences of a word across the entire document collection",
            "Importance of a word in a document relative to the collection — frequent here, rare globally",
            "Semantic similarity of two words based on context",
        ],
        "correct": 1,
    },
    23: {
        "q_pl": "Dlaczego klasyfikacja emocji w tekscie jest trudna?",
        "q_en": "Why is emotion classification in text difficult?",
        "options_pl": [
            "Modele jezykowe nie radza sobie z tekstem krotszym niz 100 slow",
            "Emocje wystepuja tylko w mowie bezposredniej, nie w pisemnej",
            "Kontekst, ironia i kultura wplywaja na znaczenie — to samo zdanie moze wyrazac rozne emocje",
        ],
        "options_en": [
            "Language models cannot handle texts shorter than 100 words",
            "Emotions appear only in direct speech, not in written form",
            "Context, irony and culture affect meaning — the same sentence can express different emotions",
        ],
        "correct": 2,
    },
    24: {
        "q_pl": "Co oznacza ze dwa slowa sa 'blisko siebie' w przestrzeni semantycznej?",
        "q_en": "What does it mean for two words to be 'close' in semantic space?",
        "options_pl": [
            "Slowa maja podobna liczbe liter i brzmia podobnie",
            "Slowa naleza do tej samej kategorii gramatycznej",
            "Slowa czesto wspolwystepuja w podobnych kontekstach i maja zblizone znaczenie",
        ],
        "options_en": [
            "The words have a similar number of letters and sound similar",
            "The words belong to the same grammatical category",
            "The words often co-occur in similar contexts and have related meaning",
        ],
        "correct": 2,
    },
    25: {
        "q_pl": "Co robi modelowanie tematyczne (topic modeling)?",
        "q_en": "What does topic modeling do?",
        "options_pl": [
            "Klasyfikuje dokumenty do z gory ustalonych kategorii",
            "Automatycznie odkrywa ukryte tematy w zbiorze dokumentow bez etykiet",
            "Tlumaczy dokumenty na inny jezyk zachowujac tematyke",
        ],
        "options_en": [
            "Classifies documents into predefined categories",
            "Automatically discovers hidden topics in a document collection without labels",
            "Translates documents into another language while preserving the topic",
        ],
        "correct": 1,
    },
    26: {
        "q_pl": "W jakich zadaniach ludzie zazwyczaj przewyzszaja modele ML?",
        "q_en": "In which tasks do humans typically outperform ML models?",
        "options_pl": [
            "Zadaniach wymagajacych szybkiego przetwarzania duzych zbiorow danych",
            "Zadaniach z wyraznie zdefiniowanymi regulami i duza liczba przykladow",
            "Zadaniach wymagajacych zdrowego rozsadku i rozumowania w zupelnie nowych sytuacjach",
        ],
        "options_en": [
            "Tasks requiring rapid processing of large datasets",
            "Tasks with clearly defined rules and many examples",
            "Tasks requiring common sense and reasoning in entirely novel situations",
        ],
        "correct": 2,
    },
    27: {
        "q_pl": "Co to jest centralnosc (centrality) w sieci spolecznej?",
        "q_en": "What is centrality in a social network?",
        "options_pl": [
            "Liczba grup do ktorych nalezy uczestnik sieci",
            "Srednia dlugosc sciezki miedzy dwoma wezlami w sieci",
            "Miara waznosci wezla w sieci na podstawie jego polaczen",
        ],
        "options_en": [
            "The number of groups a network participant belongs to",
            "The average path length between two nodes in the network",
            "A measure of a node's importance in the network based on its connections",
        ],
        "correct": 2,
    },
    28: {
        "q_pl": "Co przyspiesza rozprzestrzenianie sie dezinformacji?",
        "q_en": "What accelerates the spread of misinformation?",
        "options_pl": [
            "Dlugosc i szczegolowsc informacji",
            "Anonimowsc nadawcy wiadomosci",
            "Emocjonalny przekaz, potwierdzenie przekonan i latwost udostepniania",
        ],
        "options_en": [
            "Length and detail of the information",
            "Anonymity of the message sender",
            "Emotional content, confirmation of beliefs and ease of sharing",
        ],
        "correct": 2,
    },
    29: {
        "q_pl": "Co to jest banka filtrujaca (filter bubble)?",
        "q_en": "What is a filter bubble?",
        "options_pl": [
            "Blad algorytmu pokazujacego nieodpowiednie tresci uzytkownikowi",
            "Technika marketingowa skierowana do okreslonej grupy wiekowej",
            "Srodowisko informacyjne gdzie algorytmy pokazuja tresci zgodne z preferencjami, ograniczajac roznorodnosc",
        ],
        "options_en": [
            "An algorithm error showing inappropriate content to a user",
            "A marketing technique targeting a specific age group",
            "An information environment where algorithms show preference-matching content, limiting diversity",
        ],
        "correct": 2,
    },
    30: {
        "q_pl": "Co to jest 'bias blind spot'?",
        "q_en": "What is the 'bias blind spot'?",
        "options_pl": [
            "Selektywne zapamietywanie informacji potwierdzajacych nasze przekonania",
            "Tendencja do dostrzegania uprzedzen u innych przy slabej zdolnosci do ich wykrywania u siebie",
            "Trudnosc w podejmowaniu decyzji przy nadmiarze opcji",
        ],
        "options_en": [
            "Selectively remembering information that confirms our beliefs",
            "Tendency to notice biases in others while being poor at detecting them in oneself",
            "Difficulty making decisions when faced with too many options",
        ],
        "correct": 1,
    },
    31: {
        "q_pl": "Jaka jest kluczowa lekcja kursu 'You Were the Dataset'?",
        "q_en": "What is the key lesson of 'You Were the Dataset'?",
        "options_pl": [
            "Modele AI sa zawsze obiektywne bo nie maja emocji ani uprzedzen",
            "Prywatnosc danych nie ma znaczenia dla postepu nauki",
            "Nasze zachowania i decyzje sa danymi ktore mozna zbierac, analizowac i modelowac",
        ],
        "options_en": [
            "AI models are always objective because they have no emotions or biases",
            "Data privacy doesn't matter for scientific progress",
            "Our behaviours and decisions are data that can be collected, analysed and modelled",
        ],
        "correct": 2,
    },
    32: {
        "q_pl": "Co odroznia dobrego architekta systemu AI od zlyego?",
        "q_en": "What distinguishes a good AI system architect from a poor one?",
        "options_pl": [
            "Uzywanie najnowszych i najbardziej zlozonych algorytmow",
            "Maksymalizacja dokladnosci na zbiorze testowym za wszelka cene",
            "Uwzglednienie ograniczen danych, etyki i konsekwencji obok dokladnosci technicznej",
        ],
        "options_en": [
            "Using the latest and most complex algorithms",
            "Maximising test-set accuracy at any cost",
            "Considering data limitations, ethics and consequences alongside technical accuracy",
        ],
        "correct": 2,
    },
}


def get_question(lesson_num: int) -> dict | None:
    """Return the quiz question dict for lesson_num, or None if none exists."""
    return QUIZ_QUESTIONS.get(lesson_num)

"""Checkpoint quiz questions — one question per lesson.

Keys are lesson_num (int). Note: lesson 5 does not exist (merged into lesson 4).
Lesson nums follow _MODULE_LESSONS in engine/badges.py:
  Module 1: 1,2,3,4,6  | Module 2: 7-12  | Module 3: 13-16
  Module 4: 17-20       | Module 5: 21-26 | Module 6: 27-32

options_pl/en: list of 3 strings. correct: index 0/1/2.
"""

from __future__ import annotations

QUIZ_QUESTIONS: dict[int, dict] = {
    1: {
        "q_pl": "Co oznacza termin 'big data' w nauce kognitywnej?",
        "q_en": "What does 'big data' mean in cognitive science?",
        "options_pl": [
            "Dane z bardzo dużych plików komputerowych",
            "Dane od wielu uczestników pozwalające wykryć wzorce niemożliwe w małych próbach",
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
            "Dokładność percepcji wzrokowej",
            "Pojemność pamięci krótkotrwałej",
            "Czas od pojawienia się bodźca do odpowiedzi układu motorycznego",
        ],
        "options_en": [
            "Accuracy of visual perception",
            "Short-term memory capacity",
            "Time from stimulus onset to motor response",
        ],
        "correct": 2,
    },
    3: {
        "q_pl": "Dlaczego logi zdarzeń są ważne w zbieraniu danych?",
        "q_en": "Why are event logs important in data collection?",
        "options_pl": [
            "Zastępują ankiety poeksperymentalne",
            "Rejestrują każde działanie uczestnika z dokładnym znacznikiem czasu",
            "Mierzą aktywność mózgu w czasie rzeczywistym",
        ],
        "options_en": [
            "They replace post-experiment questionnaires",
            "They record every participant action with a precise timestamp",
            "They measure brain activity in real time",
        ],
        "correct": 1,
    },
    4: {
        "q_pl": "Co to jest wartość odstająca (outlier)?",
        "q_en": "What is an outlier?",
        "options_pl": [
            "Brak danych w rekordzie",
            "Duplikat wiersza w zbiorze danych",
            "Obserwacja znacznie odbiegająca od reszty, mogąca wskazywać na błąd lub rzadkie zdarzenie",
        ],
        "options_en": [
            "A missing value in a record",
            "A duplicate row in the dataset",
            "An observation far from the rest, possibly indicating an error or rare event",
        ],
        "correct": 2,
    },
    6: {
        "q_pl": "Jaki jest główny cel eksploracyjnej analizy danych (EDA)?",
        "q_en": "What is the main goal of Exploratory Data Analysis (EDA)?",
        "options_pl": [
            "Budowa finalnego modelu predykcyjnego",
            "Zbieranie nowych danych eksperymentalnych",
            "Zrozumienie struktury, rozkładów i relacji w danych przed modelowaniem",
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
            "Że kolory są przetwarzane szybciej niż słowa",
            "Że automatyczne procesy (czytanie) mogą interferować z kontrolowanymi (nazywanie koloru)",
            "Że pamięć krótkotrwała jest ograniczona do 7 elementów",
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
            "Szybkość percepcji wzrokowej",
            "Zdolność ignorowania irrelewantnych bodźców otaczających cel",
            "Pojemność pamięci roboczej",
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
            "Szybkość uczenia się sekwencji ruchowych",
            "Rozróżnianie kolorów pod presją czasu",
            "Hamowanie odpowiedzi - zdolność do powstrzymania automatycznej reakcji",
        ],
        "options_en": [
            "Speed of learning motor sequences",
            "Colour discrimination under time pressure",
            "Response inhibition - ability to suppress an automatic reaction",
        ],
        "correct": 2,
    },
    10: {
        "q_pl": "Co mierzy zadanie N-back?",
        "q_en": "What does the N-back task measure?",
        "options_pl": [
            "Pojemność i aktualizowanie pamięci roboczej",
            "Czas reakcji na bodziec słuchowy",
            "Rozpoznawanie wzorców wzrokowych",
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
            "Wyszukiwanie trwa krócej gdy jest więcej obiektów",
            "Wzrok musi omiatać cały ekran po kolei",
            "Natychmiastowe wykrycie celu gdy różni się jedną wyraźną cechą od dystraktorów",
        ],
        "options_en": [
            "Search is shorter when there are more objects",
            "The eye must scan the whole screen sequentially",
            "Instant detection of a target that differs by one salient feature from distractors",
        ],
        "correct": 2,
    },
    12: {
        "q_pl": "Dlaczego agregacja wielu miar kognitywnych jest wartościowsza niż jedna miara?",
        "q_en": "Why is aggregating multiple cognitive measures more valuable than one?",
        "options_pl": [
            "Jeden test wystarczy jeśli jest odpowiednio długi",
            "Średnia arytmetyczna wszystkich wyników to najlepsza miara",
            "Różne testy mierzą różne aspekty poznania i razem dają pełniejszy profil",
        ],
        "options_en": [
            "One test is enough if it is long enough",
            "The arithmetic mean of all scores is the best measure",
            "Different tests measure different aspects of cognition and together give a fuller profile",
        ],
        "correct": 2,
    },
    13: {
        "q_pl": "Co opisuje rozkład normalny?",
        "q_en": "What does a normal distribution describe?",
        "options_pl": [
            "Rozkład w którym wszystkie wartości są jednakowo prawdopodobne",
            "Rozkład z wieloma szczytami odpowiadającymi różnym grupom",
            "Symetryczny rozkład gdzie średnia, mediana i moda są równe",
        ],
        "options_en": [
            "A distribution where all values are equally probable",
            "A distribution with multiple peaks corresponding to different groups",
            "A symmetric distribution where mean, median and mode are equal",
        ],
        "correct": 2,
    },
    14: {
        "q_pl": "Dlaczego korelacja nie oznacza przyczynowości?",
        "q_en": "Why does correlation not imply causation?",
        "options_pl": [
            "Korelacja mierzy tylko liniowe zależności, a związki są zawsze nieliniowe",
            "Obie zmienne mogą zależeć od trzeciej lub współwystępowanie może być przypadkowe",
            "Zbyt mało danych zawsze powoduje korelację pozorną",
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
            "Hipoteza alternatywna jest prawdziwa z 95% pewnością",
            "Wynik jest praktycznie istotny i ma duży efekt",
            "Szansa uzyskania takich wyników przez przypadek (gdy H0 prawdziwa) jest < 5%",
        ],
        "options_en": [
            "The alternative hypothesis is true with 95% certainty",
            "The result is practically significant and has a large effect",
            "The chance of obtaining such results by chance (when H0 is true) is < 5%",
        ],
        "correct": 2,
    },
    16: {
        "q_pl": "Czym różni się regresja od klasyfikacji?",
        "q_en": "How does regression differ from classification?",
        "options_pl": [
            "Regresja działa tylko na danych czasowych, klasyfikacja na statycznych",
            "Regresja przewiduje wartość ciągłą (np. temperaturę), klasyfikacja przypisuje do kategorii",
            "Klasyfikacja wymaga zawsze więcej danych treningowych niż regresja",
        ],
        "options_en": [
            "Regression works only on time-series data, classification on static data",
            "Regression predicts a continuous value (e.g. temperature), classification assigns categories",
            "Classification always requires more training data than regression",
        ],
        "correct": 1,
    },
    17: {
        "q_pl": "Dlaczego dobór cech (feature selection) jest ważny w ML?",
        "q_en": "Why is feature selection important in ML?",
        "options_pl": [
            "Większa liczba cech zawsze poprawia dokładność modelu",
            "Cechy są dobierane przez algorytm automatycznie bez ingerencji",
            "Nieistotne cechy zwiększają szum, czas obliczeń i ryzyko przeuczenia",
        ],
        "options_en": [
            "More features always improve model accuracy",
            "Features are selected automatically by the algorithm without input",
            "Irrelevant features increase noise, computation time and overfitting risk",
        ],
        "correct": 2,
    },
    18: {
        "q_pl": "Co to jest dokładność (accuracy) klasyfikatora?",
        "q_en": "What is classifier accuracy?",
        "options_pl": [
            "Prawdopodobieństwo poprawnej klasyfikacji przykładu pozytywnego",
            "Udział poprawnie sklasyfikowanych przykładów spośród wszystkich przykładów",
            "Średni czas klasyfikacji jednego przykładu testowego",
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
            "Model który trenuje zbyt długo i zaczyna się przegrzewać",
            "Model z za dużą liczbą warstw jak w głębokiej sieci neuronowej",
            "Model zbyt dobrze dopasowany do danych treningowych, słabo generalizujący na nowe dane",
        ],
        "options_en": [
            "A model that trains too long and starts to overheat",
            "A model with too many layers like a deep neural network",
            "A model over-fitted to training data that generalizes poorly to new data",
        ],
        "correct": 2,
    },
    20: {
        "q_pl": "Czym różni się anomalia od szumu w danych?",
        "q_en": "How does an anomaly differ from noise in data?",
        "options_pl": [
            "Anomalie to zawsze błędy pomiarowe wymagające korekcji",
            "Szum pojawia się tylko w danych dźwiękowych i wideo",
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
            "Tłumaczenie tekstu na wektor liczb zmiennoprzecinkowych",
            "Usuwanie słów stopu z tekstu przed analizą",
            "Podział tekstu na mniejsze jednostki takie jak słowa lub znaki interpunkcyjne",
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
            "Liczbę wystąpień słowa w całym zbiorze dokumentów",
            "Ważność słowa w dokumencie względem całego zbioru - częste tu, rzadkie globalnie",
            "Semantyczne podobieństwo dwóch słów na podstawie kontekstu",
        ],
        "options_en": [
            "Number of occurrences of a word across the entire document collection",
            "Importance of a word in a document relative to the collection - frequent here, rare globally",
            "Semantic similarity of two words based on context",
        ],
        "correct": 1,
    },
    23: {
        "q_pl": "Dlaczego klasyfikacja emocji w tekście jest trudna?",
        "q_en": "Why is emotion classification in text difficult?",
        "options_pl": [
            "Modele językowe nie radzą sobie z tekstem krótszym niż 100 słów",
            "Emocje występują tylko w mowie bezpośredniej, nie w pisemnej",
            "Kontekst, ironia i kultura wpływają na znaczenie - to samo zdanie może wyrażać różne emocje",
        ],
        "options_en": [
            "Language models cannot handle texts shorter than 100 words",
            "Emotions appear only in direct speech, not in written form",
            "Context, irony and culture affect meaning - the same sentence can express different emotions",
        ],
        "correct": 2,
    },
    24: {
        "q_pl": "Co oznacza że dwa słowa są 'blisko siebie' w przestrzeni semantycznej?",
        "q_en": "What does it mean for two words to be 'close' in semantic space?",
        "options_pl": [
            "Słowa mają podobną liczbę liter i brzmią podobnie",
            "Słowa należą do tej samej kategorii gramatycznej",
            "Słowa często współwystępują w podobnych kontekstach i mają zbliżone znaczenie",
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
            "Klasyfikuje dokumenty do z góry ustalonych kategorii",
            "Automatycznie odkrywa ukryte tematy w zbiorze dokumentów bez etykiet",
            "Tłumaczy dokumenty na inny język zachowując tematykę",
        ],
        "options_en": [
            "Classifies documents into predefined categories",
            "Automatically discovers hidden topics in a document collection without labels",
            "Translates documents into another language while preserving the topic",
        ],
        "correct": 1,
    },
    26: {
        "q_pl": "W jakich zadaniach ludzie zazwyczaj przewyższają modele ML?",
        "q_en": "In which tasks do humans typically outperform ML models?",
        "options_pl": [
            "Zadaniach wymagających szybkiego przetwarzania dużych zbiorów danych",
            "Zadaniach z wyraźnie zdefiniowanymi regułami i dużą liczbą przykładów",
            "Zadaniach wymagających zdrowego rozsądku i rozumowania w zupełnie nowych sytuacjach",
        ],
        "options_en": [
            "Tasks requiring rapid processing of large datasets",
            "Tasks with clearly defined rules and many examples",
            "Tasks requiring common sense and reasoning in entirely novel situations",
        ],
        "correct": 2,
    },
    27: {
        "q_pl": "Co to jest centralność (centrality) w sieci społecznej?",
        "q_en": "What is centrality in a social network?",
        "options_pl": [
            "Liczba grup do których należy uczestnik sieci",
            "Średnia długość ścieżki między dwoma węzłami w sieci",
            "Miara ważności węzła w sieci na podstawie jego połączeń",
        ],
        "options_en": [
            "The number of groups a network participant belongs to",
            "The average path length between two nodes in the network",
            "A measure of a node's importance in the network based on its connections",
        ],
        "correct": 2,
    },
    28: {
        "q_pl": "Co przyspiesza rozprzestrzenianie się dezinformacji?",
        "q_en": "What accelerates the spread of misinformation?",
        "options_pl": [
            "Długość i szczegółowość informacji",
            "Anonimowość nadawcy wiadomości",
            "Emocjonalny przekaz, potwierdzenie przekonań i łatwość udostępniania",
        ],
        "options_en": [
            "Length and detail of the information",
            "Anonymity of the message sender",
            "Emotional content, confirmation of beliefs and ease of sharing",
        ],
        "correct": 2,
    },
    29: {
        "q_pl": "Co to jest bańka filtrująca (filter bubble)?",
        "q_en": "What is a filter bubble?",
        "options_pl": [
            "Błąd algorytmu pokazującego nieodpowiednie treści użytkownikowi",
            "Technika marketingowa skierowana do określonej grupy wiekowej",
            "Środowisko informacyjne gdzie algorytmy pokazują treści zgodne z preferencjami, ograniczając różnorodność",
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
            "Selektywne zapamiętywanie informacji potwierdzających nasze przekonania",
            "Tendencja do dostrzegania uprzedzeń u innych przy słabej zdolności do ich wykrywania u siebie",
            "Trudność w podejmowaniu decyzji przy nadmiarze opcji",
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
            "Modele AI są zawsze obiektywne bo nie mają emocji ani uprzedzeń",
            "Prywatność danych nie ma znaczenia dla postępu nauki",
            "Nasze zachowania i decyzje są danymi które można zbierać, analizować i modelować",
        ],
        "options_en": [
            "AI models are always objective because they have no emotions or biases",
            "Data privacy doesn't matter for scientific progress",
            "Our behaviours and decisions are data that can be collected, analysed and modelled",
        ],
        "correct": 2,
    },
    32: {
        "q_pl": "Co odróżnia dobrego architekta systemu AI od złego?",
        "q_en": "What distinguishes a good AI system architect from a poor one?",
        "options_pl": [
            "Używanie najnowszych i najbardziej złożonych algorytmów",
            "Maksymalizacja dokładności na zbiorze testowym za wszelką cenę",
            "Uwzględnienie ograniczeń danych, etyki i konsekwencji obok dokładności technicznej",
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

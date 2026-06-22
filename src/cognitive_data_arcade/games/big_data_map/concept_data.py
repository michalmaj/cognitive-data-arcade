from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LessonNode:
    lesson_num: int  # actual file number (1,2,3,4,6,7..32)
    name_pl: str  # short label PL, use \n for 2 lines
    name_en: str  # short label EN
    module: int  # 1-6
    description_pl: str  # 1 sentence shown in info bar / detail panel
    description_en: str


# Module colours (R,G,B)
MODULE_COLORS: dict[int, tuple[int, int, int]] = {
    1: (99, 102, 241),  # indigo  - Data & Cognition
    2: (155, 89, 182),  # purple  - Cognitive Science
    3: (46, 204, 113),  # green   - Statistics
    4: (230, 126, 34),  # orange  - Machine Learning
    5: (26, 188, 156),  # teal    - NLP
    6: (231, 76, 60),  # red     - Networks & Ethics
}

MODULE_NAMES: dict[int, tuple[str, str]] = {
    1: ("Dane i Kognitywistyka", "Data & Cognition"),
    2: ("Nauka o Poznaniu", "Cognitive Science"),
    3: ("Statystyka", "Statistics"),
    4: ("Machine Learning", "Machine Learning"),
    5: ("NLP", "NLP"),
    6: ("Sieci i Etyka", "Networks & Ethics"),
}

CONCEPT_NODES: list[LessonNode] = [
    # Module 1 - Data & Cognition (lessons 01,02,03,04,06)
    LessonNode(
        1,
        "Big Data\nw Nauce",
        "Big Data\nin Science",
        1,
        "Interaktywna mapa pojec laczaca metody Big Data z kognitywistyka.",
        "Interactive concept map linking Big Data methods to cognitive science.",
    ),
    LessonNode(
        2,
        "RT\nLab",
        "RT\nLab",
        1,
        "Pomiar czasu reakcji — podstawa chronometrii umyslowej od Dondersa (1868).",
        "Reaction time measurement — foundation of mental chronometry since Donders (1868).",
    ),
    LessonNode(
        3,
        "Event Log\nDetektyw",
        "Event Log\nDetective",
        1,
        "Parsowanie i analiza logow zdarzen — surowe dane kognitywistyki.",
        "Parsing and analysing event logs — the raw data of cognitive science.",
    ),
    LessonNode(
        4,
        "Jakosc\nDanych",
        "Data\nQuality",
        1,
        "Czyszczenie danych: brakujace wartosci, duplikaty, wartosci odstajace.",
        "Data cleaning: missing values, duplicates, outliers.",
    ),
    LessonNode(
        6,
        "EDA\nSandbox",
        "EDA\nSandbox",
        1,
        "Eksploracyjna analiza danych — wykresy i statystyki opisowe w praktyce.",
        "Exploratory data analysis — charts and descriptive statistics in practice.",
    ),
    # Module 2 - Cognitive Science (lessons 07-12)
    LessonNode(
        7,
        "Stroop\nChallenge",
        "Stroop\nChallenge",
        2,
        "Efekt Stroopa: konflikt poznawczy mierzony od 1935 roku, >13 000 cytowan.",
        "Stroop effect: cognitive conflict measured since 1935, >13,000 citations.",
    ),
    LessonNode(
        8,
        "Flanker\nTask",
        "Flanker\nTask",
        2,
        "Zadanie Flankera Eriksenow (1974): selekcja uwagi i hamowanie dystraktorow.",
        "Eriksen Flanker Task (1974): attentional selection and distractor inhibition.",
    ),
    LessonNode(
        9,
        "Go /\nNo-Go",
        "Go /\nNo-Go",
        2,
        "Kontrola hamowania: zdolnosc do zatrzymania automatycznej odpowiedzi.",
        "Inhibitory control: the ability to stop an automatic response.",
    ),
    LessonNode(
        10,
        "N-Back",
        "N-Back",
        2,
        "Pamiec robocza: Miller (1956) — 7+-2, Cowan (2001) — 4 chunki.",
        "Working memory: Miller (1956) 7+-2, Cowan (2001) 4 chunks.",
    ),
    LessonNode(
        11,
        "Visual\nSearch",
        "Visual\nSearch",
        2,
        "Przeszukiwanie wzrokowe: cechy vs koniunkcje, prawo Ficka-Dondersa.",
        "Visual search: features vs conjunctions, Fick-Donders law.",
    ),
    LessonNode(
        12,
        "Kognitywny\nDashboard",
        "Cognitive\nDashboard",
        2,
        "Profil funkcji wykonawczych laczacy wyniki Stroopa, Flankera i Go/No-Go.",
        "Executive function profile combining Stroop, Flanker, and Go/No-Go results.",
    ),
    # Module 3 - Statistics (lessons 13-16)
    LessonNode(
        13,
        "Rozklady",
        "Distributions",
        3,
        "Gauss (1809) do astronomii, Laplace CLT (1812) — podstawy wnioskowania.",
        "Gauss (1809) for astronomy, Laplace CLT (1812) — foundations of inference.",
    ),
    LessonNode(
        14,
        "Pulapka\nKorelacji",
        "Correlation\nTrap",
        3,
        "Pearson r (1896), Vigen falszywe korelacje (2015) — korelacja nie rowna sie przyczynowosci.",
        "Pearson r (1896), Vigen spurious correlations (2015) — correlation does not equal causation.",
    ),
    LessonNode(
        15,
        "Arena\nHipotez",
        "Hypothesis\nArena",
        3,
        "p=0.05 Fishera (1925), moc Cohena (1962) — granice testowania hipotez.",
        "Fisher p=0.05 (1925), Cohen power (1962) — limits of hypothesis testing.",
    ),
    LessonNode(
        16,
        "Suwak\nPredikcji",
        "Prediction\nSlider",
        3,
        "Regresja Galtona (1886) od wzrostu do uczenia maszynowego.",
        "Galton regression (1886) from height inheritance to machine learning.",
    ),
    # Module 4 - Machine Learning (lessons 17-20)
    LessonNode(
        17,
        "Feature\nHunter",
        "Feature\nHunter",
        4,
        "Klatwa wymiarowosci Bellmana (1961), LASSO Tibshiraniego (1996).",
        "Bellman's curse of dimensionality (1961), Tibshirani's LASSO (1996).",
    ),
    LessonNode(
        18,
        "Bitwa\nKlasyfik.",
        "Classifier\nBattle",
        4,
        "Perceptron Rosenblatta (1958), SVM Vapnika (1995), twierdzenie No Free Lunch.",
        "Rosenblatt perceptron (1958), Vapnik SVM (1995), No Free Lunch theorem.",
    ),
    LessonNode(
        19,
        "Potwor\nOverfit",
        "Overfitting\nMonster",
        4,
        "Brzytwa Ockhama, regularyzacja Tikhonovem (1963), Dropout (Srivastava 2014).",
        "Occam's Razor, Tikhonov regularization (1963), Dropout (Srivastava 2014).",
    ),
    LessonNode(
        20,
        "Alert\nAnomalii",
        "Anomaly\nAlert",
        4,
        "Isolation Forest (Liu 2008): anomalie izoluja sie szybciej niz typowe punkty.",
        "Isolation Forest (Liu 2008): anomalies isolate faster than typical points.",
    ),
    # Module 5 - NLP (lessons 21-26)
    LessonNode(
        21,
        "Tokenizer\nTekstu",
        "Text\nTokenizer",
        5,
        "Prawo Zipfa (1935), BPE (Sennrich 2016), Brown Corpus (1964).",
        "Zipf's law (1935), BPE (Sennrich 2016), Brown Corpus (1964).",
    ),
    LessonNode(
        22,
        "Waga\nSlow",
        "Word\nWeights",
        5,
        "TF-IDF: IDF wynalazla Karen Sparck Jones (1972) — jeden z najwazniejszych wkladow w IR.",
        "TF-IDF: IDF invented by Karen Sparck Jones (1972) — one of the most important IR contributions.",
    ),
    LessonNode(
        23,
        "Klasyfik.\nEmocji",
        "Emotion\nClassifier",
        5,
        "Analiza sentymentu: Pang i in. (2002), VADER (2014), BERT +5pp (2018).",
        "Sentiment analysis: Pang et al. (2002), VADER (2014), BERT +5pp (2018).",
    ),
    LessonNode(
        24,
        "Przestrzen\nSemantyki",
        "Semantic\nSpace",
        5,
        "Hipoteza dystrybucyjna Harrisa (1954), Word2Vec (2013), bias Bolukbasi (2016).",
        "Harris distributional hypothesis (1954), Word2Vec (2013), Bolukbasi bias (2016).",
    ),
    LessonNode(
        25,
        "Detektyw\nTematow",
        "Topic\nDetective",
        5,
        "LDA: Blei, Ng, Jordan (2003), >40 000 cytowan, BERTopic (2022).",
        "LDA: Blei, Ng, Jordan (2003), >40,000 citations, BERTopic (2022).",
    ),
    LessonNode(
        26,
        "Czlowiek\nvs Model",
        "Human\nvs Model",
        5,
        "Schemat Winograda (2011): GPT-4 ~90% vs mniejsze modele ~60%.",
        "Winograd Schema (2011): GPT-4 ~90% vs smaller models ~60%.",
    ),
    # Module 6 - Networks & Ethics (lessons 27-32)
    LessonNode(
        27,
        "Siec\nSpoleczna",
        "Social\nNetwork",
        6,
        "Male swiaty Milgrama (1967), sieci bezskalowe Barabasiego (1999).",
        "Milgram small worlds (1967), Barabasi scale-free networks (1999).",
    ),
    LessonNode(
        28,
        "Dezinfor-\nmacja",
        "Misinfor-\nmation",
        6,
        "SIR Kermacka i McKendricka (1927); falszywe newsy: R0 wyzsze niz prawdziwe.",
        "Kermack & McKendrick SIR (1927); false news has higher R0 than true news.",
    ),
    LessonNode(
        29,
        "Banka\nRekomend.",
        "Recomm.\nBubble",
        6,
        "Filtrowanie kolaboratywne Goldberga (1992), banka informacyjna Parisera (2011).",
        "Goldberg collaborative filtering (1992), Pariser filter bubble (2011).",
    ),
    LessonNode(
        30,
        "Slepa\nStronnyczosc",
        "Bias\nBlind Spot",
        6,
        "Niemozliwosc sprawiedliwosci Chouldechovej (2017): 3 kryteria nie moga byc spelnione jednoczesnie.",
        "Chouldechova fairness impossibility (2017): 3 criteria cannot all be met simultaneously.",
    ),
    LessonNode(
        31,
        "Byles\nDanetem",
        "You Were\nthe Dataset",
        6,
        "Efekt Hawthorne'a (1924), Cambridge Analytica (2018), RODO (2018).",
        "Hawthorne effect (1924), Cambridge Analytica (2018), GDPR (2018).",
    ),
    LessonNode(
        32,
        "Proba\nArchitekta",
        "Architect's\nTrial",
        6,
        "Prawo Goodharta (1975), EU AI Act (2024) — etyka algorytmiczna w praktyce.",
        "Goodhart's Law (1975), EU AI Act (2024) — algorithmic ethics in practice.",
    ),
]

# Sequential display numbers 1-31 (lesson_num 6 -> display 5; lesson_num 32 -> display 31)
DISPLAY_NUM: dict[int, int] = {node.lesson_num: idx + 1 for idx, node in enumerate(CONCEPT_NODES)}

# ---------------------------------------------------------------------------
# Conceptual edges with reasons.
# Keys are canonical (min, max) pairs.  Values: (reason_pl, reason_en).
# ---------------------------------------------------------------------------
EDGE_REASONS: dict[tuple[int, int], tuple[str, str]] = {
    # Module 1 internal
    (1, 2): (
        "RT Lab mierzy czas reakcji - fundamentalna jednostke danych Big Data.",
        "RT Lab measures reaction time — the fundamental unit of Big Data in cognitive science.",
    ),
    (1, 6): (
        "EDA jest pierwszym krokiem po zebraniu danych Big Data.",
        "EDA is the first step after collecting Big Data.",
    ),
    (2, 3): (
        "Logi zdarzen rejestruja nacisnieccia klawiszy i czasy reakcji — te same dane co RT Lab.",
        "Event logs record keypresses and reaction times — the same data as RT Lab.",
    ),
    (3, 4): (
        "Dane z logow zdarzen wymagaja intensywnego czyszczenia przed analiza.",
        "Event log data requires intensive cleaning before analysis.",
    ),
    (4, 6): (
        "EDA ujawnia brakujace wartosci, duplikaty i wartosci odstajace.",
        "EDA reveals missing values, duplicates, and outliers.",
    ),
    # RT Lab cross-module
    (2, 7): (
        "Efekt Stroopa mierzy sie przez czas reakcji — fundamentalne powiazanie.",
        "The Stroop effect is measured via reaction time — a fundamental link.",
    ),
    (2, 8): (
        "Zadanie Flankera mierzy RT przy selektywnej uwadze.",
        "The Flanker task measures RT during selective attention.",
    ),
    (2, 9): (
        "Go/No-Go mierzy czas reakcji przy hamowaniu automatycznej odpowiedzi.",
        "Go/No-Go measures RT during inhibition of automatic responses.",
    ),
    (2, 12): (
        "Dashboard agreguje czasy reakcji z trzech zadan poznawczych.",
        "The dashboard aggregates reaction times from three cognitive tasks.",
    ),
    (2, 31): (
        "Czasy reakcji zebrane w kursie sa przykladem danych behawioralnych.",
        "Course reaction times are a concrete example of behavioural data.",
    ),
    # Event Log cross-module
    (3, 21): (
        "Wpisy logow to strumien tokenizowanego tekstu — naturalne wejscie do NLP.",
        "Log entries are a stream of tokenised text — natural input for NLP.",
    ),
    (3, 22): (
        "TF-IDF mierzy waznosc zdarzen w logach systemowych.",
        "TF-IDF measures event importance in system logs.",
    ),
    # Data Quality cross-module
    (4, 13): (
        "Modele statystyczne zakladaja czyste dane bez wartosci odstajacych.",
        "Statistical models assume clean data without outliers.",
    ),
    (4, 20): (
        "Wartosci anomalne sa zarowno problemem jakosci danych, jak i sygnalem.",
        "Anomalous values are both a data quality problem and a detection signal.",
    ),
    # Big Data cross-module
    (1, 27): (
        "Sieci spoleczne sa glownym zrodlem danych Big Data na skale miliardow.",
        "Social networks are the main source of Big Data at billion-user scale.",
    ),
    (1, 29): (
        "Big Data na skale miliardow uzytkownikow umozliwia algorytmy rekomendacji.",
        "Big Data at billion-user scale makes recommendation algorithms possible.",
    ),
    (1, 31): (
        "Big Data zbiera dane behawioralne bez wiedzy uzytkownika — zrodlo dylematow prywatnosci.",
        "Big Data collects behavioural data without user awareness — the root of privacy dilemmas.",
    ),
    # EDA cross-module
    (6, 13): (
        "EDA poprzedza modelowanie statystyczne i ujawnia rozklady danych.",
        "EDA precedes statistical modelling and reveals data distributions.",
    ),
    (6, 14): (
        "EDA jako pierwsza ujawnia korelacje w danych — w tym zludne.",
        "EDA is first to reveal correlations in data — including spurious ones.",
    ),
    (6, 17): (
        "Selekcja cech zaczyna sie od wizualizacji i eksploracji EDA.",
        "Feature selection starts with EDA visualisation and exploration.",
    ),
    # Module 2 internal
    (7, 8): (
        "Oba zadania mierza selektywna uwage — zdolnosc do ignorowania dystraktorow.",
        "Both tasks measure selective attention — the ability to ignore distractors.",
    ),
    (8, 9): (
        "Flanker i Go/No-Go wymagaja hamowania automatycznej odpowiedzi.",
        "Flanker and Go/No-Go both require inhibiting automatic responses.",
    ),
    (9, 10): (
        "Go/No-Go i N-Back mierza funkcje wykonawcze z roznych perspektyw.",
        "Go/No-Go and N-Back measure executive functions from different perspectives.",
    ),
    (10, 11): (
        "N-Back i Visual Search angazuja uwage wzrokowa i pamiec robocza.",
        "N-Back and Visual Search both engage visual attention and working memory.",
    ),
    (11, 12): (
        "Visual Search uzupelnia profil uwagi w dashboardzie kognitywnym.",
        "Visual Search completes the attention profile in the cognitive dashboard.",
    ),
    # Cognitive tasks cross-module
    (7, 12): (
        "Stroop jest jednym z trzech testow funkcji wykonawczych w dashboardzie.",
        "Stroop is one of three executive function tests in the dashboard.",
    ),
    (7, 15): (
        "Hipotezy o efekcie Stroopa testuje sie statystycznie na danych RT.",
        "Hypotheses about the Stroop effect are tested statistically on RT data.",
    ),
    (8, 12): (
        "Flanker jest jednym z trzech testow funkcji wykonawczych w dashboardzie.",
        "Flanker is one of three executive function tests in the dashboard.",
    ),
    (9, 12): (
        "Go/No-Go jest jednym z trzech testow funkcji wykonawczych w dashboardzie.",
        "Go/No-Go is one of three executive function tests in the dashboard.",
    ),
    (10, 12): (
        "N-Back mierzy pamiec robocza — kluczowa skladowa dashboardu.",
        "N-Back measures working memory — a key component of the dashboard.",
    ),
    (10, 17): (
        "Pojemnosc pamieci roboczej jest cecha predykcyjna w uczeniu maszynowym.",
        "Working memory capacity is a predictive feature in machine learning.",
    ),
    (11, 13): (
        "Rozklady czasow przeszukiwania wzrokowego opisuje sie statystycznie.",
        "Visual search time distributions are described statistically.",
    ),
    (12, 17): (
        "Cechy z dashboardu kognitywnego (RT, bledy) staja sie wejsciem do ML.",
        "Dashboard features (RT, errors) become input data for machine learning.",
    ),
    # Module 3 internal
    (13, 14): (
        "Korelacja Pearsona zaklada rozklad normalny zmiennych.",
        "Pearson correlation assumes normally distributed variables.",
    ),
    (14, 15): (
        "Test korelacji jest szczegolnym przypadkiem testowania hipotez.",
        "Correlation testing is a special case of hypothesis testing.",
    ),
    (15, 16): (
        "Regresja wymaga testowania istotnosci wspolczynnikow statystycznych.",
        "Regression requires testing the statistical significance of coefficients.",
    ),
    # Stats cross-module
    (13, 15): (
        "Testy statystyczne zakladaja znane rozklady danych — normalnosc i wariancje.",
        "Statistical tests assume known data distributions — normality and variance.",
    ),
    (13, 16): (
        "Regresja liniowa zaklada rozklad normalny reszt — warunek statystyczny.",
        "Linear regression assumes normally distributed residuals — a statistical condition.",
    ),
    (13, 21): (
        "Prawo Zipfa jest rozkladem potegowym — laczy statystyke z lingwistyka.",
        "Zipf's law is a power-law distribution — linking statistics to linguistics.",
    ),
    (14, 30): (
        "Proxy features to korelacje zastepcze — zrodlo stronnyczosci algorytmicznej.",
        "Proxy features are surrogate correlations — a source of algorithmic bias.",
    ),
    (15, 18): (
        "Testy statystyczne oceniaja istotnosc roznic miedzy klasyfikatorami.",
        "Statistical tests assess the significance of differences between classifiers.",
    ),
    (15, 30): (
        "Niemozliwosc sprawiedliwosci jest matematycznym twierdzeniem jak test statystyczny.",
        "Fairness impossibility is a mathematical theorem analogous to a statistical test.",
    ),
    (15, 32): (
        "Prawo Goodharta jest analogiem p-hackingu — optymalizacja miary niszczy jej wartosc.",
        "Goodhart's Law is the analogue of p-hacking — optimising a measure destroys its value.",
    ),
    # Module 4 internal
    (17, 18): (
        "Selekcja cech jest niezbedna przed trenowaniem klasyfikatora.",
        "Feature selection is necessary before training a classifier.",
    ),
    (18, 19): (
        "Kazdy klasyfikator moze przeuczyc sie na zbiorze treningowym.",
        "Every classifier can overfit on the training set.",
    ),
    (19, 20): (
        "Przeuczony model falszywie klasyfikuje wiele normalnych punktow jako anomalie.",
        "An overfitted model falsely flags many normal points as anomalies.",
    ),
    # ML cross-module
    (16, 17): (
        "LASSO to regularyzacja regresji — selekcja cech przez zerowanie wspolczynnikow.",
        "LASSO is regression regularisation — feature selection via coefficient zeroing.",
    ),
    (16, 18): (
        "Regresja i klasyfikacja to dwa podstawowe zadania uczenia maszynowego.",
        "Regression and classification are the two fundamental machine learning tasks.",
    ),
    (16, 29): (
        "Filtrowanie kolaboratywne to faktoryzacja macierzy — forma regresji.",
        "Collaborative filtering is matrix factorisation — a form of regression.",
    ),
    (17, 19): (
        "Selekcja cech zmniejsza overfitting przez ograniczenie wymiaru przestrzeni.",
        "Feature selection reduces overfitting by limiting dimensionality.",
    ),
    (18, 26): (
        "Porownywanie klasyfikatora z ludzka ocena to kluczowy test wydajnosci NLP.",
        "Comparing a classifier to human judgement is a key NLP performance test.",
    ),
    (19, 30): (
        "Trade-off wariancji i obciazenia jest analogiem trade-offu w metrykach sprawiedliwosci.",
        "The variance-bias trade-off mirrors the fairness metrics trade-off.",
    ),
    (20, 28): (
        "Anomalnie szybkie rozprzestrzenianie sie tresci jest sygnalem dezinformacji.",
        "Anomalously fast content spread is a signal of misinformation.",
    ),
    (20, 29): (
        "Anomalne zachowanie uzytkownika jest sygnalem manipulacji rekomendacjami.",
        "Anomalous user behaviour signals recommendation system manipulation.",
    ),
    # Module 5 internal
    (21, 22): (
        "Tokenizacja poprzedza obliczanie wag TF-IDF dla slow.",
        "Tokenisation precedes computing TF-IDF weights for words.",
    ),
    (22, 23): (
        "TF-IDF jako cechy wejsciowe do klasyfikatora sentymentu.",
        "TF-IDF as input features for a sentiment classifier.",
    ),
    (23, 24): (
        "Embeddingi poprawiaja dokladnosc klasyfikacji sentymentu ponad TF-IDF.",
        "Embeddings improve sentiment classification accuracy beyond TF-IDF.",
    ),
    (24, 25): (
        "BERTopic uzywa embedddingow do klastrowania tematow.",
        "BERTopic uses embeddings to cluster topics.",
    ),
    (25, 26): (
        "Modele tematow i modele jezykowe razem umozliwiaja rozumienie tekstu.",
        "Topic models and language models together enable text understanding.",
    ),
    # NLP cross-module
    (21, 25): (
        "Tokenizacja jest pierwszym krokiem modelowania tematow.",
        "Tokenisation is the first step of topic modelling.",
    ),
    (22, 24): (
        "TF-IDF i embeddingi to dwie komplementarne reprezentacje tekstu.",
        "TF-IDF and embeddings are two complementary text representations.",
    ),
    (22, 25): (
        "TF-IDF wazenia slow stosuje sie przy modelowaniu tematow LDA.",
        "TF-IDF word weighting is applied in LDA topic modelling.",
    ),
    (23, 26): (
        "Klasyfikacja sentymentu vs ocena czlowieka — kluczowe porownanie w NLP.",
        "Sentiment classification vs human judgement — a key NLP comparison.",
    ),
    (23, 28): (
        "Analiza sentymentu wykrywa emocjonalne naladowanie dezinformacji.",
        "Sentiment analysis detects the emotional charge of misinformation.",
    ),
    (24, 26): (
        "Przestrzen semantyczna pozwala algorytmicznie mierzyc rozumienie jezyka.",
        "Semantic space enables algorithmic measurement of language understanding.",
    ),
    (25, 28): (
        "Klastry tematyczne dezinformacji identyfikuje sie modelowaniem tematow.",
        "Misinformation topic clusters are identified via topic modelling.",
    ),
    (25, 29): (
        "Rekomendacje oparte na tematach tworza banki informacyjne.",
        "Topic-based recommendations create information filter bubbles.",
    ),
    (26, 32): (
        "Pytanie o przewage czlowieka vs AI lezy w centrum etyki algorytmicznej.",
        "The question of human vs AI advantage is central to algorithmic ethics.",
    ),
    # Module 6 internal
    (27, 28): (
        "Sieci spoleczne sa medium rozprzestrzeniania sie dezinformacji.",
        "Social networks are the medium through which misinformation spreads.",
    ),
    (28, 29): (
        "Algorytmy rekomendacji amplifikuja zasieg dezinformacji.",
        "Recommendation algorithms amplify the reach of misinformation.",
    ),
    (29, 30): (
        "Algorytmy rekomendacji moga dyskryminowac grupy mniejszosciowe.",
        "Recommendation algorithms can discriminate against minority groups.",
    ),
    (30, 31): (
        "Dane behawioralne sa uzywane w stronniczych decyzjach algorytmicznych.",
        "Behavioural data is used in biased algorithmic decisions.",
    ),
    (31, 32): (
        "Prywatnosc danych behawioralnych i odpowiedzialnosc AI to dwie strony tej samej monety.",
        "Behavioural data privacy and AI accountability are two sides of the same coin.",
    ),
    # Networks & Ethics cross-module
    (27, 29): (
        "Grafy sieci spolecznej sa podstawa filtrowania kolaboratywnego.",
        "Social network graphs are the basis of collaborative filtering.",
    ),
    (27, 30): (
        "Metryki centralnosci sieci moga reprodukowac nierownosci reprezentacji.",
        "Network centrality metrics can reproduce representation inequalities.",
    ),
    (28, 31): (
        "Dane behawioralne zebrane przez platformy umozliwiaja targetowanie dezinformacji.",
        "Behavioural data collected by platforms enables misinformation targeting.",
    ),
    (30, 32): (
        "Stronnyczosc algorytmiczna jest centralnym problemem etycznym EU AI Act.",
        "Algorithmic bias is the central ethical problem addressed by the EU AI Act.",
    ),
}

# Edge list derived from reasons dict (canonical min/max pairs)
CONCEPT_EDGES: list[tuple[int, int]] = list(EDGE_REASONS.keys())

# ---------------------------------------------------------------------------
# Public helper
# ---------------------------------------------------------------------------
_node_map: dict[int, LessonNode] = {n.lesson_num: n for n in CONCEPT_NODES}


def get_connected(lesson_num: int, max_count: int = 5) -> list[tuple[LessonNode, str, str]]:
    """Return up to max_count connected nodes with (node, reason_pl, reason_en).

    Cross-module connections are listed first, then within-module.
    """
    src = _node_map.get(lesson_num)
    if src is None:
        return []

    results: list[tuple[LessonNode, str, str]] = []
    for a, b in CONCEPT_EDGES:
        other_num = b if a == lesson_num else (a if b == lesson_num else None)
        if other_num is None:
            continue
        other = _node_map.get(other_num)
        if other is None:
            continue
        key = (min(lesson_num, other_num), max(lesson_num, other_num))
        reason_pl, reason_en = EDGE_REASONS.get(key, ("", ""))
        results.append((other, reason_pl, reason_en))

    # Cross-module first, then within-module; ties broken by lesson_num
    results.sort(key=lambda t: (t[0].module == src.module, t[0].lesson_num))
    return results[:max_count]

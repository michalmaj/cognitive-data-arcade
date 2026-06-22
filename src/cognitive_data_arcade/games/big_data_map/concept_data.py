from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LessonNode:
    lesson_num: int  # actual file number (1,2,3,4,6,7..32)
    name_pl: str  # short label PL, use \n for 2 lines, max ~12 chars per line
    name_en: str  # short label EN
    module: int  # 1-6
    description_pl: str  # 1 sentence shown in info bar
    description_en: str


# Module colors (R,G,B)
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
        "Interaktywna mapa pojęć łącząca metody Big Data z kognitywistyką.",
        "Interactive concept map linking Big Data methods to cognitive science.",
    ),
    LessonNode(
        2,
        "RT\nLab",
        "RT\nLab",
        1,
        "Pomiar czasu reakcji - podstawa chronometrii umysłowej od Dondersa (1868).",
        "Reaction time measurement - foundation of mental chronometry since Donders (1868).",
    ),
    LessonNode(
        3,
        "Event Log\nDetektyw",
        "Event Log\nDetective",
        1,
        "Parsowanie i analiza logów zdarzeń - surowe dane kognitywistyki.",
        "Parsing and analysing event logs - the raw data of cognitive science.",
    ),
    LessonNode(
        4,
        "Jakość\nDanych",
        "Data\nQuality",
        1,
        "Czyszczenie danych: brakujące wartości, duplikaty, wartości odstające.",
        "Data cleaning: missing values, duplicates, outliers.",
    ),
    LessonNode(
        6,
        "EDA\nSandbox",
        "EDA\nSandbox",
        1,
        "Eksploracyjna analiza danych - wykresy i statystyki opisowe w praktyce.",
        "Exploratory data analysis - charts and descriptive statistics in practice.",
    ),
    # Module 2 - Cognitive Science (lessons 07-12)
    LessonNode(
        7,
        "Stroop\nChallenge",
        "Stroop\nChallenge",
        2,
        "Efekt Stroopa: konflikt poznawczy mierzony od 1935 roku, >13 000 cytowań.",
        "Stroop effect: cognitive conflict measured since 1935, >13,000 citations.",
    ),
    LessonNode(
        8,
        "Flanker\nTask",
        "Flanker\nTask",
        2,
        "Zadanie Flankera Eriksenów (1974): selekcja uwagi i hamowanie dystraktorów.",
        "Eriksen Flanker Task (1974): attentional selection and distractor inhibition.",
    ),
    LessonNode(
        9,
        "Go /\nNo-Go",
        "Go /\nNo-Go",
        2,
        "Kontrola hamowania: zdolność do zatrzymania automatycznej odpowiedzi.",
        "Inhibitory control: the ability to stop an automatic response.",
    ),
    LessonNode(
        10,
        "N-Back",
        "N-Back",
        2,
        "Pamięć robocza: Miller (1956) - 7+/-2, Cowan (2001) - 4 chunki.",
        "Working memory: Miller (1956) 7+/-2, Cowan (2001) 4 chunks.",
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
        "Profil funkcji wykonawczych łączący wyniki Stroopa, Flankera i Go/No-Go.",
        "Executive function profile combining Stroop, Flanker, and Go/No-Go results.",
    ),
    # Module 3 - Statistics (lessons 13-16)
    LessonNode(
        13,
        "Rozkłady",
        "Distributions",
        3,
        "Gauss (1809) do astronomii, Laplace CLT (1812) - podstawy wnioskowania.",
        "Gauss (1809) for astronomy, Laplace CLT (1812) - foundations of inference.",
    ),
    LessonNode(
        14,
        "Pułapka\nKorelacji",
        "Correlation\nTrap",
        3,
        "Pearson r (1896), Vigen fałszywe korelacje (2015) - korelacja != przyczynowość.",
        "Pearson r (1896), Vigen spurious correlations (2015) - correlation != causation.",
    ),
    LessonNode(
        15,
        "Arena\nHipotez",
        "Hypothesis\nArena",
        3,
        "p=0.05 Fishera (1925), moc Cohena (1962) - granice testowania hipotez.",
        "Fisher p=0.05 (1925), Cohen power (1962) - limits of hypothesis testing.",
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
        "Klątwa wymiarowości Bellmana (1961), LASSO Tibshiraniego (1996).",
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
        "Potwór\nOverfit",
        "Overfitting\nMonster",
        4,
        "Brzytwa Ockhama, regularyzacja Tikhonovą (1963), Dropout (Srivastava 2014).",
        "Occam's Razor, Tikhonov regularization (1963), Dropout (Srivastava 2014).",
    ),
    LessonNode(
        20,
        "Alert\nAnomalii",
        "Anomaly\nAlert",
        4,
        "Isolation Forest (Liu 2008): anomalie izolują się szybciej niż typowe punkty.",
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
        "Waga\nSłów",
        "Word\nWeights",
        5,
        "TF-IDF: IDF wynalazła Karen Sparck Jones (1972) - jeden z najważniejszych wkładów w IR.",
        "TF-IDF: IDF invented by Karen Sparck Jones (1972) - one of the most important IR contributions.",
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
        "Przestrzeń\nSemantyki",
        "Semantic\nSpace",
        5,
        "Hipoteza dystrybucyjna Harrisa (1954), Word2Vec (2013), bias Bolukbasi (2016).",
        "Harris distributional hypothesis (1954), Word2Vec (2013), Bolukbasi bias (2016).",
    ),
    LessonNode(
        25,
        "Detektyw\nTematów",
        "Topic\nDetective",
        5,
        "LDA: Blei, Ng, Jordan (2003), >40 000 cytowań, BERTopic (2022).",
        "LDA: Blei, Ng, Jordan (2003), >40,000 citations, BERTopic (2022).",
    ),
    LessonNode(
        26,
        "Człowiek\nvs Model",
        "Human\nvs Model",
        5,
        "Schemat Winograda (2011): GPT-4 ~90% vs mniejsze modele ~60%.",
        "Winograd Schema (2011): GPT-4 ~90% vs smaller models ~60%.",
    ),
    # Module 6 - Networks & Ethics (lessons 27-32)
    LessonNode(
        27,
        "Sieć\nSpołeczna",
        "Social\nNetwork",
        6,
        "Małe światy Milgrama (1967), sieci bezskalowe Barabasiego (1999).",
        "Milgram small worlds (1967), Barabasi scale-free networks (1999).",
    ),
    LessonNode(
        28,
        "Dezinfor-\nmacja",
        "Misinfor-\nmation",
        6,
        "SIR Kermacka i McKendricka (1927); fałszywe newsy: R0 wyższe niż prawdziwe.",
        "Kermack & McKendrick SIR (1927); false news has higher R0 than true news.",
    ),
    LessonNode(
        29,
        "Bańka\nRekomend.",
        "Recomm.\nBubble",
        6,
        "Filtrowanie kolaboratywne Goldberga (1992), bańka informacyjna Parisera (2011).",
        "Goldberg collaborative filtering (1992), Pariser filter bubble (2011).",
    ),
    LessonNode(
        30,
        "Ślepa\nStronniczość",
        "Bias\nBlind Spot",
        6,
        "Niemożliwość sprawiedliwości Chouldechovej (2017): 3 kryteria nie mogą być spełnione jednocześnie.",
        "Chouldechova fairness impossibility (2017): 3 criteria cannot all be met simultaneously.",
    ),
    LessonNode(
        31,
        "Byłeś\nDanetem",
        "You Were\nthe Dataset",
        6,
        "Efekt Hawthorne'a (1924), Cambridge Analytica (2018), RODO (2018).",
        "Hawthorne effect (1924), Cambridge Analytica (2018), GDPR (2018).",
    ),
    LessonNode(
        32,
        "Próba\nArchitekta",
        "Architect's\nTrial",
        6,
        "Prawo Goodharta (1975), EU AI Act (2024) - etyka algorytmiczna w praktyce.",
        "Goodhart's Law (1975), EU AI Act (2024) - algorithmic ethics in practice.",
    ),
]

# Conceptual edges: (lesson_num_a, lesson_num_b)
CONCEPT_EDGES: list[tuple[int, int]] = [
    # Within Module 1
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 6),
    # Within Module 2 (executive function chain)
    (7, 8),
    (8, 9),
    (9, 10),
    (10, 11),
    (11, 12),
    # Within Module 3 (stats pipeline)
    (13, 14),
    (14, 15),
    (15, 16),
    # Within Module 4 (ML pipeline)
    (17, 18),
    (18, 19),
    (19, 20),
    # Within Module 5 (NLP pipeline)
    (21, 22),
    (22, 23),
    (23, 24),
    (24, 25),
    (25, 26),
    # Within Module 6 (ethics chain)
    (27, 28),
    (28, 29),
    (29, 30),
    (30, 31),
    (31, 32),
    # Cross-module: RT -> cognitive tasks
    (2, 7),
    (2, 8),
    (2, 9),
    # Cross-module: data quality -> stats
    (4, 13),
    (6, 13),
    # Cross-module: dashboard -> ML
    (12, 17),
    # Cross-module: distributions -> NLP (Zipf)
    (13, 21),
    # Cross-module: hypothesis -> classifier
    (15, 18),
    # Cross-module: overfitting -> feature selection
    (19, 17),
    # Cross-module: embeddings -> topic modeling
    (24, 25),
    # Cross-module: social network -> misinformation
    (27, 28),
    # Cross-module: bias -> ethics
    (30, 32),
    (31, 32),
]

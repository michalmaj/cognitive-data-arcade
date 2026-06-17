from __future__ import annotations

TOPICS: dict[str, dict] = {
    "sport": {
        "label_pl": "Sport",
        "label_en": "Sport",
        "color": (231, 76, 60),
        "words": [
            "bieg", "medal", "trening", "zawodnik", "turniej",
            "rekord", "trener", "stadion", "pilka", "wynik",
            "mecz", "liga",
        ],
    },
    "nauka": {
        "label_pl": "Nauka",
        "label_en": "Science",
        "color": (52, 152, 219),
        "words": [
            "atom", "wzor", "badanie", "teoria", "eksperyment",
            "czastka", "reakcja", "laboratorium", "hipoteza",
            "odkrycie", "pierwiastek", "fala",
        ],
    },
    "zdrowie": {
        "label_pl": "Zdrowie",
        "label_en": "Health",
        "color": (39, 174, 96),
        "words": [
            "dieta", "witamina", "sen", "lekarstwo", "ruch",
            "choroba", "lekarz", "szpital", "odpornosc",
            "profilaktyka", "kaloria", "terapia",
        ],
    },
    "polityka": {
        "label_pl": "Polityka",
        "label_en": "Politics",
        "color": (241, 196, 15),
        "words": [
            "wybory", "ustawa", "rzad", "minister", "partia",
            "parlament", "debata", "koalicja", "opozycja",
            "glosowanie", "senat", "prawo",
        ],
    },
    "tech": {
        "label_pl": "Tech",
        "label_en": "Tech",
        "color": (155, 89, 182),
        "words": [
            "komputer", "algorytm", "siec", "dane", "program",
            "serwer", "model", "baza", "interfejs", "chmura",
            "robot", "sensor",
        ],
    },
}

DOCUMENTS: list[dict] = [
    # sport (3 documents)
    {
        "text_pl": "Zawodnik zdobyl zloty medal na mistrzostwach swiata. Trener swietuje to historyczne zwyciestwo.",
        "dominant": "sport",
        "weights": {"sport": 0.72, "nauka": 0.08, "zdrowie": 0.12, "polityka": 0.03, "tech": 0.05},
    },
    {
        "text_pl": "Liga pilkarska oglosila nowy rekord ogladalnosci. Kibice wypelnili stadion po brzegi.",
        "dominant": "sport",
        "weights": {"sport": 0.68, "nauka": 0.04, "zdrowie": 0.08, "polityka": 0.14, "tech": 0.06},
    },
    {
        "text_pl": "Biegacz pobil swoj osobisty rekord na dystansie maraton. Intensywny trening przynisl efekty.",
        "dominant": "sport",
        "weights": {"sport": 0.75, "nauka": 0.05, "zdrowie": 0.14, "polityka": 0.02, "tech": 0.04},
    },
    # nauka (3 documents)
    {
        "text_pl": "Naukowcy odkryli nowa czastke w eksperymencie akceleratorowym. Teoria wymaga weryfikacji.",
        "dominant": "nauka",
        "weights": {"sport": 0.04, "nauka": 0.74, "zdrowie": 0.08, "polityka": 0.06, "tech": 0.08},
    },
    {
        "text_pl": "Hipoteza naukowa zostala potwierdzona w laboratorium. Wyniki opublikowano w prestizowym czasopismie.",
        "dominant": "nauka",
        "weights": {"sport": 0.03, "nauka": 0.70, "zdrowie": 0.10, "polityka": 0.05, "tech": 0.12},
    },
    {
        "text_pl": "Badanie reakcji chemicznych ujawnilo nowy pierwiastek. Odkrycie zmienia rozumienie atomu.",
        "dominant": "nauka",
        "weights": {"sport": 0.02, "nauka": 0.78, "zdrowie": 0.06, "polityka": 0.04, "tech": 0.10},
    },
    # zdrowie (3 documents)
    {
        "text_pl": "Lekarze zalecaja regularny ruch i zbilansowana diete. Witaminy wzmacniaja odpornosc.",
        "dominant": "zdrowie",
        "weights": {"sport": 0.12, "nauka": 0.08, "zdrowie": 0.70, "polityka": 0.04, "tech": 0.06},
    },
    {
        "text_pl": "Sen jest kluczowy dla regeneracji ciala. Brak snu zwieksza ryzyko chorob sercowych.",
        "dominant": "zdrowie",
        "weights": {"sport": 0.06, "nauka": 0.14, "zdrowie": 0.72, "polityka": 0.03, "tech": 0.05},
    },
    {
        "text_pl": "Nowe lekarstwo przeszlo pomyslnie testy kliniczne. Terapia moze pomoc milionom pacjentow.",
        "dominant": "zdrowie",
        "weights": {"sport": 0.03, "nauka": 0.18, "zdrowie": 0.68, "polityka": 0.05, "tech": 0.06},
    },
    # polityka (3 documents)
    {
        "text_pl": "Wybory parlamentarne przyciagnely rekordowa frekwencje. Koalicja rzadzaca stracila wiekszosc.",
        "dominant": "polityka",
        "weights": {"sport": 0.03, "nauka": 0.04, "zdrowie": 0.05, "polityka": 0.82, "tech": 0.06},
    },
    {
        "text_pl": "Minister oglosil nowa ustawe regulujaca rynek pracy. Opozycja zapowiada debate w parlamencie.",
        "dominant": "polityka",
        "weights": {"sport": 0.02, "nauka": 0.05, "zdrowie": 0.07, "polityka": 0.80, "tech": 0.06},
    },
    {
        "text_pl": "Senat przeglosowal budzet na przyszly rok. Rzad broni swoich decyzji finansowych.",
        "dominant": "polityka",
        "weights": {"sport": 0.03, "nauka": 0.04, "zdrowie": 0.04, "polityka": 0.83, "tech": 0.06},
    },
    # tech (3 documents)
    {
        "text_pl": "Nowy algorytm sztucznej inteligencji bije rekordy na benchmarkach. Model uczy sie na danych z chmury.",
        "dominant": "tech",
        "weights": {"sport": 0.04, "nauka": 0.15, "zdrowie": 0.03, "polityka": 0.04, "tech": 0.74},
    },
    {
        "text_pl": "Firma zaprezentowala nowy interfejs do obslugi robotow. Baza danych przechowuje miliony rekordow.",
        "dominant": "tech",
        "weights": {"sport": 0.03, "nauka": 0.10, "zdrowie": 0.04, "polityka": 0.06, "tech": 0.77},
    },
    {
        "text_pl": "Siec neuronowa nauczona na miliardach parametrow tworzy tekst jak czlowiek. Program analizuje wzory jezyka.",
        "dominant": "tech",
        "weights": {"sport": 0.02, "nauka": 0.12, "zdrowie": 0.03, "polityka": 0.05, "tech": 0.78},
    },
]

# 8 intruder sets: sport x2, nauka x2, zdrowie x2, polityka x1, tech x1
INTRUDER_SETS: list[dict] = [
    {
        "topic": "sport",
        "words": ["bieg", "medal", "trening", "zawodnik", "turniej", "rekord", "trener", "stadion"],
        "intruder": "algorytm",
    },
    {
        "topic": "sport",
        "words": ["pilka", "wynik", "mecz", "liga", "bieg", "turniej", "rekord", "trener"],
        "intruder": "ustawa",
    },
    {
        "topic": "nauka",
        "words": ["atom", "wzor", "badanie", "teoria", "eksperyment", "czastka", "reakcja", "laboratorium"],
        "intruder": "koalicja",
    },
    {
        "topic": "nauka",
        "words": ["hipoteza", "odkrycie", "pierwiastek", "fala", "wzor", "teoria", "reakcja", "badanie"],
        "intruder": "dieta",
    },
    {
        "topic": "zdrowie",
        "words": ["dieta", "witamina", "sen", "lekarstwo", "ruch", "choroba", "lekarz", "szpital"],
        "intruder": "turniej",
    },
    {
        "topic": "zdrowie",
        "words": ["odpornosc", "profilaktyka", "kaloria", "terapia", "sen", "ruch", "lekarz", "choroba"],
        "intruder": "program",
    },
    {
        "topic": "polityka",
        "words": ["wybory", "ustawa", "rzad", "minister", "partia", "parlament", "debata", "koalicja"],
        "intruder": "sensor",
    },
    {
        "topic": "tech",
        "words": ["komputer", "algorytm", "siec", "dane", "program", "model", "baza", "interfejs"],
        "intruder": "wybory",
    },
]

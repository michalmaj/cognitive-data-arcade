# src/cognitive_data_arcade/games/semantic_space/word_data.py
from __future__ import annotations

import math

CLUSTERS: dict[str, dict] = {
    "emocje":    {"color": (155, 89, 182), "label": "Emocje"},
    "zwierzeta": {"color": (39, 174, 96),  "label": "Zwierzęta"},
    "nauka":     {"color": (52, 152, 219), "label": "Nauka"},
    "jedzenie":  {"color": (230, 126, 34), "label": "Jedzenie"},
    "sport":     {"color": (231, 76, 60),  "label": "Sport"},
}

WORDS: dict[str, dict] = {
    # emocje
    "radosc":      {"label": "radość",      "x": 0.12, "y": 0.18, "cluster": "emocje"},
    "szczescie":   {"label": "szczęście",   "x": 0.18, "y": 0.24, "cluster": "emocje"},
    "smutek":      {"label": "smutek",      "x": 0.22, "y": 0.38, "cluster": "emocje"},
    "gniew":       {"label": "gniew",       "x": 0.10, "y": 0.48, "cluster": "emocje"},
    "strach":      {"label": "strach",      "x": 0.15, "y": 0.55, "cluster": "emocje"},
    "nadzieja":    {"label": "nadzieja",    "x": 0.08, "y": 0.30, "cluster": "emocje"},
    "milosc":      {"label": "miłość",      "x": 0.20, "y": 0.15, "cluster": "emocje"},
    "zazdrosc":    {"label": "zazdrość",    "x": 0.28, "y": 0.44, "cluster": "emocje"},
    "spokoj":      {"label": "spokój",      "x": 0.05, "y": 0.22, "cluster": "emocje"},
    "duma":        {"label": "duma",        "x": 0.25, "y": 0.28, "cluster": "emocje"},
    # zwierzeta
    "kot":         {"label": "kot",         "x": 0.62, "y": 0.14, "cluster": "zwierzeta"},
    "pies":        {"label": "pies",        "x": 0.70, "y": 0.22, "cluster": "zwierzeta"},
    "kon":         {"label": "koń",         "x": 0.65, "y": 0.32, "cluster": "zwierzeta"},
    "ptak":        {"label": "ptak",        "x": 0.55, "y": 0.20, "cluster": "zwierzeta"},
    "ryba":        {"label": "ryba",        "x": 0.58, "y": 0.38, "cluster": "zwierzeta"},
    "wilk":        {"label": "wilk",        "x": 0.74, "y": 0.34, "cluster": "zwierzeta"},
    "lew":         {"label": "lew",         "x": 0.78, "y": 0.18, "cluster": "zwierzeta"},
    "slon":        {"label": "słoń",        "x": 0.72, "y": 0.44, "cluster": "zwierzeta"},
    "mysz":        {"label": "mysz",        "x": 0.60, "y": 0.48, "cluster": "zwierzeta"},
    "zaba":        {"label": "żaba",        "x": 0.52, "y": 0.42, "cluster": "zwierzeta"},
    # nauka
    "badania":     {"label": "badania",     "x": 0.38, "y": 0.68, "cluster": "nauka"},
    "wiedza":      {"label": "wiedza",      "x": 0.45, "y": 0.75, "cluster": "nauka"},
    "odkrycie":    {"label": "odkrycie",    "x": 0.35, "y": 0.80, "cluster": "nauka"},
    "teoria":      {"label": "teoria",      "x": 0.50, "y": 0.70, "cluster": "nauka"},
    "eksperyment": {"label": "eksperyment", "x": 0.30, "y": 0.72, "cluster": "nauka"},
    "dane":        {"label": "dane",        "x": 0.55, "y": 0.78, "cluster": "nauka"},
    "hipoteza":    {"label": "hipoteza",    "x": 0.42, "y": 0.85, "cluster": "nauka"},
    "wynik":       {"label": "wynik",       "x": 0.48, "y": 0.82, "cluster": "nauka"},
    "analiza":     {"label": "analiza",     "x": 0.38, "y": 0.88, "cluster": "nauka"},
    "model":       {"label": "model",       "x": 0.60, "y": 0.85, "cluster": "nauka"},
    # jedzenie
    "chleb":       {"label": "chleb",       "x": 0.78, "y": 0.65, "cluster": "jedzenie"},
    "jablko":      {"label": "jabłko",      "x": 0.85, "y": 0.58, "cluster": "jedzenie"},
    "zupa":        {"label": "zupa",        "x": 0.72, "y": 0.72, "cluster": "jedzenie"},
    "mieso":       {"label": "mięso",       "x": 0.80, "y": 0.75, "cluster": "jedzenie"},
    "ryz":         {"label": "ryż",         "x": 0.88, "y": 0.70, "cluster": "jedzenie"},
    "kawa":        {"label": "kawa",        "x": 0.68, "y": 0.60, "cluster": "jedzenie"},
    "herbata":     {"label": "herbata",     "x": 0.75, "y": 0.58, "cluster": "jedzenie"},
    "ciasto":      {"label": "ciasto",      "x": 0.82, "y": 0.82, "cluster": "jedzenie"},
    "warzywo":     {"label": "warzywo",     "x": 0.88, "y": 0.62, "cluster": "jedzenie"},
    "owoc":        {"label": "owoc",        "x": 0.90, "y": 0.55, "cluster": "jedzenie"},
    # sport
    "pilka":       {"label": "piłka",       "x": 0.22, "y": 0.82, "cluster": "sport"},
    "bieg":        {"label": "bieg",        "x": 0.15, "y": 0.88, "cluster": "sport"},
    "tenis":       {"label": "tenis",       "x": 0.28, "y": 0.92, "cluster": "sport"},
    "skoki":       {"label": "skoki",       "x": 0.10, "y": 0.80, "cluster": "sport"},
    "plywanie":    {"label": "pływanie",    "x": 0.08, "y": 0.92, "cluster": "sport"},
    "druzyna":     {"label": "drużyna",     "x": 0.30, "y": 0.85, "cluster": "sport"},
    "trening":     {"label": "trening",     "x": 0.18, "y": 0.75, "cluster": "sport"},
    "mecz":        {"label": "mecz",        "x": 0.35, "y": 0.75, "cluster": "sport"},
    "zwyciestwo":  {"label": "zwycięstwo",  "x": 0.25, "y": 0.70, "cluster": "sport"},
    "stadion":     {"label": "stadion",     "x": 0.12, "y": 0.68, "cluster": "sport"},
}


def _compute_similarities() -> dict[str, list[tuple[str, float]]]:
    """Derive similarity scores from (x,y) distance + same-cluster bonus, scale to [0.10, 0.95]."""
    result: dict[str, list[tuple[str, float]]] = {}
    word_items = list(WORDS.items())
    for key, wd in word_items:
        scores: list[tuple[str, float]] = []
        for other_key, other_wd in word_items:
            if other_key == key:
                continue
            dist = math.sqrt((wd["x"] - other_wd["x"]) ** 2 + (wd["y"] - other_wd["y"]) ** 2)
            bonus = 0.5 if wd["cluster"] == other_wd["cluster"] else 0.0
            scores.append((other_key, bonus - 0.5 * dist))
        scores.sort(key=lambda t: -t[1])
        top8 = scores[:8]
        raws = [s for _, s in top8]
        lo, hi = min(raws), max(raws)
        if hi == lo:
            result[key] = [(k, 0.50) for k, _ in top8]
        else:
            result[key] = [
                (k, round(0.10 + (s - lo) / (hi - lo) * 0.85, 2))
                for k, s in top8
            ]
    return result


SIMILARITIES: dict[str, list[tuple[str, float]]] = _compute_similarities()

# Words that semantically bridge two clusters — used by bridge mission type.
# Each entry: (word_key, [cluster_a, cluster_b], difficulty)
BRIDGE_WORDS: list[tuple[str, list[str], int]] = [
    ("wynik",      ["nauka", "sport"],   2),
    ("mecz",       ["sport", "nauka"],   2),
    ("trening",    ["sport", "nauka"],   3),
    ("druzyna",    ["sport", "emocje"],  3),
]

# (a, b, c, correct_answer, [wrong1, wrong2, wrong3], explanation_pl, explanation_en)
ANALOGIES: list[tuple] = [
    (
        "Paryż", "Francja", "Polska", "Warszawa",
        ["Kraków", "Berlin", "Praga"],
        "Stolica kraju — relacja geograficzna zakodowana w wektorach.",
        "Capital city relation — encoded in word vectors.",
    ),
    (
        "pies", "szczenię", "kot", "kotek",
        ["kocur", "kociak", "kotka"],
        "Dorosły–młody: embeddingi kodują wzorce morfologiczne.",
        "Adult–young: embeddings encode morphological patterns.",
    ),
    (
        "piłkarz", "boisko", "tenisista", "kort",
        ["trampolina", "stadion", "tor"],
        "Sport–miejsce gry: analogia kontekstowa.",
        "Sport–venue analogy encoded in context.",
    ),
    (
        "radość", "szczęście", "smutek", "żal",
        ["gniew", "strach", "ból"],
        "Synonim emocji — bliskość semantyczna działa jak lustro.",
        "Emotion synonym — semantic proximity works like a mirror.",
    ),
]

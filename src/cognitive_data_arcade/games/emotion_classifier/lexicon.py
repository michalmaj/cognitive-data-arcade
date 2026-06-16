# src/cognitive_data_arcade/games/emotion_classifier/lexicon.py
from __future__ import annotations

LEXICON: dict[str, int] = {
    # +2: strongly positive
    "doskonaly": 2, "doskonale": 2, "doskonala": 2,
    "znakomity": 2, "znakomite": 2, "znakomita": 2,
    "swietny": 2, "swietnie": 2, "swietna": 2,
    "rewelacyjny": 2, "rewelacyjne": 2, "rewelacyjna": 2,
    "fantastyczny": 2, "fantastyczne": 2, "fantastyczna": 2,
    "genialny": 2, "genialne": 2, "genialnie": 2,
    "perfekcyjny": 2, "perfekcyjnie": 2,
    "sukces": 2, "sukcesem": 2,
    "imponujacy": 2, "imponujace": 2,
    "rewelacja": 2,
    "super": 2,
    # +1: mildly positive
    "dobry": 1, "dobre": 1, "dobra": 1, "dobrze": 1,
    "pozytywny": 1, "pozytywne": 1, "pozytywnie": 1, "pozytywna": 1,
    "zadowolony": 1, "zadowoleni": 1, "zadowolenie": 1, "zadowolenia": 1,
    "trafny": 1, "trafne": 1,
    "szybki": 1, "szybko": 1,
    "uzyteczny": 1, "uzyteczne": 1, "uzyteczna": 1,
    "ciekawy": 1, "ciekawe": 1,
    "udany": 1, "udane": 1,
    "niezle": 1, "niezla": 1, "niezly": 1,
    "poprawny": 1, "poprawnie": 1, "poprawna": 1,
    "brawo": 1,
    # -1: mildly negative
    "trudny": -1, "trudne": -1, "trudno": -1, "trudnosci": -1,
    "slaby": -1, "slabe": -1, "slabo": -1,
    "powolny": -1, "powolnie": -1,
    "blad": -1, "bledna": -1, "bledow": -1, "bledami": -1,
    "problem": -1, "problemy": -1, "problemow": -1,
    "watpliwy": -1, "watpliwe": -1, "watpliwosci": -1,
    "rozczarowujacy": -1, "rozczarowujace": -1, "rozczarowani": -1,
    "zle": -1,
    # -2: strongly negative
    "fatalny": -2, "fatalne": -2, "fatalnie": -2,
    "katastrofa": -2, "katastroficzny": -2, "katastroficzne": -2,
    "tragiczny": -2, "tragiczne": -2, "tragicznie": -2,
    "koszmarny": -2, "koszmarne": -2, "koszmarnie": -2,
    "bezuzyteczny": -2, "bezuzyteczne": -2, "bezuzyteczna": -2,
    "porazka": -2,
    "klapa": -2,
}

TRAP_LABELS: dict[str, str] = {
    "clear_pos": "LATWY: Pozytywny",
    "clear_neg": "LATWY: Negatywny",
    "negation":  "PULAPKA: Negacja",
    "intensity": "PULAPKA: Intensywnosc",
    "irony":     "PULAPKA: Ironia",
    "mixed":     "PULAPKA: Mieszany",
}

TRAP_HINTS: dict[str, str] = {
    "clear_pos": "To zdanie ma wyrazne slowa pozytywne. Powinno byc latwe.",
    "clear_neg": "To zdanie ma wyrazne slowa negatywne. Powinno byc latwe.",
    "negation":  "To zdanie zawiera slowo negujace. Czy leksykon je zauwazy?",
    "intensity": "Uwaga na stopniowanie — czy 'dobry' i 'doskonaly' to to samo?",
    "irony":     "Czy to zdanie brzmi zbyt pozytywnie jak na kontekst?",
    "mixed":     "To zdanie laczy kilka trudnosci naraz.",
}


def classify(word_scores: dict[str, int]) -> tuple[str, int]:
    """Return (verdict, total_score). verdict in {'positive','negative','neutral'}."""
    total = sum(word_scores.values())
    if total > 0:
        return "positive", total
    if total < 0:
        return "negative", total
    return "neutral", total


def compute_round_score(
    tagged_words: dict[str, str],
    word_scores: dict[str, int],
    truth: str,
    elapsed_s: float,
) -> tuple[int, int, int, int]:
    """Return (correct_pts, wrong_pts, beat_bonus, speed_bonus).

    wrong_pts is <= 0 (penalty per wrong tag is -2).
    beat_bonus is 15 if player verdict == truth and lexicon verdict != truth.
    speed_bonus is 5 if elapsed_s < 15.0.
    """
    correct_pts = 0
    wrong_pts = 0
    for word, player_tag in tagged_words.items():
        lex_score = word_scores.get(word, 0)
        if lex_score == 0:
            continue
        expected_tag = "positive" if lex_score > 0 else "negative"
        if player_tag == expected_tag:
            correct_pts += 5
        else:
            wrong_pts -= 2

    player_ws = {w: LEXICON[w] for w in tagged_words if w in LEXICON}
    player_verdict, _ = classify(player_ws)
    lexicon_verdict, _ = classify(word_scores)
    beat_bonus = 15 if (player_verdict == truth and lexicon_verdict != truth) else 0
    speed_bonus = 5 if elapsed_s < 15.0 else 0
    return correct_pts, wrong_pts, beat_bonus, speed_bonus

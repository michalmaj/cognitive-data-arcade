# src/cognitive_data_arcade/games/emotion_classifier/lexicon.py
from __future__ import annotations

LEXICON: dict[str, int] = {
    # +2: strongly positive
    "doskonały": 2, "doskonale": 2, "doskonała": 2,
    "znakomity": 2, "znakomite": 2, "znakomita": 2,
    "świetny": 2, "świetnie": 2, "świetna": 2,
    "rewelacyjny": 2, "rewelacyjne": 2, "rewelacyjna": 2,
    "fantastyczny": 2, "fantastyczne": 2, "fantastyczna": 2,
    "genialny": 2, "genialne": 2, "genialnie": 2,
    "perfekcyjny": 2, "perfekcyjnie": 2,
    "sukces": 2, "sukcesem": 2,
    "imponujący": 2, "imponujące": 2,
    "rewelacja": 2,
    "super": 2,
    # +1: mildly positive
    "dobry": 1, "dobre": 1, "dobra": 1, "dobrze": 1,
    "pozytywny": 1, "pozytywne": 1, "pozytywnie": 1, "pozytywna": 1,
    "zadowolony": 1, "zadowoleni": 1, "zadowolenie": 1, "zadowolenia": 1,
    "trafny": 1, "trafne": 1,
    "szybki": 1, "szybko": 1,
    "użyteczny": 1, "użyteczne": 1, "użyteczna": 1,
    "ciekawy": 1, "ciekawe": 1,
    "udany": 1, "udane": 1,
    "nieźle": 1, "nieźła": 1, "nieźły": 1,
    "poprawny": 1, "poprawnie": 1, "poprawna": 1,
    "brawo": 1,
    # -1: mildly negative
    "trudny": -1, "trudne": -1, "trudno": -1, "trudności": -1,
    "słaby": -1, "słabe": -1, "słabo": -1,
    "powolny": -1, "powolnie": -1,
    "błąd": -1, "błędna": -1, "błędów": -1, "błędami": -1,
    "problem": -1, "problemy": -1, "problemów": -1,
    "wątpliwy": -1, "wątpliwe": -1, "wątpliwości": -1,
    "rozczarowujący": -1, "rozczarowujące": -1, "rozczarowani": -1,
    "źle": -1,
    # -2: strongly negative
    "fatalny": -2, "fatalne": -2, "fatalnie": -2,
    "katastrofa": -2, "katastroficzny": -2, "katastroficzne": -2,
    "tragiczny": -2, "tragiczne": -2, "tragicznie": -2,
    "koszmarny": -2, "koszmarne": -2, "koszmarnie": -2,
    "bezużyteczny": -2, "bezużyteczne": -2, "bezużyteczna": -2,
    "porażka": -2,
    "klapa": -2,
}

TRAP_LABELS: dict[str, str] = {
    "clear_pos": "ŁATWY: Pozytywny",
    "clear_neg": "ŁATWY: Negatywny",
    "negation":  "PUŁAPKA: Negacja",
    "intensity": "PUŁAPKA: Intensywność",
    "irony":     "PUŁAPKA: Ironia",
    "mixed":     "PUŁAPKA: Mieszany",
}

TRAP_HINTS: dict[str, str] = {
    "clear_pos": "To zdanie ma wyraźne słowa pozytywne. Powinno być łatwe.",
    "clear_neg": "To zdanie ma wyraźne słowa negatywne. Powinno być łatwe.",
    "negation":  "To zdanie zawiera słowo negujące. Czy leksykon je zauważy?",
    "intensity": "Uwaga na stopniowanie — czy 'dobry' i 'doskonały' to to samo?",
    "irony":     "Czy to zdanie brzmi zbyt pozytywnie jak na kontekst?",
    "mixed":     "To zdanie łączy kilka trudności naraz.",
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

    player_ws = {w: word_scores[w] for w in tagged_words if w in word_scores}
    player_verdict, _ = classify(player_ws)
    lexicon_verdict, _ = classify(word_scores)
    beat_bonus = 15 if (player_verdict == truth and lexicon_verdict != truth) else 0
    speed_bonus = 5 if elapsed_s < 15.0 else 0
    return correct_pts, wrong_pts, beat_bonus, speed_bonus

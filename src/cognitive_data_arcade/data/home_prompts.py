# src/cognitive_data_arcade/data/home_prompts.py
"""Per-module suggestions for between-session home activity. Index = module_idx (0-based)."""

from __future__ import annotations

HOME_PROMPTS: dict[int, dict[str, str]] = {
    0: {
        "pl": (
            "Zrob Daily Challenge 3x w tym tygodniu.\n"
            "Otworz swoj plik CSV z RT Lab w notatniku i znajdz najszybsza probe.\n"
            "Pobij swoj sredni czas reakcji - zagraj jeszcze raz w innych warunkach."
        ),
        "en": (
            "Complete Daily Challenge 3x this week.\n"
            "Open your RT Lab CSV in a text editor and find your fastest trial.\n"
            "Beat your mean reaction time - play again under different conditions."
        ),
    },
    1: {
        "pl": (
            "Zrob Daily Challenge 3x w tym tygodniu.\n"
            "Sprobuj przejsc N-Back na poziom wyzszy niz ostatnio.\n"
            "Zagraj w Go/No-Go i porownaj wskaznik falszywie pozytywnych z poprzednia sesja."
        ),
        "en": (
            "Complete Daily Challenge 3x this week.\n"
            "Try to clear N-Back at one level higher than your last session.\n"
            "Play Go/No-Go and compare your false-alarm rate with your previous session."
        ),
    },
    2: {
        "pl": (
            "Zrob Daily Challenge 3x w tym tygodniu.\n"
            "W Distribution Playground: wyprobuj rozklad, ktorego jeszcze nie uzywales.\n"
            "Zapisz jeden przyklad z zycia, ktory ilustruje pulapke korelacji z lekcji 14."
        ),
        "en": (
            "Complete Daily Challenge 3x this week.\n"
            "In Distribution Playground: try a distribution you haven't used before.\n"
            "Write down one real-life example that illustrates the correlation trap from lesson 14."
        ),
    },
    3: {
        "pl": (
            "Zrob Daily Challenge 3x w tym tygodniu.\n"
            "W Overfitting Monster: znajdz punkt, w ktorym model przestaje sie przetrenowywac.\n"
            "W Feature Hunter: sprobuj uzyc tylko 3 cech i porownaj wynik z pelnym zestawem."
        ),
        "en": (
            "Complete Daily Challenge 3x this week.\n"
            "In Overfitting Monster: find the exact point where the model stops overfitting.\n"
            "In Feature Hunter: try using only 3 features and compare the score with the full set."
        ),
    },
    4: {
        "pl": (
            "Zrob Daily Challenge 3x w tym tygodniu.\n"
            "W Semantic Space Explorer: znajdz 3 pary slow o zaskakujacym podobienstwie.\n"
            "Zapisz jeden blad klasyfikatora sentymentu, ktory wydaje ci sie nieoczekiwany."
        ),
        "en": (
            "Complete Daily Challenge 3x this week.\n"
            "In Semantic Space Explorer: find 3 word pairs with a surprisingly high similarity.\n"
            "Write down one sentiment classifier error that surprised you."
        ),
    },
    5: {
        "pl": (
            "Zrob Daily Challenge 3x w tym tygodniu.\n"
            "W Recommendation Bubble: porownaj wynik roznorodnosci przy maksymalnym i minimalnym filtrze.\n"
            "Napisz jeden akapit odpowiedzi na pytanie refleksyjne z The Architect's Trial."
        ),
        "en": (
            "Complete Daily Challenge 3x this week.\n"
            "In Recommendation Bubble: compare diversity scores with max vs. min filter settings.\n"
            "Write one paragraph in response to the reflection question from The Architect's Trial."
        ),
    },
}

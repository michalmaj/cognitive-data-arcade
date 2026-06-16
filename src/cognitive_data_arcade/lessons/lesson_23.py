# src/cognitive_data_arcade/lessons/lesson_23.py
"""Lesson 23 -- Emotion Classifier (lexicon-based sentiment analysis)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Klasyfikator leksykonowy przypisuje sentyment na podstawie słownika słów z wagami. "
            "Każde słowo dostaje wartość liczbową: +2 = bardzo pozytywne, -2 = bardzo negatywne. "
            "Suma wag otagowanych słów decyduje o wyniku.",
            "Algorytm jest prosty: suma > 0 → pozytywny, suma < 0 → negatywny, suma = 0 → neutralny. "
            "Nie ma tu żadnego rozumienia zdania jako całości — tylko lokalne dopasowanie słów.",
            "Trzy główne pułapki leksykonu: negacja ('nie dobry' ≠ 'dobry'), "
            "intensywność ('dobry' ≠ 'doskonały'), ironia ('Świetna robota' może być sarkazmem).",
            "Modele ML (np. BERT, RoBERTa) uczą się z kontekstu całego zdania. "
            "Potrafią wykrywać negację, intensywność i ironię, których leksykon nigdy nie zrozumie.",
        ],
        "notes": [
            "Leksykony są nadal stosowane w produkcji, gdy szybkość i interpretowalność "
            "są ważniejsze niż dokładność (np. monitoring mediów społecznościowych w czasie rzeczywistym).",
            "Popularne leksykony: VADER (angielski), SentiWordNet (wielojęzyczny), "
            "Słownik Nacechowania Emocjonalnego (polski).",
        ],
        "tasks": [
            "Zagraj w Emotion Classifier — w której kategorii pułapek leksykon mylił się najczęściej?",
            "Napisz 3 własne zdania w stylu 'negacja', 'ironia', 'intensywność' po polsku "
            "i sprawdź, jak leksykon je oceniłby.",
            "Porównaj wynik leksykonu z wynikiem modelu BERT dla tego samego zdania z negacją. "
            "Czym różni się klasyfikacja?",
        ],
    },
    "en": {
        "theory": [
            "A lexicon-based classifier assigns sentiment using a dictionary of words with weights. "
            "Each word gets a numeric score: +2 = strongly positive, -2 = strongly negative. "
            "The sum of tagged word weights decides the verdict.",
            "The algorithm is simple: sum > 0 → positive, sum < 0 → negative, sum = 0 → neutral. "
            "There is no understanding of the sentence as a whole — just local keyword matching.",
            "Three main lexicon pitfalls: negation ('not good' ≠ 'good'), "
            "intensity ('good' ≠ 'excellent'), irony ('Great job' can be sarcasm).",
            "ML models (e.g., BERT, RoBERTa) learn from full sentence context. "
            "They can detect negation, intensity and irony that a simple lexicon will never understand.",
        ],
        "notes": [
            "Lexicons are still used in production when speed and interpretability matter more "
            "than accuracy (e.g., real-time social media monitoring).",
            "Popular lexicons: VADER (English), SentiWordNet (multilingual), "
            "Emotional Valence Dictionary (Polish).",
        ],
        "tasks": [
            "Play Emotion Classifier — which trap category fooled the lexicon most often?",
            "Write 3 sentences in Polish with 'negation', 'irony', and 'intensity' traps "
            "and predict how the lexicon would score them.",
            "Compare a lexicon verdict vs. BERT for a sentence with negation. What's different?",
        ],
    },
}

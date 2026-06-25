"""Lesson 23 - Emotion Classifier (lexicon-based sentiment analysis)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Klasyfikator leksykonowy przypisuje sentyment na podstawie słownika słów z wagami. Każde słowo dostaje wartość liczbową: +2 = bardzo pozytywne, -2 = bardzo negatywne. Suma wag otagowanych słów decyduje o wyniku.",
            "Algorytm jest prosty: suma > 0 = pozytywny, suma < 0 = negatywny, suma = 0 = neutralny. Nie ma tu żadnego rozumienia zdania jako całości - tylko lokalne dopasowanie słów.",
            "Trzy główne pułapki leksykonu: negacja ('nie dobry' nie równa się 'dobry'), intensywność ('dobry' nie równa się 'doskonały'), ironia ('Świetna robota' może być sarkazmem). Prosty leksykon nie radzi sobie z żadną z tych pułapek.",
            "VADER (Hutto i Gilbert, 2014) - Valence Aware Dictionary and sEntiment Reasoner. Opracowany specjalnie dla mediów społecznościowych, obsługuje wielkie litery (WIELKIE = intensywność), wykrzykniki i emotikony. Jeden z najczęściej stosowanych leksykonów w badaniach social media.",
            "Pang i in. (2002) i Turney (2002) niezależnie zaproponowali uczenie maszynowe do analizy sentymentu. Pang zebrał 700 pozytywnych i 700 negatywnych recenzji filmowych z IMDb; Turney używał analogii semantycznych. Te dwa artykuły z 2002 roku zapoczątkowały nowoczesne uczenie maszynowe dla sentymentu.",
            "Modele ML (np. BERT, RoBERTa) uczą się z kontekstu całego zdania. Potrafią wykrywać negację, intensywność i ironię, których leksykon nigdy nie zrozumie. BERT (Devlin i in., 2018) uzyskał przełomowe wyniki na benchmarkach analizy sentymentu, bijąc dotychczasowe SOTA o ponad 5 punktów procentowych.",
        ],
        "notes": [
            "Leksykony są nadal stosowane w produkcji, gdy szybkość i interpretowalność są ważniejsze niż dokładność (np. monitoring mediów społecznościowych w czasie rzeczywistym).",
            "Popularne leksykony: VADER (angielski), SentiWordNet (wielojęzyczny), Słownik Nacechowania Emocjonalnego (polski). SentiWordNet (Baccianella i in., 2010) przypisuje wyniki sentymentu do synsetów WordNet z uwzględnieniem części mowy.",
        ],
        "tasks": [
            "Zagraj w Emotion Classifier - w której kategorii pułapek leksykon mylił się najczęściej?",
            "Sformułuj 3 zdania - po jednym dla każdej pułapki (negacja, ironia, intensywność) - i przewidź, jak leksykon je oceni. Sprawdź wynik.",
            "Porównaj wynik leksykonu z wynikiem modelu BERT dla zdania z negacją. Czym różni się klasyfikacja?",
        ],
    },
    "en": {
        "theory": [
            "A lexicon-based classifier assigns sentiment using a dictionary of words with weights. Each word gets a numeric score: +2 = strongly positive, -2 = strongly negative. The sum of tagged word weights decides the verdict.",
            "The algorithm is simple: sum > 0 = positive, sum < 0 = negative, sum = 0 = neutral. There is no understanding of the sentence as a whole - just local keyword matching.",
            "Three main lexicon pitfalls: negation ('not good' does not equal 'good'), intensity ('good' does not equal 'excellent'), irony ('Great job' can be sarcasm). A simple lexicon cannot handle any of these.",
            "VADER (Hutto and Gilbert, 2014) - Valence Aware Dictionary and sEntiment Reasoner. Designed specifically for social media, it handles capitalisation (ALL-CAPS = intensity), exclamation marks, and emoticons. One of the most widely used lexicons in social media research.",
            "Pang et al. (2002) and Turney (2002) independently proposed machine learning for sentiment analysis. Pang collected 700 positive and 700 negative movie reviews from IMDb; Turney used semantic analogies. These two 2002 papers launched modern ML-based sentiment analysis.",
            "ML models (e.g., BERT, RoBERTa) learn from full sentence context. They can detect negation, intensity and irony that a simple lexicon will never understand. BERT (Devlin et al., 2018) achieved breakthrough results on sentiment benchmarks, exceeding previous state-of-the-art by more than 5 percentage points.",
        ],
        "notes": [
            "Lexicons are still used in production when speed and interpretability matter more than accuracy (e.g., real-time social media monitoring).",
            "Popular lexicons: VADER (English), SentiWordNet (multilingual), Emotional Valence Dictionary (Polish). SentiWordNet (Baccianella et al., 2010) assigns sentiment scores to WordNet synsets with part-of-speech specificity.",
        ],
        "tasks": [
            "Play Emotion Classifier - which trap category fooled the lexicon most often?",
            "Formulate 3 sentences - one for each trap (negation, irony, intensity) - and predict how the lexicon will score them. Check the result.",
            "Compare a lexicon verdict vs. BERT for a sentence with negation. What is different about the classification?",
        ],
    },
}

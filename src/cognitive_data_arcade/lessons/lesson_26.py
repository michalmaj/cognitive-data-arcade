"""Lesson 26 - Human vs Model Challenge (language model failure modes)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Model językowy to maszyna do przewidywania następnego słowa na podstawie statystyk. Nie 'rozumie' tekstu - uczy się wzorców z miliardów zdań. To wystarcza do wielu zadań, ale zawodzi gdy potrzebna jest logika lub kontekst.",
            "Negacja to systematyczna słaba strona modeli. 'Nie był zły film' zawiera słowo 'zły', które model może skojarzyć z negatywnym sentymentem - ignorując 'nie'. Proste klasyfikatory sentymentu mylą się na tego typu zdaniach w 30-40% przypadków.",
            "Sarkazm i ironia wymagają znajomości kontekstu kulturowego i tonu, którego model nie 'słyszy'. Zdanie 'No jasne, to genialny pomysł...' - model widzi 'genialny', nie słyszy ironii. Idiomy są podobnym wyzwaniem: 'kopać się z koniem' to nie fizyka.",
            "Schemat Winograda (Levesque i in., 2011) - test zdrowego rozsądku dla modeli językowych. Przykład: 'Trofeum nie zmieściło się w walizce, bo było za duże.' Które 'ono' jest za duże? Dla człowieka to oczywiste (trofeum), model musi rozumieć semantykę wielkości. GPT-4 rozwiązuje ok. 90% przypadków, mniejsze modele - ok. 60%.",
            "Argument Chińskiego Pokoju (Searle, 1980) - filozoficzny argument, że model wykonujący poprawne operacje na symbolach nie 'rozumie' ich znaczenia, tak jak osoba w pokoju odpowiadająca na chińskie pytania za pomocą słownika nie rozumie chińskiego.",
            "Dlaczego ludzie wciąż wygrywają z modelami na trudnych przypadkach? Bo dysponujemy wspólnymi doświadczeniami, intuicjami językowymi i zdolnością rozumowania przyczynowego. AI jest świetna w typowych przypadkach, człowiek - na krawędzi rozkładu.",
        ],
        "notes": [
            "Większe modele (GPT-4, Claude) radzą sobie lepiej z negacją i sarkazmem niż małe klasyfikatory, ale wciąż zawodzą na bardzo specyficznych przypadkach kulturowych lub zdaniach wieloznacznych. Rozmiar modelu nie rozwiązuje problemu rozumienia - opóźnia tylko punkt porażki.",
            "Benchmarki NLP (GLUE, SuperGLUE) mierzą średnie wyniki na dużych zbiorach testowych. Dobry wynik benchmarkowy nie gwarantuje odporności na krawędzi rozkładu - dlatego testy adversarialne i red-teaming są niezbędne przed wdrożeniem modelu.",
        ],
        "tasks": [
            "Znajdź zdanie, na którym chatbot się myli - użyj negacji lub sarkazmu. Zapisz zdanie, odpowiedź modelu i poprawną odpowiedź. Co model 'zobaczył' zamiast sensu?",
            "Wyjaśnij, dlaczego sarkazm jest trudny dla modelu językowego. Co musi wiedzieć człowiek, żeby rozpoznać sarkazm w tekście bez kontekstu głosu?",
            "Zaprojektuj test, który niezawodnie zmyli klasyfikator sentymentu. Napisz 3 zdania: jedno z negacją, jedno sarkazm, jedno idiom. Sprawdź na dowolnym darmowym narzędziu NLP online.",
        ],
    },
    "en": {
        "theory": [
            "A language model is a next-word prediction machine trained on statistics. It does not 'understand' text - it learns patterns from billions of sentences. This is enough for many tasks, but fails when logic or context is required.",
            "Negation is a systematic weakness of language models. 'It was not a bad film' contains 'bad', which the model may associate with negative sentiment - ignoring 'not'. Simple sentiment classifiers misclassify such sentences in 30-40% of cases.",
            "Sarcasm and irony require cultural context and tone that a model cannot 'hear'. 'Oh sure, that is a brilliant idea...' - the model sees 'brilliant', not sarcasm. Idioms are a similar challenge: figurative language is processed literally.",
            "The Winograd Schema Challenge (Levesque et al., 2011) - a common-sense test for language models. Example: 'The trophy did not fit in the suitcase because it was too big.' What is 'it'? For a human it is obvious (the trophy), but the model must understand size semantics. GPT-4 solves approximately 90% of cases; smaller models approximately 60%.",
            "The Chinese Room argument (Searle, 1980) - a philosophical argument that a model executing correct operations on symbols does not 'understand' their meaning, just as a person in a room answering Chinese questions using a dictionary does not understand Chinese.",
            "Why do humans still beat models on hard cases? Because shared experiences, linguistic intuition, and causal reasoning are available to humans. AI excels at typical cases; humans excel at the tail of the distribution.",
        ],
        "notes": [
            "Larger models (GPT-4, Claude) handle negation and sarcasm better than small classifiers, but still fail on very specific cultural cases or ambiguous sentences. Model size does not solve understanding - it only delays the failure point.",
            "NLP benchmarks (GLUE, SuperGLUE) measure average performance on large test sets. A good benchmark score does not guarantee robustness at the edge of the distribution - that is why adversarial tests and red-teaming are essential before deployment.",
        ],
        "tasks": [
            "Find a sentence that fools a chatbot - use negation or sarcasm. Record the sentence, the model's answer, and the correct answer. What did the model 'see' instead of the meaning?",
            "Explain why sarcasm is hard for a language model. What does a human need to know to detect sarcasm in text without vocal tone?",
            "Design a test that reliably fools a sentiment classifier. Write 3 sentences: one with negation, one sarcasm, one idiom. Test on any free NLP tool online.",
        ],
    },
}

REFLECTION = {
    "pl": {
        "title": "Human vs Model Challenge — Refleksja",
        "cards": [
            {
                "label": "Ograniczenia modeli",
                "color": "indigo",
                "text": "Model językowy przewiduje następne słowo ze statystyk — nie 'rozumie'. Negacja ('nie był zły film') zawiera 'zły' — model kojarzy je z negatywem bez 'nie'. Błąd w 30-40% przypadków.",
            },
            {
                "label": "Schemat Winograda",
                "color": "orange",
                "text": "Levesque (2011): 'Trofeum nie zmieściło się w walizce, bo było za duże.' GPT-4 rozwiązuje ~90%, małe modele ~60%. Potrzebne jest rozumowanie o świecie, nie statystyka słów.",
            },
            {
                "label": "Chiński pokój",
                "color": "green",
                "text": "Searle (1980): system wykonujący poprawne operacje na symbolach nie 'rozumie' ich znaczenia. Modele są świetne na centrum rozkładu — zawodzą na krawędziach: sarkazm, ironia, kontekst kulturowy.",
            },
        ],
        "question": "Model LLM osiąga 94% na benchmarku NLI, ale zawodzi na zdaniach z podwójną negacją. Jak zaprojektujesz test odróżniający 'rozumienie' od 'statystycznego dopasowania wzorca'?",
    },
    "en": {
        "title": "Human vs Model Challenge — Reflection",
        "cards": [
            {
                "label": "Model limitations",
                "color": "indigo",
                "text": "A language model predicts the next word from statistics — it does not 'understand'. Negation ('not a bad film') contains 'bad' — the model associates it with negative sentiment without 'not'. Error in 30–40% of cases.",
            },
            {
                "label": "Winograd schema",
                "color": "orange",
                "text": "Levesque (2011): 'The trophy did not fit in the suitcase because it was too big.' GPT-4 solves ~90%, small models ~60%. World-knowledge reasoning is needed, not word statistics.",
            },
            {
                "label": "Chinese Room",
                "color": "green",
                "text": "Searle (1980): a system performing correct operations on symbols does not 'understand' their meaning. Models excel at the centre of the distribution — they fail at the edges: sarcasm, irony, cultural context.",
            },
        ],
        "question": "An LLM achieves 94% on an NLI benchmark but fails on sentences with double negation. How would you design a test that distinguishes 'understanding' from 'statistical pattern matching'?",
    },
}

"""Lesson 26 - Human vs Model Challenge (language model failure modes)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Model językowy to maszyna do przewidywania następnego słowa na podstawie statystyk. "
            "Nie 'rozumie' tekstu - uczy się wzorców z miliardów zdań. "
            "To wystarcza do wielu zadań, ale zawodzi gdy potrzebna jest logika lub kontekst.",
            "Negacja to systematyczna słaba strona modeli. 'Nie był zły film' zawiera słowo 'zły', "
            "które model może skojarzyć z negatywnym sentymentem - ignorując 'nie'. "
            "Proste klasyfikatory sentymentu mylą się na tego typu zdaniach w 30-40% przypadków.",
            "Sarkazm i ironia wymagają znajomości kontekstu kulturowego i tonu, którego model nie 'słyszy'. "
            "Zdanie 'No jasne, to genialny pomysł...' - model widzi 'genialny', nie słyszy ironii. "
            "Idiomy i zwroty frazeologiczne są podobnym wyzwaniem: 'kopać się z koniem' to nie fizyka.",
            "Dlaczego ludzie wciąż wygrywają z modelami na trudnych przypadkach? "
            "Bo mamy wspólne doświadczenia, intuicje językowe i zdolność do rozumowania przyczynowego. "
            "AI jest świetna w typowych przypadkach, człowiek - w krawędzi rozkładu.",
        ],
        "notes": [
            "Większe modele (GPT-4, Claude) radzą sobie lepiej z negacją i sarkazmem niż małe klasyfikatory, "
            "ale wciąż zawodzą na bardzo specyficznych przypadkach kulturowych lub zdaniach wieloznacznych. "
            "Rozmiar modelu nie rozwiązuje problemu rozumienia - opóźnia tylko punkt porażki.",
            "Benchmarki NLP (GLUE, SuperGLUE) mierzą średnie wyniki na dużych zbiorach testowych. "
            "Dobry wynik benchmarkowy nie gwarantuje braku porażki na krawędzi rozkładu - "
            "dlatego testy adversarialne i 'red-teaming' są niezbędne przed wdrożeniem modelu.",
        ],
        "tasks": [
            "Znajdź zdanie, na którym Twój ulubiony chatbot się myli - użyj negacji lub sarkazmu. "
            "Zapisz zdanie, odpowiedź modelu i poprawną odpowiedź. Co model 'zobaczył' zamiast sensu?",
            "Wyjaśnij słowami prostymi, dlaczego sarkazm jest trudny dla modelu językowego. "
            "Użyj analogii: co musiałbyś wiedzieć ty, żeby rozpoznać sarkazm w tekście bez kontekstu?",
            "Zaprojektuj test, który niezawodnie zmyli klasyfikator sentymentu. "
            "Napisz 3 zdania: jedno z negacją, jedno sarkazm, jedno idiom. "
            "Sprawdź na dowolnym darmowym narzędziu NLP online.",
        ],
    },
    "en": {
        "theory": [
            "A language model is a next-word prediction machine trained on statistics. "
            "It does not 'understand' text - it learns patterns from billions of sentences. "
            "This is enough for many tasks, but fails when logic or context is required.",
            "Negation is a systematic weakness of language models. 'It was not a bad film' contains 'bad', "
            "which the model may associate with negative sentiment - ignoring 'not'. "
            "Simple sentiment classifiers misclassify such sentences in 30-40% of cases.",
            "Sarcasm and irony require cultural context and tone that a model cannot 'hear'. "
            "'Oh sure, that is a brilliant idea...' - the model sees 'brilliant', not sarcasm. "
            "Idioms are a similar challenge: the model may take figurative language literally.",
            "Why do humans still beat models on hard cases? "
            "Because we share experiences, linguistic intuition, and causal reasoning ability. "
            "AI excels at typical cases; humans excel at the tail of the distribution.",
        ],
        "notes": [
            "Larger models (GPT-4, Claude) handle negation and sarcasm better than small classifiers, "
            "but still fail on very specific cultural cases or ambiguous sentences. "
            "Model size does not solve understanding - it only delays the failure point.",
            "NLP benchmarks (GLUE, SuperGLUE) measure average performance on large test sets. "
            "A good benchmark score does not guarantee robustness at the edge of the distribution - "
            "that is why adversarial tests and red-teaming are essential before deployment.",
        ],
        "tasks": [
            "Find a sentence that fools your favorite chatbot - use negation or sarcasm. "
            "Record the sentence, the model's answer, and the correct answer. "
            "What did the model 'see' instead of the meaning?",
            "Explain in simple terms why sarcasm is hard for a language model. "
            "Use an analogy: what would you need to know to detect sarcasm in text without context?",
            "Design a test that reliably fools a sentiment classifier. "
            "Write 3 sentences: one with negation, one sarcasm, one idiom. "
            "Test on any free NLP tool online.",
        ],
    },
}

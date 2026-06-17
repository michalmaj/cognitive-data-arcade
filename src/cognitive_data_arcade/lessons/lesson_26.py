"""Lesson 26 -- Human vs Model Challenge (language model failure modes)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Model jezykowy to maszyna do przewidywania nastepnego slowa na podstawie statystyk. "
            "Nie 'rozumie' tekstu -- uczy sie wzorcow z miliardow zdan. "
            "To wystarcza do wielu zadan, ale zawodzi gdy potrzebna jest logika lub kontekst.",
            "Negacja to systematyczna slaba strona modeli. 'Nie byl zly film' zawiera slowo 'zly', "
            "ktore model moze skojarzyc z negatywnym sentymentem -- ignorujac 'nie'. "
            "Proste klasyfikatory sentymentu myla sie na tego typu zdaniach w 30-40% przypadkow.",
            "Sarkazm i ironia wymagaja znajomosci kontekstu kulturowego i tonu, ktorego model nie 'slyszy'. "
            "Zdanie 'No jasne, to genialny pomysl...' -- model widzi 'genialny', nie slyszy ironii. "
            "Idiomy i zwroty frazeologiczne sa podobnym wyzwaniem: 'kopac sie z koniem' to nie fizyka.",
            "Dlaczego ludzie wciaz wygrywaja z modelami na trudnych przypadkach? "
            "Bo mamy wspolne doswiadczenia, intuicje jezykowe i zdolnosc do rozumowania przyczynowego. "
            "AI jest swietna w typowych przypadkach, czlowiek -- w krawedzi rozkladu.",
        ],
        "notes": [
            "Wieksze modele (GPT-4, Claude) radza sobie lepiej z negacja i sarkazmem niz male klasyfikatory, "
            "ale wciaz zawodza na bardzo specyficznych przypadkach kulturowych lub zdaniach wieloznacznych. "
            "Rozmiar modelu nie rozwiazuje problemu rozumienia -- opoznia tylko punkt porazki.",
            "Benchmarki NLP (GLUE, SuperGLUE) mierza srednie wyniki na duzych zbiorach testowych. "
            "Dobry wynik benchmarkowy nie gwarantuje braku porazki na krawedzi rozkladu -- "
            "dlatego testy adversarialne i 'red-teaming' sa niezbedne przed wdrozeniem modelu.",
        ],
        "tasks": [
            "Znajdz zdanie, na ktorym Twoj ulubiony chatbot sie myli -- uzyj negacji lub sarkazmu. "
            "Zapisz zdanie, odpowiedz modelu i poprawna odpowiedz. Co model 'zobaczyl' zamiast sensu?",
            "Wyjasn slowami prostymi, dlaczego sarkazm jest trudny dla modelu jezykowego. "
            "Uzyj analogii: co musialbys wiedziec ty, zeby rozpoznac sarkazm w tekscie bez kontekstu?",
            "Zaprojektuj test, ktory niezawodnie zmyli klasyfikator sentymentu. "
            "Napisz 3 zdania: jedno z negacja, jedno sarkazm, jedno idiom. "
            "Sprawdz na dowolnym darmowym narzedziu NLP online.",
        ],
    },
    "en": {
        "theory": [
            "A language model is a next-word prediction machine trained on statistics. "
            "It does not 'understand' text -- it learns patterns from billions of sentences. "
            "This is enough for many tasks, but fails when logic or context is required.",
            "Negation is a systematic weakness of language models. 'It was not a bad film' contains 'bad', "
            "which the model may associate with negative sentiment -- ignoring 'not'. "
            "Simple sentiment classifiers misclassify such sentences in 30-40% of cases.",
            "Sarcasm and irony require cultural context and tone that a model cannot 'hear'. "
            "'Oh sure, that is a brilliant idea...' -- the model sees 'brilliant', not sarcasm. "
            "Idioms are a similar challenge: the model may take figurative language literally.",
            "Why do humans still beat models on hard cases? "
            "Because we share experiences, linguistic intuition, and causal reasoning ability. "
            "AI excels at typical cases; humans excel at the tail of the distribution.",
        ],
        "notes": [
            "Larger models (GPT-4, Claude) handle negation and sarcasm better than small classifiers, "
            "but still fail on very specific cultural cases or ambiguous sentences. "
            "Model size does not solve understanding -- it only delays the failure point.",
            "NLP benchmarks (GLUE, SuperGLUE) measure average performance on large test sets. "
            "A good benchmark score does not guarantee robustness at the edge of the distribution -- "
            "that is why adversarial tests and red-teaming are essential before deployment.",
        ],
        "tasks": [
            "Find a sentence that fools your favorite chatbot -- use negation or sarcasm. "
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

"""Lesson 25 - Topic Detective (LDA & topic modeling)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "LDA (Latent Dirichlet Allocation) to algorytm odkrywający ukryte tematy w zbiorze dokumentów. "
            "Nie wymaga etykiet - sam wykrywa współwystępujące słowa i grupuje je w tematy. "
            "Wynik: każdy temat to rozkład prawdopodobieństwa nad słowami korpusu.",
            "Temat w LDA to nie kategoria - to 'rodzina słów'. "
            "Top-5 słów tematu to jego 'odcisk palca': Sport: bieg, medal, trening, zawodnik, turniej. "
            "Słowa o wysokim prawdopodobieństwie definiują charakter tematu.",
            "Każdy dokument w LDA to mieszanina tematów, nie pojedyncza etykieta. "
            "Artykuł o sportowcu na diecie może być w 70% Sport i 25% Zdrowie. "
            "Rozkład tematyczny dokumentu to wektor prawdopodobieństw.",
            "Parametr K (liczba tematów) to hiperparametr - nie ma jednej poprawnej odpowiedzi. "
            "Za mało K: tematy są zbyt ogólne. Za dużo K: fragmentacja, tematy się powtarzają. "
            "Oceniamy K przez interpretację jakościową i metryki jak perplexity.",
        ],
        "notes": [
            "LDA kontra NMF (Non-negative Matrix Factorization): oba rozkładają macierz dokumentów na tematy, "
            "ale NMF daje rzadsze, bardziej interpretowalne rozkłady. "
            "LDA jest bardziej probabilistyczne; NMF często szybsze obliczeniowo.",
            "Zastosowania: analiza recenzji (Amazon, Twitter), klasyfikacja dokumentów medycznych, "
            "automatyczne tagowanie artykułów, analiza trendów w social media. "
            "Popularne biblioteki: Gensim, Scikit-learn (LatentDirichletAllocation).",
        ],
        "tasks": [
            "Zagraj w Topic Detective - w którym typie misji najczęściej się myliłeś? "
            "Co to mówi o Twoim rozumieniu tematów jako rozkładów słów?",
            "Weź dowolny artykuł z internetu i szacuj 'na oko' jego rozkład tematyczny. "
            "Ile procent tekstu należy do każdego tematu? Porównaj z intuicją LDA.",
            "Wyjaśnij przyjacielowi czym różni się 'temat LDA' od kategorii w słowniku. "
            "Dlaczego LDA może odkryć temat, którego człowiek by nie wymyślił?",
        ],
    },
    "en": {
        "theory": [
            "LDA (Latent Dirichlet Allocation) is an algorithm that discovers hidden topics in a document collection. "
            "It requires no labels - it detects co-occurring words and groups them into topics. "
            "Result: each topic is a probability distribution over the vocabulary.",
            "A topic in LDA is not a category - it's a 'word family'. "
            "The top-5 words form its 'fingerprint': Sport: run, medal, training, athlete, tournament. "
            "High-probability words define the character of the topic.",
            "Each document in LDA is a mixture of topics, not a single label. "
            "An article about an athlete on a diet might be 70% Sport and 25% Health. "
            "The topic distribution of a document is a probability vector.",
            "Parameter K (number of topics) is a hyperparameter - there's no single correct answer. "
            "Too few K: topics are too broad. Too many K: fragmentation, topics overlap. "
            "We evaluate K through qualitative interpretation and metrics like perplexity.",
        ],
        "notes": [
            "LDA vs NMF (Non-negative Matrix Factorization): both decompose the document matrix into topics, "
            "but NMF yields sparser, more interpretable decompositions. "
            "LDA is more probabilistic; NMF is often faster computationally.",
            "Applications: review analysis (Amazon, Twitter), medical document classification, "
            "automatic article tagging, trend analysis in social media. "
            "Popular libraries: Gensim, Scikit-learn (LatentDirichletAllocation).",
        ],
        "tasks": [
            "Play Topic Detective - which mission type did you get wrong most? "
            "What does that say about your understanding of topics as word distributions?",
            "Take any article online and estimate 'by eye' its topic distribution. "
            "What percentage of the text belongs to each topic? Compare with LDA intuition.",
            "Explain to a friend how an 'LDA topic' differs from a dictionary category. "
            "Why might LDA discover a topic that a human would never think to define?",
        ],
    },
}

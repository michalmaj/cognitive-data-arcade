"""Lesson 25 - Topic Detective (LDA & topic modeling)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "LDA (Latent Dirichlet Allocation) to algorytm odkrywający ukryte tematy w zbiorze dokumentów. Nie wymaga etykiet - sam wykrywa współwystępujące słowa i grupuje je w tematy. Wynik: każdy temat to rozkład prawdopodobieństwa nad słowami korpusu.",
            "Blei, Ng i Jordan (2003) opublikowali LDA w Journal of Machine Learning Research. Artykuł zyskał ponad 40 000 cytowań i jest jednym z najczęściej cytowanych artykułów w historii uczenia maszynowego. Nazwa pochodzi od rozkładu Dirichleta - Petera Lejeune'a Dirichleta (1805-1859), niemieckiego matematyka, którego rozkład leży u podstaw bayesowskich modeli mieszanin.",
            "Temat w LDA to nie kategoria - to 'rodzina słów'. Top-5 słów tematu to jego 'odcisk palca': Sport: bieg, medal, trening, zawodnik, turniej. Słowa o wysokim prawdopodobieństwie definiują charakter tematu.",
            "Każdy dokument w LDA to mieszanina tematów, nie pojedyncza etykieta. Artykuł o sportowcu na diecie może być w 70% Sport i 25% Zdrowie. Rozkład tematyczny dokumentu to wektor prawdopodobieństw.",
            "Parametr K (liczba tematów) to hiperparametr - nie ma jednej poprawnej odpowiedzi. Za mało K: tematy są zbyt ogólne. Za dużo K: fragmentacja, tematy się powtarzają. Ocenia się K przez interpretację jakościową i metryki jak perplexity.",
            "BERTopic (Grootendorst, 2022) - nowoczesne podejście łączące osadzenia zdań (sentence-transformers) z klastrowaniem HDBSCAN. Nie wymaga podawania K z góry - liczba tematów wyłania się z danych. Dostępne jako pakiet Python, dominuje w nowych badaniach analizy tekstów.",
        ],
        "notes": [
            "LDA kontra NMF (Non-negative Matrix Factorization): oba rozkładają macierz dokumentów na tematy, ale NMF daje rzadsze, bardziej interpretowalne rozkłady. LDA jest bardziej probabilistyczne; NMF często szybsze obliczeniowo.",
            "Zastosowania: analiza recenzji (Amazon, Twitter), klasyfikacja dokumentów medycznych, automatyczne tagowanie artykułów, analiza trendów w social media. Popularne biblioteki: Gensim, Scikit-learn (LatentDirichletAllocation).",
        ],
        "tasks": [
            "Zagraj w Topic Detective - w którym typie misji najczęściej pojawiały się błędy? Co to mówi o rozumieniu tematów jako rozkładów słów?",
            "Weź dowolny artykuł z internetu i oszacuj jego rozkład tematyczny. Ile procent tekstu należy do każdego tematu? Porównaj z intuicją LDA.",
            "Wyjaśnij, czym różni się 'temat LDA' od kategorii w słowniku. Dlaczego LDA może odkryć temat, którego człowiek by nie wymyślił?",
        ],
    },
    "en": {
        "theory": [
            "LDA (Latent Dirichlet Allocation) is an algorithm that discovers hidden topics in a document collection. It requires no labels - it detects co-occurring words and groups them into topics. Result: each topic is a probability distribution over the vocabulary.",
            "Blei, Ng and Jordan (2003) published LDA in the Journal of Machine Learning Research. The paper has accumulated over 40,000 citations and is one of the most-cited papers in the history of machine learning. The name comes from the Dirichlet distribution - named after Peter Lejeune Dirichlet (1805-1859), a German mathematician whose distribution underlies Bayesian mixture models.",
            "A topic in LDA is not a category - it is a 'word family'. The top-5 words form its 'fingerprint': Sport: run, medal, training, athlete, tournament. High-probability words define the character of the topic.",
            "Each document in LDA is a mixture of topics, not a single label. An article about an athlete on a diet might be 70% Sport and 25% Health. The topic distribution of a document is a probability vector.",
            "Parameter K (number of topics) is a hyperparameter - there is no single correct answer. Too few K: topics are too broad. Too many K: fragmentation, topics overlap. K is evaluated through qualitative interpretation and metrics like perplexity.",
            "BERTopic (Grootendorst, 2022) - a modern approach combining sentence embeddings (sentence-transformers) with HDBSCAN clustering. It does not require specifying K in advance - the number of topics emerges from the data. Available as a Python package, it now dominates new text analysis research.",
        ],
        "notes": [
            "LDA vs NMF (Non-negative Matrix Factorization): both decompose the document matrix into topics, but NMF yields sparser, more interpretable decompositions. LDA is more probabilistic; NMF is often faster computationally.",
            "Applications: review analysis (Amazon, Twitter), medical document classification, automatic article tagging, trend analysis in social media. Popular libraries: Gensim, Scikit-learn (LatentDirichletAllocation).",
        ],
        "tasks": [
            "Play Topic Detective - which mission type produced the most errors? What does this say about understanding topics as word distributions?",
            "Take any article online and estimate its topic distribution. What percentage of the text belongs to each topic? Compare with LDA intuition.",
            "Explain how an 'LDA topic' differs from a dictionary category. Why might LDA discover a topic that a human would never think to define?",
        ],
    },
}

"""Lesson 25 -- Topic Detective (LDA & topic modeling)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "LDA (Latent Dirichlet Allocation) to algorytm odkrywajacy ukryte tematy w zbiorze dokumentow. "
            "Nie wymaga etykiet -- sam wykrywa wspolwystepujace slowa i grupuje je w tematy. "
            "Wynik: kazdy temat to rozklad prawdopodobienstwa nad slowami korpusu.",
            "Temat w LDA to nie kategoria -- to 'rodzina slow'. "
            "Top-5 slow tematu to jego 'odcisk palca': Sport: bieg, medal, trening, zawodnik, turniej. "
            "Slowa o wysokim prawdopodobienstwie definiuja charakter tematu.",
            "Kazdy dokument w LDA to mieszanina tematow, nie pojedyncza etykieta. "
            "Artykul o sportowcu na diecie moze byc w 70% Sport i 25% Zdrowie. "
            "Rozklad tematyczny dokumentu to wektor prawdopodobienstw.",
            "Parametr K (liczba tematow) to hiperparametr -- nie ma jednej poprawnej odpowiedzi. "
            "Za malo K: tematy sa zbyt ogolne. Za duzo K: fragmentacja, tematy sie powtarzaja. "
            "Oceniamy K przez interpretacje jakosciowa i metryki jak perplexity.",
        ],
        "notes": [
            "LDA kontra NMF (Non-negative Matrix Factorization): oba rozkladaja macierz dokumentow na tematy, "
            "ale NMF daje rzadsze, bardziej interpretowalyne rozklady. "
            "LDA jest bardziej probabilistyczne; NMF czesto szybsze obliczeniowo.",
            "Zastosowania: analiza recenzji (Amazon, Twitter), klasyfikacja dokumentow medycznych, "
            "automatyczne tagowanie artykulow, analiza trendow w social media. "
            "Popularne biblioteki: Gensim, Scikit-learn (LatentDirichletAllocation).",
        ],
        "tasks": [
            "Zagraj w Topic Detective -- w ktorym typie misji najczesciej sie myliles? "
            "Co to mowi o Twoim rozumieniu tematow jako rozkladow slow?",
            "Wez dowolny artykul z internetu i szacuj 'na oko' jego rozklad tematyczny. "
            "Ile procent tekstu nalezy do kazdego tematu? Porownaj z intuicja LDA.",
            "Wyjasnij przyjacielowi czym rozni sie 'temat LDA' od kategorii w slowniku. "
            "Dlaczego LDA moze odkryc temat, ktorego czlowiek by nie wymyslil?",
        ],
    },
    "en": {
        "theory": [
            "LDA (Latent Dirichlet Allocation) is an algorithm that discovers hidden topics in a document collection. "
            "It requires no labels -- it detects co-occurring words and groups them into topics. "
            "Result: each topic is a probability distribution over the vocabulary.",
            "A topic in LDA is not a category -- it's a 'word family'. "
            "The top-5 words form its 'fingerprint': Sport: run, medal, training, athlete, tournament. "
            "High-probability words define the character of the topic.",
            "Each document in LDA is a mixture of topics, not a single label. "
            "An article about an athlete on a diet might be 70% Sport and 25% Health. "
            "The topic distribution of a document is a probability vector.",
            "Parameter K (number of topics) is a hyperparameter -- there's no single correct answer. "
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
            "Play Topic Detective -- which mission type did you get wrong most? "
            "What does that say about your understanding of topics as word distributions?",
            "Take any article online and estimate 'by eye' its topic distribution. "
            "What percentage of the text belongs to each topic? Compare with LDA intuition.",
            "Explain to a friend how an 'LDA topic' differs from a dictionary category. "
            "Why might LDA discover a topic that a human would never think to define?",
        ],
    },
}

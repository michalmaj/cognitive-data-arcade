"""Lesson 22 - Word Weight Factory (Bag of Words and TF-IDF)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Bag of Words (BoW) to najprostszy sposób zamiany tekstu na liczby: liczymy, ile razy każdy token pojawia się w dokumencie. Wynikiem jest wektor o długości równej rozmiarowi słownika. Dwa dokumenty z tym samym słowem dostaną niezerową wartość na tej samej pozycji - to fundament wielu metod klasyfikacji tekstu.",
            "Term Frequency (TF) normalizuje surowe zliczenia przez długość dokumentu: TF(t, d) = count(t, d) / |d|. Dzięki temu krótki i długi dokument są porównywalne: słowo pojawiające się 3 razy w zdaniu 10-słowowym (TF=0.3) waży więcej niż 3 razy w eseju 300-słowowym (TF=0.01).",
            "Inverse Document Frequency (IDF) - Karen Spärck Jones (1972), brytyjska informatyczka, wynalazła miarę IDF i opublikowała ją w Journal of Documentation. Formalnie: IDF(t) = log((N+1) / (df(t)+1)), gdzie N to liczba dokumentów, a df(t) - liczba dokumentów zawierających token t. Słowa pospolite mają niski IDF, słowa specjalistyczne - wysoki. Spärck Jones otrzymała nagrodę ACM Software System Award w 2004 r.",
            "TF-IDF łączy obie miary: TF-IDF(t, d) = TF(t, d) x IDF(t). Token wysoko oceniony przez TF-IDF jest jednocześnie częsty w danym dokumencie i rzadki w korpusie - co czyni go charakterystycznym sygnałem tego dokumentu. To intuicja stojąca za wyszukiwarkami internetowymi i klasyfikacją tekstu.",
            "Word2Vec (Mikolov i in., 2013) - osadzenia słów, które kodują semantykę: wynik operacji 'krol' - 'mezczyzna' + 'kobieta' daje wektor bliski słowu 'krolowa'. TF-IDF liczy słowa niezależnie; Word2Vec koduje ich znaczenie jako miejsce w przestrzeni wektorowej. Oba podejścia łączy współczesne wyszukiwanie semantyczne.",
        ],
        "notes": [
            "BoW i TF-IDF ignorują kolejność słów - zdania 'pies gryzie człowieka' i 'człowiek gryzie psa' mają identyczny wektor. Modele sekwencyjne (RNN, Transformer) przezwyciężają to przez kodowanie pozycji.",
            "Dobór korpusu mocno wpływa na IDF. Jeśli wszystkie dokumenty dotyczą psychologii poznawczej, słowo 'reakcja' będzie miało niski IDF i małą wagę TF-IDF - mimo że jest kluczowe dziedzinowo. Warto zestawiać korpusy z różnych dziedzin.",
        ],
        "tasks": [
            "Uruchom Word Weight Factory i przejdź do kroku BoW. Porównaj wiersz 'Stroop PL' z wierszem 'N-Back EN'. Które tokeny mają wartość 0 w obu dokumentach? Co to znaczy?",
            "Przejdź do kroku IDF. Zidentyfikuj 3 tokeny z najwyższym IDF i 3 z najniższym. Wyjaśnij, dlaczego tokeny o najwyższym IDF są unikalne dla jednego dokumentu.",
            "Włącz usuwanie stop words i obserwuj, jak zmienia się macierz BoW i wykres IDF. Czy wartości TF-IDF najważniejszych tokenów rosną czy maleją? Dlaczego?",
            "Dodaj własny tekst w slocie 'Wlasny' (np. opis innego eksperymentu). Sprawdź, jakie nowe tokeny trafiają do słownika i jak wpływają na IDF istniejących tokenów.",
        ],
    },
    "en": {
        "theory": [
            "Bag of Words (BoW) is the simplest way to convert text to numbers: count how many times each token appears in a document. The result is a vector whose length equals the vocabulary size. Two documents sharing a word get a non-zero value at the same position - this is the foundation of many text classification methods.",
            "Term Frequency (TF) normalises raw counts by document length: TF(t, d) = count(t, d) / |d|. This makes short and long documents comparable: a word appearing 3 times in a 10-word sentence (TF=0.3) carries more weight than 3 times in a 300-word essay (TF=0.01).",
            "Inverse Document Frequency (IDF) - Karen Sparck Jones (1972), a British computer scientist, invented IDF and published it in the Journal of Documentation. Formally: IDF(t) = log((N+1) / (df(t)+1)), where N is the number of documents and df(t) is the count containing token t. Common words have low IDF; domain-specific words have high IDF. Sparck Jones received the ACM Software System Award in 2004.",
            "TF-IDF combines both measures: TF-IDF(t, d) = TF(t, d) x IDF(t). A token with a high TF-IDF score is both frequent in the document and rare in the corpus - making it a distinctive signal for that document. This is the intuition behind search engines and text classification.",
            "Word2Vec (Mikolov et al., 2013) - word embeddings that encode semantics: the operation 'king' - 'man' + 'woman' yields a vector close to 'queen'. TF-IDF counts words independently; Word2Vec encodes their meaning as a position in vector space. Both approaches are combined in modern semantic search.",
        ],
        "notes": [
            "BoW and TF-IDF ignore word order - 'dog bites man' and 'man bites dog' produce identical vectors. Sequential models (RNN, Transformer) overcome this by encoding position.",
            "Corpus choice strongly affects IDF. If all documents concern cognitive psychology, the word 'reaction' will have a low IDF and small TF-IDF weight - even though it is domain-critical. Mixing corpora from different fields is helpful.",
        ],
        "tasks": [
            "Open Word Weight Factory and go to the BoW step. Compare the 'Stroop PL' row with the 'N-Back EN' row. Which tokens have value 0 in both documents? What does that mean?",
            "Go to the IDF step. Identify 3 tokens with the highest IDF and 3 with the lowest. Explain why the highest-IDF tokens are unique to a single document.",
            "Enable stop-word removal and observe how the BoW matrix and IDF chart change. Do TF-IDF scores for the most important tokens increase or decrease? Why?",
            "Add custom text in the 'Wlasny' slot (e.g., another experiment description). Check which new tokens enter the vocabulary and how they affect existing IDF scores.",
        ],
    },
}

REFLECTION = {
    "pl": {
        "title": "Word Weight Factory — Refleksja",
        "cards": [
            {
                "label": "TF-IDF",
                "color": "indigo",
                "text": "TF(t,d) = zliczenia / długość dokumentu. IDF(t) = log(N/df(t)) — Karen Spärck Jones (1972). Wysoki TF-IDF: słowo częste w tym dokumencie i rzadkie w korpusie — charakterystyczny sygnał.",
            },
            {
                "label": "BoW vs embeddingi",
                "color": "orange",
                "text": "BoW ignoruje kolejność: 'pies gryzie człowieka' = 'człowiek gryzie psa'. Word2Vec (Mikolov 2013) koduje znaczenie jako pozycję w przestrzeni wektorowej.",
            },
            {
                "label": "Rzadkość",
                "color": "green",
                "text": "Przy dużym słowniku większość dokumentów ma 99% zer w wektorze TF-IDF. Macierze rzadkie (sparse) rozwiązują problem pamięci, ale nie dodają semantyki — duże słowniki to problem wymiarowości.",
            },
        ],
        "question": "Dokument zawiera słowo 'matrix' 10 razy, a w korpusie 1000 dokumentów pojawia się w 2 z nich. Oblicz IDF. Co TF-IDF mówi o tym słowie — i czego nie mówi?",
    },
    "en": {
        "title": "Word Weight Factory — Reflection",
        "cards": [
            {
                "label": "TF-IDF",
                "color": "indigo",
                "text": "TF(t,d) = count / document length. IDF(t) = log(N/df(t)) — Karen Spärck Jones (1972). High TF-IDF: a word frequent in this document and rare in the corpus — a characteristic signal.",
            },
            {
                "label": "BoW vs embeddings",
                "color": "orange",
                "text": "BoW ignores word order: 'dog bites man' = 'man bites dog'. Word2Vec (Mikolov 2013) encodes meaning as position in a vector space.",
            },
            {
                "label": "Sparsity",
                "color": "green",
                "text": "With a large vocabulary, most documents have 99% zeros in their TF-IDF vector. Sparse matrices solve the memory problem but add no semantics — large vocabularies are a dimensionality problem.",
            },
        ],
        "question": "A document contains the word 'matrix' 10 times; it appears in 2 out of 1,000 corpus documents. Calculate the IDF. What does TF-IDF tell you about this word — and what does it not tell you?",
    },
}

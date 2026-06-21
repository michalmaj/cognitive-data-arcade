# src/cognitive_data_arcade/lessons/lesson_22.py
"""Lesson 22 - Word Weight Factory (Bag of Words and TF-IDF)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Bag of Words (BoW) to najprostszy sposób zamiany tekstu na liczby: liczymy, ile razy "
            "każdy token pojawia się w dokumencie. Wynikiem jest wektor o długości równej rozmiarowi "
            "słownika. Dwa dokumenty z tym samym słowem dostaną niezerową wartość na tej samej "
            "pozycji — to fundament wielu metod klasyfikacji tekstu.",
            "Term Frequency (TF) normalizuje surowe zliczenia przez długość dokumentu: "
            "TF(t, d) = count(t, d) / |d|. Dzięki temu krótki i długi dokument są porównywalne: "
            "słowo pojawiające się 3 razy w zdaniu 10-słowowym (TF=0.3) waży więcej niż "
            "3 razy w eseju 300-słowowym (TF=0.01).",
            "Inverse Document Frequency (IDF) mierzy rzadkość tokenu w całym korpusie: "
            "IDF(t) = log((N+1) / (df(t)+1)), gdzie N to liczba dokumentów, a df(t) to liczba "
            "dokumentów zawierających token t. Słowa pospolite ('i', 'w', 'the') mają niski IDF; "
            "słowa specjalistyczne ('stroop', 'flanker', 'N-back') mają wysoki IDF.",
            "TF-IDF łączy obie miary: TF-IDF(t, d) = TF(t, d) × IDF(t). Token wysoko oceniony "
            "przez TF-IDF jest jednocześnie częsty w danym dokumencie i rzadki w korpusie — "
            "co czyni go charakterystycznym sygnałem tego dokumentu. To intuicja stojąca za "
            "wyszukiwarkami internetowymi i klasyfikacją tekstu w uczeniu maszynowym.",
        ],
        "notes": [
            "BoW i TF-IDF ignorują kolejność słów — zdania 'pies gryzie człowieka' i "
            "'człowiek gryzie psa' mają identyczny wektor. To poważne ograniczenie, które "
            "modele sekwencyjne (RNN, Transformer) przezwyciężają przez kodowanie pozycji. "
            "W zadaniach kognitywnych, gdzie liczy się kontekst zdania, TF-IDF bywa niewystarczające.",
            "Dobór korpusu mocno wpływa na IDF. Jeśli wszystkie dokumenty dotyczą psychologii "
            "poznawczej, słowo 'reakcja' będzie miało niski IDF i małą wagę TF-IDF — mimo że "
            "jest kluczowe dziedzinowo. Warto zestawiać korpusy z różnych dziedzin, by IDF "
            "lepiej odróżniał terminologię specjalistyczną.",
        ],
        "tasks": [
            "Uruchom Word Weight Factory i przejdź do kroku BoW. Porównaj wiersz 'Stroop PL' "
            "z wierszem 'N-Back EN'. Które tokeny mają wartość 0 w obu dokumentach? Co to znaczy?",
            "Przejdź do kroku IDF. Zidentyfikuj 3 tokeny z najwyższym IDF i 3 z najniższym. "
            "Wyjaśnij, dlaczego tokeny o najwyższym IDF są unikalne dla jednego dokumentu.",
            "Włącz usuwanie stop words i obserwuj, jak zmienia się macierz BoW i wykres IDF. "
            "Czy wartości TF-IDF najważniejszych tokenów rosną czy maleją? Dlaczego?",
            "Dodaj własny tekst w slocie 'Wlasny' (np. opis innego eksperymentu). Sprawdź, "
            "jakie nowe tokeny trafiają do słownika i jak wpływają na IDF istniejących tokenów.",
        ],
    },
    "en": {
        "theory": [
            "Bag of Words (BoW) is the simplest way to convert text to numbers: count how many "
            "times each token appears in a document. The result is a vector whose length equals "
            "the vocabulary size. Two documents sharing a word get a non-zero value at the same "
            "position — this is the foundation of many text classification methods.",
            "Term Frequency (TF) normalises raw counts by document length: "
            "TF(t, d) = count(t, d) / |d|. This makes short and long documents comparable: "
            "a word appearing 3 times in a 10-word sentence (TF=0.3) carries more weight than "
            "3 times in a 300-word essay (TF=0.01).",
            "Inverse Document Frequency (IDF) measures how rare a token is across the corpus: "
            "IDF(t) = log((N+1) / (df(t)+1)), where N is the number of documents and df(t) is "
            "the number of documents containing token t. Common words ('and', 'the', 'is') have "
            "low IDF; domain-specific words ('stroop', 'flanker', 'n-back') have high IDF.",
            "TF-IDF combines both measures: TF-IDF(t, d) = TF(t, d) × IDF(t). A token with a "
            "high TF-IDF score is both frequent in the document and rare in the corpus — making "
            "it a distinctive signal for that document. This is the intuition behind search engines "
            "and text classification in machine learning.",
        ],
        "notes": [
            "BoW and TF-IDF ignore word order — 'dog bites man' and 'man bites dog' produce "
            "identical vectors. Sequential models (RNN, Transformer) overcome this by encoding "
            "position. In cognitive tasks where sentence context matters, TF-IDF may be insufficient.",
            "Corpus choice strongly affects IDF. If all documents concern cognitive psychology, "
            "the word 'reaction' will have a low IDF and small TF-IDF weight — even though it is "
            "domain-critical. Mixing corpora from different fields helps IDF better discriminate "
            "between specialist terminology.",
        ],
        "tasks": [
            "Open Word Weight Factory and go to the BoW step. Compare the 'Stroop PL' row with "
            "the 'N-Back EN' row. Which tokens have value 0 in both documents? What does that mean?",
            "Go to the IDF step. Identify 3 tokens with the highest IDF and 3 with the lowest. "
            "Explain why the highest-IDF tokens are unique to a single document.",
            "Enable stop-word removal and observe how the BoW matrix and IDF chart change. "
            "Do TF-IDF scores for the most important tokens increase or decrease? Why?",
            "Add your own text in the 'Wlasny' slot (e.g., another experiment description). "
            "Check which new tokens enter the vocabulary and how they affect existing IDF scores.",
        ],
    },
}

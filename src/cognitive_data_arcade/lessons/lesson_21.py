# src/cognitive_data_arcade/lessons/lesson_21.py
"""Lesson 21 - Text Tokenizer Lab (text preprocessing and tokenization)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Tokenizacja to pierwszy krok przetwarzania języka naturalnego (NLP): dzielimy surowy "
            "tekst na mniejsze jednostki zwane tokenami. Najprościej rozbijamy zdanie na słowa po "
            "białych znakach, ale prawdziwe systemy muszą radzić sobie z interpunkcją, skrótami "
            "i emotikonami. Każdy wybór metody wpływa na jakość dalszej analizy.",
            "Normalizacja obejmuje zamianę liter na małe (lowercasing) oraz usuwanie interpunkcji. "
            "Dzięki temu 'Czas', 'czas' i 'CZAS' traktowane są jako ten sam token. "
            "Bez normalizacji słownik rośnie sztucznie, a modele uczą się pozornych różnic "
            "zamiast semantycznych podobieństw.",
            "Stop words (słowa funkcyjne) to wyrazy tak częste, że niosą mało informacji: "
            "'i', 'w', 'się', 'że', 'na'. Usunięcie ich zmniejsza szum i przyspiesza obliczenia, "
            "ale może uszkodzić zdania wymagające kontekstu gramatycznego. "
            "W analizie kognitywnej stop words bywają ważne -- np. częstość 'nie' sygnalizuje negację.",
            "N-gramy to sekwencje n kolejnych tokenów. Bigram 'czas reakcji' niesie więcej znaczenia "
            "niż dwa osobne słowa 'czas' i 'reakcji'. Trigramy ('długi czas reakcji') dodają jeszcze "
            "więcej kontekstu. W psychologii eksperymentalnej n-gramy pomagają wykryć powtarzające się "
            "frazy w opisach uczestników badania.",
            "Prawo Zipfa głosi, że częstość słowa jest odwrotnie proporcjonalna do jego rangi: "
            "najczęstsze słowo pojawia się mniej więcej dwa razy częściej niż drugie, trzy razy "
            "częściej niż trzecie itd. To zjawisko obserwujemy w każdym języku naturalnym -- "
            "kilka słów dominuje, podczas gdy ogromna większość występuje rzadko.",
        ],
        "notes": [
            "Żadna metoda tokenizacji nie jest idealna. Podział po białych znakach rozrywa skróty "
            "(np. 'dr. hab.') i słowa z łącznikiem ('naukowo-badawczy'). Zaawansowane tokenizatory "
            "używają reguł językowych lub modeli statystycznych, ale nadal popełniają błędy. "
            "Zawsze sprawdź, czy specyfika twojego korpusu nie wymaga dostosowania narzędzia.",
            "Każdy etap preprocessingu to kompromis. Usunięcie stop words przyspiesza obliczenia, "
            "lecz może pogorszyć wyniki klasyfikacji sentimentu (słowo 'nie' bywa stop word!). "
            "Lowercasing upraszcza słownik, ale zamazuje różnicę między 'Polska' (kraj) "
            "a 'polska' (przymiotnik). Decyzje te warto dokumentować i testować eksperymentalnie.",
        ],
        "tasks": [
            "Uruchom Text Tokenizer Lab i załaduj preset 'Tweet PL'. Sprawdź, co się dzieje "
            "z tokenami po włączeniu usuwania interpunkcji. Ile tokenów znika? Dlaczego?",
            "Przełącz się na preset 'Abstract EN' i porównaj wyniki bigramów i trigramów. "
            "Które n-gramy najlepiej opisują temat tekstu? Zapisz trzy najważniejsze.",
            "Włącz usuwanie stop words i sprawdź wykres częstości. Czy rozkład nadal przypomina "
            "prawo Zipfa? Co zmieniło się na szczycie listy najczęstszych tokenów?",
            "Porównaj ten sam tekst z włączonym i wyłączonym lowercasingiem. "
            "O ile różni się liczba unikalnych tokenów? Wyjaśnij, skąd wynika ta różnica.",
        ],
    },
    "en": {
        "theory": [
            "Tokenization is the first step of natural language processing (NLP): we split raw text "
            "into smaller units called tokens. The simplest approach splits on whitespace, but real "
            "systems must handle punctuation, abbreviations, and emoticons. Each choice of method "
            "affects the quality of all downstream analysis.",
            "Normalisation involves converting characters to lowercase and stripping punctuation. "
            "This ensures that 'Time', 'time' and 'TIME' are treated as the same token. "
            "Without normalisation the vocabulary grows artificially, and models learn spurious "
            "distinctions instead of semantic similarities.",
            "Stop words are function words so frequent they carry little information: "
            "'the', 'in', 'is', 'a', 'of'. Removing them reduces noise and speeds up computation, "
            "but can damage sentences that require grammatical context. "
            "In cognitive analysis stop words sometimes matter -- e.g. frequency of 'not' signals negation.",
            "N-grams are sequences of n consecutive tokens. The bigram 'reaction time' carries more "
            "meaning than the two separate words 'reaction' and 'time'. Trigrams ('long reaction time') "
            "add even more context. In experimental psychology n-grams help detect recurring phrases "
            "in participant descriptions.",
            "Zipf's law states that a word's frequency is inversely proportional to its rank: "
            "the most frequent word appears roughly twice as often as the second, three times as often "
            "as the third, and so on. This phenomenon is observed in every natural language -- "
            "a few words dominate while the vast majority appear rarely.",
        ],
        "notes": [
            "No tokenization method is perfect. Splitting on whitespace breaks abbreviations "
            "(e.g. 'Dr. Smith') and hyphenated words ('evidence-based'). Advanced tokenizers use "
            "language rules or statistical models but still make errors. Always check whether "
            "your corpus has specific characteristics that require a customised tool.",
            "Every preprocessing step is a trade-off. Removing stop words speeds up computation "
            "but can hurt sentiment classification (the word 'not' is often a stop word!). "
            "Lowercasing simplifies the vocabulary but blurs the difference between 'Poland' (country) "
            "and 'poland' (lowercase adjective). These decisions are worth documenting and testing empirically.",
        ],
        "tasks": [
            "Launch Text Tokenizer Lab and load the 'Tweet PL' preset. See what happens to tokens "
            "when you enable punctuation removal. How many tokens disappear and why?",
            "Switch to the 'Abstract EN' preset and compare bigram and trigram results. "
            "Which n-grams best describe the topic of the text? Write down the three most important ones.",
            "Enable stop word removal and inspect the frequency chart. Does the distribution still "
            "resemble Zipf's law? What changed at the top of the most-frequent tokens list?",
            "Compare the same text with and without lowercasing enabled. "
            "By how much does the unique token count differ? Explain where that difference comes from.",
        ],
    },
}

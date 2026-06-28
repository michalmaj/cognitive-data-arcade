"""Lesson 21 - Text Tokenizer Lab (text preprocessing and tokenization)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Tokenizacja to pierwszy krok przetwarzania języka naturalnego (NLP): dzielimy surowy tekst na mniejsze jednostki zwane tokenami. Najprościej rozbijamy zdanie na słowa po białych znakach, ale prawdziwe systemy muszą radzić sobie z interpunkcją, skrótami i emotikonami. Każdy wybór metody wpływa na jakość dalszej analizy.",
            "Normalizacja obejmuje zamianę liter na małe (lowercasing) oraz usuwanie interpunkcji. Dzięki temu 'Czas', 'czas' i 'CZAS' traktowane są jako ten sam token. Bez normalizacji słownik rośnie sztucznie, a modele uczą się pozornych różnic zamiast semantycznych podobieństw.",
            "Stop words (słowa funkcyjne) to wyrazy tak częste, że niosą mało informacji: 'i', 'w', 'się', 'że', 'na'. Usunięcie ich zmniejsza szum i przyspiesza obliczenia, ale może uszkodzić zdania wymagające kontekstu gramatycznego. W analizie kognitywnej stop words bywają ważne - np. częstość 'nie' sygnalizuje negację.",
            "N-gramy to sekwencje n kolejnych tokenów. Bigram 'czas reakcji' niesie więcej znaczenia niż dwa osobne słowa 'czas' i 'reakcji'. Trigramy ('długi czas reakcji') dodają jeszcze więcej kontekstu. W psychologii eksperymentalnej n-gramy pomagają wykryć powtarzające się frazy w opisach uczestników badania.",
            "Prawo Zipfa - George Kingsley Zipf odkrył je w 1935 r. analizując frekwencję słów w angielszczyźnie. Częstość słowa jest odwrotnie proporcjonalna do jego rangi: najczęstsze słowo pojawia się ok. dwa razy częściej niż drugie, trzy razy częściej niż trzecie itd. Zjawisko obserwuje się w każdym języku naturalnym.",
            "BPE (Byte-Pair Encoding) - algorytm tokenizacji zaproponowany przez Sennricha i in. (2016) dla tłumaczenia maszynowego. Iteracyjnie scala najczęstsze pary tokenów w nowe tokeny, tworząc słownik podwyrazowy. GPT-2 (OpenAI, 2019) używa słownika 50 257 tokenów BPE; nieznane słowa rozkłada na fragmenty, nie traci żadnego tekstu.",
            "Korpus Browna (1964) - pierwszy milionowy korpus języka angielskiego; zebrany na Brown University przez Francisa i Kucerę. Zawierał 500 próbek z 15 gatunków tekstu po ok. 2000 słów każda. Był przez dekadę standardem w językoznawstwie korpusowym i umożliwił pierwsze ilościowe badania frekwencji słów.",
        ],
        "notes": [
            "Żadna metoda tokenizacji nie jest idealna. Podział po białych znakach rozrywa skróty i słowa z łącznikiem. Zaawansowane tokenizatory używają reguł językowych lub modeli statystycznych, ale nadal popełniają błędy. Warto sprawdzić, czy specyfika danego korpusu nie wymaga dostosowania narzędzia.",
            "Każdy etap preprocessingu to kompromis. Usunięcie stop words przyspiesza obliczenia, lecz może pogorszyć wyniki klasyfikacji sentimentu (słowo 'nie' bywa stop word). Lowercasing upraszcza słownik, ale zamazuje różnicę między 'Polska' (kraj) a 'polska' (przymiotnik). Decyzje te warto dokumentować i testować eksperymentalnie.",
        ],
        "tasks": [
            "Uruchom Text Tokenizer Lab i załaduj preset 'Tweet PL'. Sprawdź, co się dzieje z tokenami po włączeniu usuwania interpunkcji. Ile tokenów znika? Dlaczego?",
            "Przełącz się na preset 'Abstract EN' i porównaj wyniki bigramów i trigramów. Które n-gramy najlepiej opisują temat tekstu? Zapisz trzy najważniejsze.",
            "Włącz usuwanie stop words i sprawdź wykres częstości. Czy rozkład nadal przypomina prawo Zipfa? Co zmieniło się na szczycie listy najczęstszych tokenów?",
            "Porównaj ten sam tekst z włączonym i wyłączonym lowercasingiem. O ile różni się liczba unikalnych tokenów? Wyjaśnij, skąd wynika ta różnica.",
        ],
    },
    "en": {
        "theory": [
            "Tokenization is the first step of natural language processing (NLP): raw text is split into smaller units called tokens. The simplest approach splits on whitespace, but real systems must handle punctuation, abbreviations, and emoticons. Each choice of method affects the quality of all downstream analysis.",
            "Normalisation involves converting characters to lowercase and stripping punctuation. This ensures that 'Time', 'time' and 'TIME' are treated as the same token. Without normalisation the vocabulary grows artificially, and models learn spurious distinctions instead of semantic similarities.",
            "Stop words are function words so frequent they carry little information: 'the', 'in', 'is', 'a', 'of'. Removing them reduces noise and speeds up computation, but can damage sentences that require grammatical context. In cognitive analysis stop words sometimes matter - e.g. frequency of 'not' signals negation.",
            "N-grams are sequences of n consecutive tokens. The bigram 'reaction time' carries more meaning than the two separate words 'reaction' and 'time'. Trigrams ('long reaction time') add even more context. In experimental psychology n-grams help detect recurring phrases in participant descriptions.",
            "Zipf's law - George Kingsley Zipf discovered it in 1935 while analysing word frequencies in English. A word's frequency is inversely proportional to its rank: the most frequent word appears approximately twice as often as the second, three times as often as the third, and so on. The phenomenon is observed in every natural language.",
            "BPE (Byte-Pair Encoding) - a tokenisation algorithm proposed by Sennrich et al. (2016) for machine translation. It iteratively merges the most frequent token pairs into new tokens, creating a subword vocabulary. GPT-2 (OpenAI, 2019) uses a vocabulary of 50,257 BPE tokens; unknown words are decomposed into fragments, never discarded.",
            "The Brown Corpus (1964) - the first million-word corpus of English; assembled at Brown University by Francis and Kucera. It contained 500 samples from 15 text genres of approximately 2,000 words each. For a decade it was the standard in corpus linguistics and enabled the first quantitative studies of word frequency.",
        ],
        "notes": [
            "No tokenization method is perfect. Splitting on whitespace breaks abbreviations and hyphenated words. Advanced tokenizers use language rules or statistical models but still make errors. It is worth checking whether the specific corpus requires a customised tool.",
            "Every preprocessing step is a trade-off. Removing stop words speeds up computation but can hurt sentiment classification (the word 'not' is often a stop word). Lowercasing simplifies the vocabulary but blurs the difference between 'Poland' (country) and 'poland' (lowercase adjective). These decisions are worth documenting and testing empirically.",
        ],
        "tasks": [
            "Launch Text Tokenizer Lab and load the 'Tweet PL' preset. See what happens to tokens when you enable punctuation removal. How many tokens disappear and why?",
            "Switch to the 'Abstract EN' preset and compare bigram and trigram results. Which n-grams best describe the topic of the text? Write down the three most important ones.",
            "Enable stop word removal and inspect the frequency chart. Does the distribution still resemble Zipf's law? What changed at the top of the most-frequent tokens list?",
            "Compare the same text with and without lowercasing enabled. By how much does the unique token count differ? Explain where that difference comes from.",
        ],
    },
}

REFLECTION = {
    "pl": {
        "title": "Text Tokenizer Lab — Refleksja",
        "cards": [
            {
                "label": "Tokenizacja",
                "color": "indigo",
                "text": "Tokenizacja dzieli tekst na mniejsze jednostki. BPE (Sennrich 2016) iteracyjnie scala najczęstsze pary znaków — tak działa GPT: słownik 50 257 tokenów, żaden tekst nie jest nieznany.",
            },
            {
                "label": "Normalizacja",
                "color": "orange",
                "text": "Lowercase i usuwanie interpunkcji redukują słownik. Prawo Zipfa (1935): najczęstsze słowo pojawia się ~2× częściej od drugiego. 20% słownika pokrywa 80% tekstu.",
            },
            {
                "label": "Stop words",
                "color": "green",
                "text": "Słowa funkcyjne ('i', 'w', 'się') niosą mało informacji semantycznej. Usunięcie zmniejsza szum, ale usuwa kontekst gramatyczny — słowo 'nie' może być kluczowe dla negacji.",
            },
        ],
        "question": "Tokenizator dzieli 'niezapomniany' na 3 tokeny. Dlaczego nieznane słowa są kosztowniejsze obliczeniowo i jak BPE radzi sobie z neologizmami?",
    },
    "en": {
        "title": "Text Tokenizer Lab — Reflection",
        "cards": [
            {
                "label": "Tokenisation",
                "color": "indigo",
                "text": "Tokenisation splits text into smaller units. BPE (Sennrich 2016) iteratively merges the most frequent character pairs — GPT uses this: a vocabulary of 50,257 tokens, no text is unknown.",
            },
            {
                "label": "Normalisation",
                "color": "orange",
                "text": "Lowercasing and removing punctuation reduce vocabulary size. Zipf's law (1935): the most frequent word appears ~2x more often than the second. 20% of vocabulary covers 80% of text.",
            },
            {
                "label": "Stop words",
                "color": "green",
                "text": "Function words ('and', 'in', 'the') carry little semantic information. Removing them reduces noise but removes grammatical context — the word 'not' can be crucial for negation.",
            },
        ],
        "question": "A tokeniser splits 'unforgettable' into 3 tokens. Why are unknown words computationally more expensive, and how does BPE handle neologisms?",
    },
}

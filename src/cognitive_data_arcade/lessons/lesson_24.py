"""Lesson 24 -- Semantic Space Explorer (embeddings & semantic similarity)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Embedding to reprezentacja slowa jako wektora liczb. "
            "Slowa uczone na duzych tekstach - 'kot' i 'pies' pojawiaja sie w podobnych zdaniach, "
            "wiec ich wektory sa blisko siebie w przestrzeni wielowymiarowej.",
            "Podobienstwo kosinusowe (cosine similarity) mierzy kat miedzy wektorami. "
            "Wynik bliski 1.0 = bardzo podobne, bliski 0.0 = niepowiazane, ujemny = przeciwstawne. "
            "Mierzymy kat, nie odleglosc - skala wektora nie ma znaczenia.",
            "Klastry semantyczne wylaniaja sie automatycznie: emocje blisko emocji, "
            "zwierzeta blisko zwierzat. Nikt nie programowal tych kategorii - "
            "model nauczyl sie ich z kontekstu.",
            "Analogie wektorowe: krol - mezczyzna + kobieta = krolowa. "
            "To odkrycie z 2013 roku (Word2Vec, Mikolov) pokazalo, ze embeddingi "
            "koduja relacje semantyczne jako arytmetyke wektorow.",
        ],
        "notes": [
            "Embeddingi maja wady: bias spoleczny (lekarz = mezczyzna), "
            "polisemia (bank = rzeka / finansowy), brak rozumienia negacji ('nie dobry' != 'zly'). "
            "LLM z kontekstem (BERT, GPT) czesciowo rozwiazuja te problemy.",
            "Popularne modele: Word2Vec (2013), GloVe (2014), FastText (2016), "
            "oraz kontekstowe: ELMo, BERT, GPT. "
            "Kazde slowo dostaje inny wektor w zaleznosci od zdania w modelach kontekstowych.",
        ],
        "tasks": [
            "Zagraj w Semantic Space Explorer - w ktorej misji bladziles najczesciej? "
            "Co to mowi o Twoim rozumieniu klastrow semantycznych?",
            "Wymien 3 polskie slowa, ktore Twoim zdaniem sa na granicy dwoch kategorii semantycznych. "
            "Dlaczego sa trudne do jednoznacznego zaklasyfikowania?",
            "Porownaj podobienstwo kosinusowe a odleglosc euklidesowa dla wektorow slow. "
            "Kiedy kazda miara jest lepsza?",
        ],
    },
    "en": {
        "theory": [
            "An embedding represents a word as a vector of numbers. "
            "Trained on large corpora - 'cat' and 'dog' appear in similar sentences, "
            "so their vectors land close together in high-dimensional space.",
            "Cosine similarity measures the angle between vectors. "
            "Score near 1.0 = very similar, near 0.0 = unrelated, negative = opposite. "
            "We measure angle, not distance - vector magnitude doesn't matter.",
            "Semantic clusters emerge automatically: emotions near emotions, "
            "animals near animals. Nobody programmed these categories - "
            "the model learned them from context.",
            "Vector analogies: king - man + woman = queen. "
            "This 2013 discovery (Word2Vec, Mikolov) showed that embeddings "
            "encode semantic relations as vector arithmetic.",
        ],
        "notes": [
            "Embeddings have flaws: social bias (doctor = man), "
            "polysemy (bank = river / financial), no negation understanding. "
            "Contextual LLMs (BERT, GPT) partially solve these issues.",
            "Popular models: Word2Vec (2013), GloVe (2014), FastText (2016), "
            "and contextual: ELMo, BERT, GPT. "
            "Each word gets a different vector depending on the sentence in contextual models.",
        ],
        "tasks": [
            "Play Semantic Space Explorer - which mission type did you get wrong most? "
            "What does that say about your intuition for semantic clusters?",
            "Name 3 Polish words you think sit on the boundary between two semantic categories. "
            "Why are they hard to classify cleanly?",
            "Compare cosine similarity vs Euclidean distance for word vectors. "
            "When is each measure better?",
        ],
    },
}

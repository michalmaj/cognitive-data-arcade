"""Lesson 24 - Semantic Space Explorer (embeddings & semantic similarity)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Embedding to reprezentacja słowa jako wektora liczb. "
            "Słowa uczone na dużych tekstach - 'kot' i 'pies' pojawiają się w podobnych zdaniach, "
            "więc ich wektory są blisko siebie w przestrzeni wielowymiarowej.",
            "Podobieństwo kosinusowe (cosine similarity) mierzy kąt między wektorami. "
            "Wynik bliski 1.0 = bardzo podobne, bliski 0.0 = niepowiązane, ujemny = przeciwstawne. "
            "Mierzymy kąt, nie odległość - skala wektora nie ma znaczenia.",
            "Klastry semantyczne wyłaniają się automatycznie: emocje blisko emocji, "
            "zwierzęta blisko zwierząt. Nikt nie programował tych kategorii - "
            "model nauczył się ich z kontekstu.",
            "Analogie wektorowe: król - mężczyzna + kobieta = królowa. "
            "To odkrycie z 2013 roku (Word2Vec, Mikolov) pokazało, że embeddingi "
            "kodują relacje semantyczne jako arytmetykę wektorów.",
        ],
        "notes": [
            "Embeddingi mają wady: bias społeczny (lekarz = mężczyzna), "
            "polisemia (bank = rzeka / finansowy), brak rozumienia negacji ('nie dobry' != 'zły'). "
            "LLM z kontekstem (BERT, GPT) częściowo rozwiązują te problemy.",
            "Popularne modele: Word2Vec (2013), GloVe (2014), FastText (2016), "
            "oraz kontekstowe: ELMo, BERT, GPT. "
            "Każde słowo dostaje inny wektor w zależności od zdania w modelach kontekstowych.",
        ],
        "tasks": [
            "Zagraj w Semantic Space Explorer - w której misji błądziłeś najczęściej? "
            "Co to mówi o Twoim rozumieniu klastrów semantycznych?",
            "Wymień 3 polskie słowa, które Twoim zdaniem są na granicy dwóch kategorii semantycznych. "
            "Dlaczego są trudne do jednoznacznego zaklasyfikowania?",
            "Porównaj podobieństwo kosinusowe a odległość euklidesową dla wektorów słów. "
            "Kiedy każda miara jest lepsza?",
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

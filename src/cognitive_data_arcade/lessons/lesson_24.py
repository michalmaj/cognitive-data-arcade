"""Lesson 24 - Semantic Space Explorer (embeddings & semantic similarity)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Embedding to reprezentacja słowa jako wektora liczb. Słowa uczone na dużych tekstach - 'kot' i 'pies' pojawiają sie w podobnych zdaniach, więc ich wektory są blisko siebie w przestrzeni wielowymiarowej.",
            "Hipoteza dystrybucyjna (Harris, 1954) - 'słowa, które pojawiają sie w tych samych kontekstach, mają tendencję do podobnych znaczeń'. Word2Vec (Mikolov, 2013) sformalizował tę intuicję algorytmicznie - o 59 lat po oryginalnej hipotezie. Hipoteza Harrisa leży u podstaw każdego współczesnego modelu językowego.",
            "Podobieństwo kosinusowe (cosine similarity) mierzy kąt między wektorami. Wynik bliski 1.0 = bardzo podobne, bliski 0.0 = niepowiązane, ujemny = przeciwstawne. Mierzy sie kąt, nie odległość - skala wektora nie ma znaczenia.",
            "Klastry semantyczne wyłaniają sie automatycznie: emocje blisko emocji, zwierzęta blisko zwierząt. Nikt nie programował tych kategorii - model nauczył sie ich z kontekstu. To emergentna właściwość wynikająca wyłącznie z rozkładu słów w tekstach.",
            "Analogie wektorowe: krol - mezczyzna + kobieta = krolowa. To odkrycie z 2013 r. (Word2Vec, Mikolov) pokazało, że embeddingi kodują relacje semantyczne jako arytmetykę wektorów.",
            "Bias w embeddingach - Bolukbasi i in. (2016) wykazali, że Word2Vec koduje stereotypy płciowe: 'pielęgniarka' jest do 'kobiety' jak 'lekarz' do 'mężczyzny'. Embeddingi uczą sie nie tylko struktury językowej, ale też uprzedzeń obecnych w treningowym korpusie tekstów.",
        ],
        "notes": [
            "Embeddingi mają wady: bias społeczny (lekarz = mężczyzna), polisemia (bank = rzeka / finansowy), brak rozumienia negacji ('nie dobry' nie równa sie 'zły'). Modele kontekstowe (BERT, GPT) częściowo rozwiązują te problemy.",
            "Popularne modele: Word2Vec (2013), GloVe (Pennington i in., 2014 - Global Vectors z macierzy współwystępowań), FastText (2016 - obsługa podwyrazów), oraz kontekstowe: ELMo, BERT, GPT. W modelach kontekstowych każde słowo dostaje inny wektor zależnie od zdania.",
        ],
        "tasks": [
            "Zagraj w Semantic Space Explorer - w której misji pojawiało sie najwięcej błędów? Co to mówi o intuicji dotyczącej klastrów semantycznych?",
            "Wymień 3 polskie słowa, które wydają sie leżeć na granicy dwóch kategorii semantycznych. Dlaczego są trudne do jednoznacznego zaklasyfikowania?",
            "Porównaj podobieństwo kosinusowe i odległość euklidesową dla wektorów słów. Kiedy każda miara jest lepsza?",
        ],
    },
    "en": {
        "theory": [
            "An embedding represents a word as a vector of numbers. Trained on large corpora - 'cat' and 'dog' appear in similar sentences, so their vectors land close together in high-dimensional space.",
            "The distributional hypothesis (Harris, 1954) - 'words that occur in the same contexts tend to have similar meanings'. Word2Vec (Mikolov, 2013) formalised this intuition algorithmically - 59 years after the original hypothesis. Harris's hypothesis underlies every modern language model.",
            "Cosine similarity measures the angle between vectors. Score near 1.0 = very similar, near 0.0 = unrelated, negative = opposite. The angle is measured, not the distance - vector magnitude does not matter.",
            "Semantic clusters emerge automatically: emotions near emotions, animals near animals. Nobody programmed these categories - the model learned them from context. This is an emergent property arising solely from the distribution of words in text.",
            "Vector analogies: king - man + woman = queen. This 2013 discovery (Word2Vec, Mikolov) showed that embeddings encode semantic relations as vector arithmetic.",
            "Bias in embeddings - Bolukbasi et al. (2016) demonstrated that Word2Vec encodes gender stereotypes: 'nurse' is to 'woman' as 'doctor' is to 'man'. Embeddings learn not only linguistic structure but also the prejudices present in the training corpus.",
        ],
        "notes": [
            "Embeddings have flaws: social bias (doctor = man), polysemy (bank = river / financial), no negation understanding ('not good' does not equal 'bad'). Contextual models (BERT, GPT) partially solve these issues.",
            "Popular models: Word2Vec (2013), GloVe (Pennington et al., 2014 - Global Vectors from co-occurrence matrices), FastText (2016 - subword handling), and contextual: ELMo, BERT, GPT. In contextual models each word gets a different vector depending on the sentence.",
        ],
        "tasks": [
            "Play Semantic Space Explorer - in which mission type did the most errors occur? What does this say about intuitions about semantic clusters?",
            "Name 3 Polish words that seem to sit on the boundary between two semantic categories. Why are they hard to classify cleanly?",
            "Compare cosine similarity vs Euclidean distance for word vectors. When is each measure better?",
        ],
    },
}

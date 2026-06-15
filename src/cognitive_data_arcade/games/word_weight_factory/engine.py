from __future__ import annotations

import math
import string
from dataclasses import dataclass

from cognitive_data_arcade.games.text_tokenizer.stop_words import (
    STOP_WORDS_EN,
    STOP_WORDS_PL,
)


@dataclass
class WeightMatrix:
    vocab: list[str]
    doc_titles: list[str]
    bow: list[list[int]]
    tf: list[list[float]]
    idf: list[float]
    tfidf: list[list[float]]


class WeightEngine:
    def process(
        self,
        docs: list[str],
        titles: list[str],
        lowercase: bool,
        rm_punct: bool,
        rm_stops: bool,
        lang: str,
    ) -> WeightMatrix:
        if not docs:
            return WeightMatrix([], [], [], [], [], [])

        stops = STOP_WORDS_PL if lang == "pl" else STOP_WORDS_EN

        tokenized: list[list[str]] = []
        for text in docs:
            tokens = text.split()
            if lowercase:
                tokens = [t.lower() for t in tokens]
            if rm_punct:
                tokens = [t.strip(string.punctuation) for t in tokens]
                tokens = [t for t in tokens if t]
            if rm_stops:
                tokens = [t for t in tokens if t.lower() not in stops]
            tokenized.append(tokens)

        vocab = sorted({t for toks in tokenized for t in toks})
        if not vocab:
            return WeightMatrix([], list(titles), [], [], [], [])

        vocab_idx = {w: i for i, w in enumerate(vocab)}
        N = len(docs)
        V = len(vocab)

        bow: list[list[int]] = []
        for toks in tokenized:
            row = [0] * V
            for t in toks:
                if t in vocab_idx:
                    row[vocab_idx[t]] += 1
            bow.append(row)

        tf: list[list[float]] = []
        for i, toks in enumerate(tokenized):
            doc_len = max(1, len(toks))
            tf.append([bow[i][j] / doc_len for j in range(V)])

        idf: list[float] = []
        for j in range(V):
            df = sum(1 for i in range(N) if bow[i][j] > 0)
            idf.append(math.log((N + 1) / (df + 1)))

        tfidf: list[list[float]] = [
            [tf[i][j] * idf[j] for j in range(V)]
            for i in range(N)
        ]

        return WeightMatrix(
            vocab=vocab,
            doc_titles=list(titles),
            bow=bow,
            tf=tf,
            idf=idf,
            tfidf=tfidf,
        )

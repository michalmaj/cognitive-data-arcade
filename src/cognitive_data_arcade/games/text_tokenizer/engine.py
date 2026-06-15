from __future__ import annotations

import string
from dataclasses import dataclass

from cognitive_data_arcade.games.text_tokenizer.stop_words import (
    STOP_WORDS_EN, STOP_WORDS_PL,
)


@dataclass
class TokenizerState:
    raw_tokens: list[str]
    tokens: list[str]
    unique_count: int
    ngrams: list[tuple[str, ...]]
    freq: dict[str, int]


class TokenizerEngine:
    def process(
        self,
        text: str,
        lowercase: bool,
        rm_punct: bool,
        rm_stops: bool,
        lang: str,
        ngram_n: int,
    ) -> TokenizerState:
        raw_tokens = text.split()
        tokens = list(raw_tokens)

        if lowercase:
            tokens = [t.lower() for t in tokens]

        if rm_punct:
            tokens = [t.strip(string.punctuation) for t in tokens]
            tokens = [t for t in tokens if t]

        if rm_stops:
            stops = STOP_WORDS_PL if lang == "pl" else STOP_WORDS_EN
            tokens = [t for t in tokens if t.lower() not in stops]

        ngrams: list[tuple[str, ...]] = []
        if ngram_n >= 1 and len(tokens) >= ngram_n:
            ngrams = list(zip(*[tokens[i:] for i in range(ngram_n)]))

        freq: dict[str, int] = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
        freq = dict(sorted(freq.items(), key=lambda x: -x[1]))

        return TokenizerState(
            raw_tokens=raw_tokens,
            tokens=tokens,
            unique_count=len(set(tokens)),
            ngrams=ngrams,
            freq=freq,
        )

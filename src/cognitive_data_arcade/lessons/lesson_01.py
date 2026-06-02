"""Lesson 01 — Big Data in Cognitive Science (BigDataMap)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Co to Big Data — trzy V: volume (terabajty danych), velocity (dane w czasie rzeczywistym), variety (wiele formatów). Dane kognitywne spełniają wszystkie trzy kryteria.",
            "Dlaczego ilość danych zmienia metodę — przy małych N liczymy statystyki. Przy dużych N możemy modelować strukturę, szukać wzorców i budować sieci pojęć.",
            "Graf pojęć — węzły to koncepty, krawędzie to relacje. Sieć pozwala zobaczyć jak wiedza jest zorganizowana — nie lista faktów, lecz mapa zależności między ideami.",
            "Poziomy L1 i L2 — L1 to główne kategorie dziedziny, L2 to szczegółowe pojęcia. Hierarchia pozwala nawigować od ogółu do szczegółu i z powrotem.",
            "Skala a interpretacja — 10 pojęć to słownik. 10 000 pojęć to ontologia. Metody analizy muszą skalować się razem z ilością danych, inaczej tracimy sens w szumie.",
        ],
        "notes": [
            "Jak czytać sieć pojęć — zacznij od węzłów L1 (główne kategorie). Krawędzie między nimi pokazują najsilniejsze relacje w całym systemie wiedzy.",
            "Co oznacza gęstość sieci — węzeł z wieloma krawędziami to pojęcie centralne dla dziedziny. Węzeł izolowany to pojęcie peryferyjne lub zbyt wąsko zdefiniowane.",
            "Połączenia między pojęciami niosą znaczenie — dwa podobne słowa mogą mieć różne miejsce w sieci, co ujawnia czy są synonimami czy zupełnie odmiennymi konceptami.",
        ],
        "tasks": [
            "Znajdź węzeł L1 z największą liczbą połączeń do innych węzłów. Co to mówi o centralności tego pojęcia w dziedzinie kognitywistyki?",
            "Czy jest jakieś pojęcie L2, które pasowałoby do więcej niż jednego L1? Jeśli tak — co to mówi o wieloznaczności lub interdyscyplinarności tego terminu?",
            "Gdybyś dodał nowy węzeł do sieci — gdzie by pasował? Z którymi istniejącymi pojęciami miałby krawędzie i dlaczego?",
        ],
    },
    "en": {
        "theory": [
            "What is Big Data — three Vs: volume (terabytes of data), velocity (real-time streams), variety (many formats). Cognitive data meets all three criteria.",
            "Why data scale changes the method — with small N we compute statistics. With large N we can model structure, find patterns, and build concept networks.",
            "A concept graph — nodes are concepts, edges are relations. A network reveals how knowledge is organised — not a list of facts, but a map of dependencies between ideas.",
            "L1 and L2 levels — L1 are the main domain categories, L2 are specific concepts. The hierarchy lets you navigate from the general to the specific and back.",
            "Scale and interpretation — 10 concepts is a glossary. 10,000 concepts is an ontology. Analysis methods must scale with data volume, otherwise meaning is lost in noise.",
        ],
        "notes": [
            "How to read a concept network — start with L1 nodes (main categories). Edges between them show the strongest relations in the entire knowledge system.",
            "What network density means — a node with many edges is central to the domain. An isolated node is peripheral or too narrowly defined.",
            "Connections between concepts carry meaning — two similar-sounding words may occupy different places in the network, revealing whether they are synonyms or distinct concepts.",
        ],
        "tasks": [
            "Find the L1 node with the most connections to other nodes. What does this say about the centrality of that concept in the cognitive science domain?",
            "Is there an L2 concept that could belong to more than one L1? If so — what does that say about the ambiguity or interdisciplinary nature of that term?",
            "If you were to add a new node to the network — where would it fit? Which existing concepts would it connect to, and why?",
        ],
    },
}

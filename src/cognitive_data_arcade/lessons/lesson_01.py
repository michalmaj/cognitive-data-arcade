"""Lesson 01 - Big Data in Cognitive Science (BigDataMap)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Co to Big Data - trzy V: volume (terabajty danych), velocity (dane w czasie rzeczywistym), variety (wiele formatów). Dane kognitywne spełniają wszystkie trzy kryteria.",
            "Dlaczego ilość danych zmienia metodę - przy małych N liczymy statystyki. Przy dużych N możemy modelować strukturę, szukać wzorców i budować sieci pojęć.",
            "Graf pojęć - węzły to koncepty, krawędzie to relacje. Sieć pozwala zobaczyć jak wiedza jest zorganizowana - nie lista faktów, lecz mapa zależności między ideami.",
            "Poziomy L1 i L2 - L1 to główne kategorie dziedziny, L2 to szczegółowe pojęcia. Hierarchia pozwala nawigować od ogółu do szczegółu i z powrotem.",
            "Skala a interpretacja - 10 pojęć to słownik. 10 000 pojęć to ontologia. Metody analizy muszą skalować się razem z ilością danych, inaczej tracimy sens w szumie.",
            "Pierwszy komputerowy tezaurus semantyczny - WordNet - zawiera około 155 000 słów angielskich pogrupowanych w 117 000 tzw. synsetów. Zbudowanie go zajęło zespołowi Princeton University ponad 10 lat ręcznej pracy (1985-2006). To pokazuje, że budowanie wiedzy strukturalnej jest kosztowne nawet dla języka naturalnego.",
            "Grafy wiedzy w praktyce - Google Knowledge Graph zawiera ponad 500 miliardów faktów o 5 miliardach encji. Kiedy wyszukiwarka pokazuje panel boczny z informacją o osobie lub miejscu, korzysta właśnie z takiej struktury. Kognitywistyka buduje podobne struktury dla procesów umysłowych.",
            "Efekt emergencji w sieciach - w grafie pojęć często pojawiają się skupiska (klastry), które nie były planowane przez projektantów. Te klastry ujawniają ukrytą strukturę dziedziny. Odkrycie niespodziewanego skupiska bywa punktem wyjścia dla nowej teorii.",
        ],
        "notes": [
            "Jak czytać sieć pojęć - zacznij od węzłów L1 (główne kategorie). Krawędzie między nimi pokazują najsilniejsze relacje w całym systemie wiedzy.",
            "Co oznacza gęstość sieci - węzeł z wieloma krawędziami to pojęcie centralne dla dziedziny. Węzeł izolowany to pojęcie peryferyjne lub zbyt wąsko zdefiniowane.",
            "Połączenia między pojęciami niosą znaczenie - dwa podobne słowa mogą mieć różne miejsce w sieci, co ujawnia czy są synonimami czy zupełnie odmiennymi konceptami.",
            "Warto sprawdzić, które pojęcia łączą dwa odległe skupiska - te pojęcia to tzw. mosty semantyczne i często odpowiadają terminom interdyscyplinarnym.",
        ],
        "tasks": [
            "Znajdź węzeł L1 z największą liczbą połączeń do innych węzłów. Co to mówi o centralności tego pojęcia w dziedzinie kognitywistyki?",
            "Czy jest jakieś pojęcie L2, które pasowałoby do więcej niż jednego L1? Jeśli tak - co to mówi o wieloznaczności lub interdyscyplinarności tego terminu?",
            "Gdybyś dodał nowy węzeł do sieci - gdzie by pasował? Z którymi istniejącymi pojęciami miałby krawędzie i dlaczego?",
        ],
    },
    "en": {
        "theory": [
            "What is Big Data - three Vs: volume (terabytes of data), velocity (real-time streams), variety (many formats). Cognitive data meets all three criteria.",
            "Why data scale changes the method - with small N we compute statistics. With large N we can model structure, find patterns, and build concept networks.",
            "A concept graph - nodes are concepts, edges are relations. A network reveals how knowledge is organised - not a list of facts, but a map of dependencies between ideas.",
            "L1 and L2 levels - L1 are the main domain categories, L2 are specific concepts. The hierarchy lets you navigate from the general to the specific and back.",
            "Scale and interpretation - 10 concepts is a glossary. 10,000 concepts is an ontology. Analysis methods must scale with data volume, otherwise meaning is lost in noise.",
            "The first computational semantic thesaurus - WordNet - contains around 155,000 English words grouped into 117,000 so-called synsets. Building it took the Princeton University team over 10 years of manual work (1985-2006). This shows that building structured knowledge is expensive even for natural language.",
            "Knowledge graphs in practice - the Google Knowledge Graph contains over 500 billion facts about 5 billion entities. When a search engine displays a side panel about a person or place, it uses exactly this kind of structure. Cognitive science builds similar structures for mental processes.",
            "The emergence effect in networks - in a concept graph, clusters often appear that were not planned by the designers. These clusters reveal the hidden structure of the domain. Discovering an unexpected cluster is often the starting point for a new theory.",
        ],
        "notes": [
            "How to read a concept network - start with L1 nodes (main categories). Edges between them show the strongest relations in the entire knowledge system.",
            "What network density means - a node with many edges is central to the domain. An isolated node is peripheral or too narrowly defined.",
            "Connections between concepts carry meaning - two similar-sounding words may occupy different places in the network, revealing whether they are synonyms or distinct concepts.",
            "It is worth checking which concepts connect two distant clusters - these are called semantic bridges and often correspond to interdisciplinary terms.",
        ],
        "tasks": [
            "Find the L1 node with the most connections to other nodes. What does this say about the centrality of that concept in the cognitive science domain?",
            "Is there an L2 concept that could belong to more than one L1? If so - what does that say about the ambiguity or interdisciplinary nature of that term?",
            "If you were to add a new node to the network - where would it fit? Which existing concepts would it connect to, and why?",
        ],
    },
}

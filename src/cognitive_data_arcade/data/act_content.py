"""Narrative texts for act intro screens and act bridge screens.

Each entry corresponds to module_idx 0-5 (same as _MODULES in menu.py).
ASCII only in any text rendered via pygame font — no Polish diacritics.
"""

from __future__ import annotations

# Act intro texts — shown once before first game of each act/module.
ACT_INTROS: list[dict[str, str]] = [
    {  # Act 0 — Module 1: Data Basics
        "title_pl": "Akt 1: Swiat pelny danych",
        "title_en": "Act 1: A World Full of Data",
        "text_pl": (
            "Zanim zaczniesz analizowac dane, musisz je zobaczyc.\n"
            "Sa wszedzie — w kazdym kliknieciu, kazdej decyzji,\n"
            "kazdej sekundzie ktora mierzysz.\n\n"
            "Ten akt to Twoj pierwszy krok: obserwuj, eksploruj,\n"
            "zadaj pierwsze pytania."
        ),
        "text_en": (
            "Before you can analyze data, you need to see it.\n"
            "It's everywhere — in every click, every decision,\n"
            "every second you measure.\n\n"
            "This act is your first step: observe, explore,\n"
            "ask your first questions."
        ),
    },
    {  # Act 1 — Module 2: Cognitive Experiments
        "title_pl": "Akt 2: Ty jestes danymi",
        "title_en": "Act 2: You Are the Data",
        "text_pl": (
            "Czas zmienic perspektywe.\n"
            "Przez szesc kolejnych gier to Ty jestes obiektem badania —\n"
            "Twoj czas reakcji, poziom uwagi i pamiec robocza\n"
            "stana sie danymi.\n\n"
            "Naukowcy mierza to od dziesiecioleci.\n"
            "Teraz zmierzysz siebie sam."
        ),
        "text_en": (
            "Time to shift perspective.\n"
            "For the next six games, you are the subject —\n"
            "your reaction time, attention, and working memory\n"
            "become data points.\n\n"
            "Scientists have been measuring these for decades.\n"
            "Now you'll measure yourself."
        ),
    },
    {  # Act 2 — Module 3: Statistics
        "title_pl": "Akt 3: Jak wyciagac sens z liczb",
        "title_en": "Act 3: Making Sense of Numbers",
        "text_pl": (
            "Masz dane — teraz potrzebujesz narzedzi.\n"
            "Rozklady, korelacje, hipotezy, predykcje —\n"
            "to jezyk ktorym naukowcy rozmawiaja z danymi.\n\n"
            "Ten akt uczy Cie tego jezyka:\n"
            "nie przez definicje, ale przez eksperyment."
        ),
        "text_en": (
            "You have data — now you need tools.\n"
            "Distributions, correlations, hypotheses, predictions —\n"
            "this is the language scientists use to speak with data.\n\n"
            "This act teaches you that language:\n"
            "not through definitions, but through experiment."
        ),
    },
    {  # Act 3 — Module 4: Machine Learning
        "title_pl": "Akt 4: Maszyny ucza sie",
        "title_en": "Act 4: Machines That Learn",
        "text_pl": (
            "Maszyny nie rozumieja — ucza sie z wzorcow w danych.\n"
            "Moga uczyc sie zbyt dobrze (overfitting),\n"
            "znajdowac wyjatki (anomalie)\n"
            "i klasyfikowac rzeczy, ktorych nigdy nie widzialy.\n\n"
            "Ten akt pokazuje jak to dziala od srodka, i gdzie sie sypie."
        ),
        "text_en": (
            "Machines don't understand — they learn from patterns in data.\n"
            "They can learn too well (overfitting),\n"
            "spot exceptions (anomalies),\n"
            "and classify things they've never seen before.\n\n"
            "This act shows you how that works from the inside, and where it breaks."
        ),
    },
    {  # Act 4 — Module 5: Language & NLP
        "title_pl": "Akt 5: Maszyny czytaja",
        "title_en": "Act 5: Machines That Read",
        "text_pl": (
            "Tekst to tez dane.\n"
            "Tokenizacja, wagi slow, emocje, semantyka —\n"
            "maszyny 'czytaja' inaczej niz Ty,\n"
            "ale moga znajdowac wzorce w milionach dokumentow.\n\n"
            "Na koncu: sprawdzisz czy Ty czy model jest lepszy."
        ),
        "text_en": (
            "Text is data too.\n"
            "Tokenization, word weights, emotions, semantics —\n"
            "machines 'read' differently than you do,\n"
            "but they find patterns across millions of documents.\n\n"
            "At the end: you'll find out who's better — you or the model."
        ),
    },
    {  # Act 5 — Module 6: Networks, Ethics & Finale
        "title_pl": "Akt 6: Dane tworza spoleczenstwo — i synteza",
        "title_en": "Act 6: Data Shapes Society — and the Synthesis",
        "text_pl": (
            "Algorytmy decyduja co widzisz w sieci,\n"
            "jak szybko dezinformacja sie rozprzestrzenia,\n"
            "w jakiej bance zyjiesz.\n\n"
            "A na koncu odkryjesz, ze przez cala te podroz\n"
            "bylies czyms wiecej niz obserwatorem.\n"
            "Bylies zestawem danych."
        ),
        "text_en": (
            "Algorithms decide what you see online,\n"
            "how fast misinformation spreads,\n"
            "what bubble you live in.\n\n"
            "And at the end you will discover that throughout this journey\n"
            "you were more than an observer.\n"
            "You were the dataset."
        ),
    },
]

# Bridge texts — shown in ModuleCompleteScene before badge reveal.
# module_idx 0-5. Last entry (5) is the grand finale — no "next module" bridge.
ACT_BRIDGES: list[dict[str, str]] = [
    {  # After Act 0
        "text_pl": (
            "Zauwazyles? W Reaction Time Lab\n"
            "dane nie byly skads pobrane — to Ty je stworzyles.\n"
            "Co to mowi o Tobie?"
        ),
        "text_en": (
            "Did you notice? In Reaction Time Lab\n"
            "the data wasn't sourced from somewhere — you created it.\n"
            "What does that say about you?"
        ),
    },
    {  # After Act 1
        "text_pl": (
            "Masz juz swoje dane.\nPytanie brzmi: co z nimi zrobic?\nJak wyciagnac z nich sens?"
        ),
        "text_en": (
            "You now have your own data.\n"
            "The question is: what do you do with it?\n"
            "How do you make sense of it?"
        ),
    },
    {  # After Act 2
        "text_pl": (
            "Wiesz juz jak analizowac dane.\nAle co jesli zamiast Ciebie — analizowalaby maszyna?"
        ),
        "text_en": (
            "You now know how to analyze data.\n"
            "But what if instead of you — a machine did the analyzing?"
        ),
    },
    {  # After Act 3
        "text_pl": (
            "Maszyny ucza sie z danych ktore my tworzymy.\n"
            "Ale co sie dzieje kiedy te algorytmy\n"
            "zaczynaja ksztaltowac spoleczenstwo?"
        ),
        "text_en": (
            "Machines learn from data we create.\n"
            "But what happens when those algorithms\n"
            "start shaping society?"
        ),
    },
    {  # After Act 4
        "text_pl": (
            "Znasz narzedzia, pulapki i konsekwencje.\n"
            "Czas zebys sam zaprojektowal system —\n"
            "i spojrzal na siebie z drugiej strony."
        ),
        "text_en": (
            "You know the tools, the pitfalls, and the consequences.\n"
            "Time to design a system yourself —\n"
            "and see yourself from the other side."
        ),
    },
    {  # After Act 5 (grand finale — no next act)
        "text_pl": (
            "Gratulacje.\n"
            "Przez caly ten kurs bylies jednoczesnie naukowcem\n"
            "i obiektem badania.\n"
            "Bylies zestawem danych."
        ),
        "text_en": (
            "Congratulations.\n"
            "Throughout this course you were both the scientist\n"
            "and the subject.\n"
            "You were the dataset."
        ),
    },
]

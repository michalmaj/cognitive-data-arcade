"""Narrative texts for act intro screens and act bridge screens.

Each entry corresponds to module_idx 0-5 (same as _MODULES in menu.py).

Fields:
  title_pl / title_en      — full title used in ActIntroScene (get_font, Unicode OK)
  short_title_pl / _en     — card title for SyllabusScene (get_font, Unicode OK)
  desc_pl / desc_en        — 1-2 line description for SyllabusScene cards
  text_pl / text_en        — multi-line narrative body for ActIntroScene
"""

from __future__ import annotations

# Act intro texts — shown once before first game of each act/module.
ACT_INTROS: list[dict[str, str]] = [
    {  # Act 0 - Module 1: Data Basics
        "title_pl": "Akt 1: Świat pełen danych",
        "title_en": "Act 1: A World Full of Data",
        "short_title_pl": "Świat pełen danych",
        "short_title_en": "A World Full of Data",
        "desc_pl": "Dane są wszędzie — w każdym kliknięciu i każdej decyzji.\nZacznij obserwować i zadawaj pierwsze pytania.",
        "desc_en": "Data is everywhere — in every click and every decision.\nStart observing and ask your first questions.",
        "text_pl": (
            "Zanim zaczniesz analizować dane, musisz je zobaczyć.\n"
            "Są wszędzie - w każdym kliknięciu, każdej decyzji,\n"
            "każdej sekundzie którą mierzysz.\n\n"
            "Ten akt to Twój pierwszy krok: obserwuj, eksploruj,\n"
            "zadaj pierwsze pytania."
        ),
        "text_en": (
            "Before you can analyze data, you need to see it.\n"
            "It's everywhere - in every click, every decision,\n"
            "every second you measure.\n\n"
            "This act is your first step: observe, explore,\n"
            "ask your first questions."
        ),
    },
    {  # Act 1 - Module 2: Cognitive Experiments
        "title_pl": "Akt 2: Ty jesteś danymi",
        "title_en": "Act 2: You Are the Data",
        "short_title_pl": "Ty jesteś danymi",
        "short_title_en": "You Are the Data",
        "desc_pl": "Przez sześć gier to Ty jesteś obiektem badania.\nTwój czas reakcji i pamięć robocza stają się danymi.",
        "desc_en": "For six games you are the subject under study.\nYour reaction time and working memory become data points.",
        "text_pl": (
            "Czas zmienić perspektywę.\n"
            "Przez sześć kolejnych gier to Ty jesteś obiektem badania -\n"
            "Twój czas reakcji, poziom uwagi i pamięć robocza\n"
            "staną się danymi.\n\n"
            "Naukowcy mierzą to od dziesięcioleci.\n"
            "Teraz zmierzysz siebie sam."
        ),
        "text_en": (
            "Time to shift perspective.\n"
            "For the next six games, you are the subject -\n"
            "your reaction time, attention, and working memory\n"
            "become data points.\n\n"
            "Scientists have been measuring these for decades.\n"
            "Now you'll measure yourself."
        ),
    },
    {  # Act 2 - Module 3: Statistics
        "title_pl": "Akt 3: Jak wyciągnąć sens z liczb",
        "title_en": "Act 3: Making Sense of Numbers",
        "short_title_pl": "Sens z liczb",
        "short_title_en": "Making Sense of Numbers",
        "desc_pl": "Rozkłady, korelacje, hipotezy, predykcje —\njęzyk którym nauka rozmawia z danymi.",
        "desc_en": "Distributions, correlations, hypotheses, predictions —\nthe language scientists use to speak with data.",
        "text_pl": (
            "Masz dane - teraz potrzebujesz narzędzi.\n"
            "Rozkłady, korelacje, hipotezy, predykcje -\n"
            "to język którym naukowcy rozmawiają z danymi.\n\n"
            "Ten akt uczy Cię tego języka:\n"
            "nie przez definicje, ale przez eksperyment."
        ),
        "text_en": (
            "You have data - now you need tools.\n"
            "Distributions, correlations, hypotheses, predictions -\n"
            "this is the language scientists use to speak with data.\n\n"
            "This act teaches you that language:\n"
            "not through definitions, but through experiment."
        ),
    },
    {  # Act 3 - Module 4: Machine Learning
        "title_pl": "Akt 4: Maszyny się uczą",
        "title_en": "Act 4: Machines That Learn",
        "short_title_pl": "Maszyny się uczą",
        "short_title_en": "Machines That Learn",
        "desc_pl": "Maszyny uczą się z wzorców w danych — mogą uczyć się\nzbyt dobrze, wykrywać anomalie i klasyfikować nieznane.",
        "desc_en": "Machines learn from patterns — they can overfit,\nspot anomalies and classify things they've never seen.",
        "text_pl": (
            "Maszyny nie rozumieją - uczą się z wzorców w danych.\n"
            "Mogą uczyć się zbyt dobrze (overfitting),\n"
            "znajdować wyjątki (anomalie)\n"
            "i klasyfikować rzeczy, których nigdy nie widziały.\n\n"
            "Ten akt pokazuje jak to działa od środka, i gdzie się sypie."
        ),
        "text_en": (
            "Machines don't understand - they learn from patterns in data.\n"
            "They can learn too well (overfitting),\n"
            "spot exceptions (anomalies),\n"
            "and classify things they've never seen before.\n\n"
            "This act shows you how that works from the inside, and where it breaks."
        ),
    },
    {  # Act 4 - Module 5: Language & NLP
        "title_pl": "Akt 5: Maszyny czytają",
        "title_en": "Act 5: Machines That Read",
        "short_title_pl": "Maszyny czytają",
        "short_title_en": "Machines That Read",
        "desc_pl": "Tekst to też dane. Tokenizacja, wagi słów, semantyka —\nmaszyny 'czytają' inaczej, lecz skalują się na miliony tekstów.",
        "desc_en": "Text is data too. Tokenization, word weights, semantics —\nmachines 'read' differently but scale to millions of documents.",
        "text_pl": (
            "Tekst to też dane.\n"
            "Tokenizacja, wagi słów, emocje, semantyka -\n"
            "maszyny 'czytają' inaczej niż Ty,\n"
            "ale mogą znajdować wzorce w milionach dokumentów.\n\n"
            "Na końcu: sprawdzisz czy Ty czy model jest lepszy."
        ),
        "text_en": (
            "Text is data too.\n"
            "Tokenization, word weights, emotions, semantics -\n"
            "machines 'read' differently than you do,\n"
            "but they find patterns across millions of documents.\n\n"
            "At the end: you'll find out who's better - you or the model."
        ),
    },
    {  # Act 5 - Module 6: Networks, Ethics & Finale
        "title_pl": "Akt 6: Dane tworzą społeczeństwo - i synteza",
        "title_en": "Act 6: Data Shapes Society - and the Synthesis",
        "short_title_pl": "Dane tworzą społeczeństwo",
        "short_title_en": "Data Shapes Society",
        "desc_pl": "Algorytmy decydują co widzisz w sieci i w jakiej bańce żyjesz.\nNa końcu odkryjesz, że przez całą podróż byłeś zestawem danych.",
        "desc_en": "Algorithms decide what you see online and what bubble you live in.\nAt the end you'll discover that throughout this journey you were the dataset.",
        "text_pl": (
            "Algorytmy decydują co widzisz w sieci,\n"
            "jak szybko dezinformacja się rozprzestrzenia,\n"
            "w jakiej bańce żyjesz.\n\n"
            "A na końcu odkryjesz, że przez całą tę podróż\n"
            "byłeś czymś więcej niż obserwatorem.\n"
            "Byłeś zestawem danych."
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
            "Zauważyłeś? W Reaction Time Lab\n"
            "dane nie były skądś pobrane - to Ty je stworzyłeś.\n"
            "Co to mówi o Tobie?"
        ),
        "text_en": (
            "Did you notice? In Reaction Time Lab\n"
            "the data wasn't sourced from somewhere - you created it.\n"
            "What does that say about you?"
        ),
    },
    {  # After Act 1
        "text_pl": (
            "Masz już swoje dane.\nPytanie brzmi: co z nimi zrobić?\nJak wyciągnąć z nich sens?"
        ),
        "text_en": (
            "You now have your own data.\n"
            "The question is: what do you do with it?\n"
            "How do you make sense of it?"
        ),
    },
    {  # After Act 2
        "text_pl": (
            "Wiesz już jak analizować dane.\nAle co jeśli zamiast Ciebie - analizowałaby maszyna?"
        ),
        "text_en": (
            "You now know how to analyze data.\n"
            "But what if instead of you - a machine did the analyzing?"
        ),
    },
    {  # After Act 3
        "text_pl": (
            "Maszyny uczą się z danych które my tworzymy.\n"
            "Ale co się dzieje kiedy te algorytmy\n"
            "zaczynają kształtować społeczeństwo?"
        ),
        "text_en": (
            "Machines learn from data we create.\n"
            "But what happens when those algorithms\n"
            "start shaping society?"
        ),
    },
    {  # After Act 4
        "text_pl": (
            "Znasz narzędzia, pułapki i konsekwencje.\n"
            "Czas żebyś sam zaprojektował system -\n"
            "i spojrzał na siebie z drugiej strony."
        ),
        "text_en": (
            "You know the tools, the pitfalls, and the consequences.\n"
            "Time to design a system yourself -\n"
            "and see yourself from the other side."
        ),
    },
    {  # After Act 5 (grand finale — no next act)
        "text_pl": (
            "Gratulacje.\n"
            "Przez cały ten kurs byłeś jednocześnie naukowcem\n"
            "i obiektem badania.\n"
            "Byłeś zestawem danych."
        ),
        "text_en": (
            "Congratulations.\n"
            "Throughout this course you were both the scientist\n"
            "and the subject.\n"
            "You were the dataset."
        ),
    },
]

# src/cognitive_data_arcade/lessons/lesson_12.py
"""Lesson 12 -- Comparing Cognitive Tasks (Cognitive Dashboard)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Po co porownywac zadania poznawcze? Kazde zadanie mierzy inny aspekt umyslu: prosty czas reakcji to czysty czas motoryczny i sensoryczny; Stroop mierzy kontrole wykonawcza; Flanker -- selektywna uwage; Go/No-Go -- hamowanie impulsow. Zestawiajac je razem, mozemy zobaczyc profil poznawczy danej osoby.",
            "Efekt Stroopa -- interferencja slowo vs. kolor. Kiedy kolor atramentu nie zgadza sie ze znaczeniem slowa (np. slowo CZERWONY napisane zielonym atramentem), mozg musi aktywnie hamowac automatyczne czytanie. Roznica RT miedzy warunkiem niezgodnym a zgodnym to miara kontroli wykonawczej. Typowo wynosi 50-100 ms.",
            "Efekt Flankera -- koszty uwagi selektywnej. Kiedy strzalki flankujace wskazuja w przeciwnym kierunku niz strzalka centralna, czas reakcji rosnie. Mowi to, ze mozg przetwarza caly wyswietlany obszar, nie tylko punkt centralny. Efekt Flankera jest zazwyczaj mniejszy niz efekt Stroopa (30-60 ms).",
            "Go/No-Go -- hamowanie jako osobny komponent. W tym zadaniu czekasz na zielone kolo (Go) i powstrzymujesz sie przed nacisnieciem przy czerwonym (No-Go). Falszywe alarmy -- nacisniecia na No-Go -- mierza impulsywnosc. Hit rate mierzy szybkosc i czulosc. To inne zdolnosci niz interferencja.",
            "Dlaczego RT jest punktem odniesienia? Prosty czas reakcji (jeden bodziec, jedna odpowiedz, brak konfliktu) daje nam baseline -- minimalny czas przetwarzania sensoryczno-motorycznego. Efekty Stroopa i Flankera mierzone sa wzgledem tego baseline. Im wyzszy baseline, tym wolniej dzialaja wszystkie zdolnosci.",
        ],
        "notes": [
            "Kolejnosc zadan ma znaczenie. Efekty poznawcze moga byc wieksze na poczatku sesji (zimny mozg) lub pod koniec (zmeczenie). W profesjonalnych badaniach kolejnosc jest randomizowana miedzy uczestnikami. W naszym dashboardzie mozesz wybrac kolejnosc -- eksperymentuj!",
            "8 prob to za malo na pewne wnioski. W prawdziwych badaniach kazde zadanie ma minimum 30-60 prob, zeby srednia RT byla stabilna statystycznie. Z 8 prob mozesz zobaczyc swoje tendencje, ale nie traktuj wyniku jako ostatecznego orzeczenia o swoich zdolnosciach.",
            "Roznice miedzy ludzmi sa duze i normalne. Ktos moze miec duzy efekt Stroopa i maly efekt Flankera -- i to OK. Profile poznawcze sa czescia indywidualnej zmiennosci. Wiek, zmeczenie, kawa i trening wplywaja na wyniki bardziej niz inteligencja.",
        ],
        "tasks": [
            "Porownaj swoj efekt Stroopa i efekt Flankera: ktory jest wiekszy? Jak myslisz, dlaczego? Czy slowa sa trudniejsze do zignorowania niz kierunki strzalek?",
            "Oblicz swoj koszt uwagi -- o ile procent wolniejszy jestes w warunkach niezgodnych niz zgodnych? Podziel efekt (ms) przez sredni RT w warunku zgodnym i pomnoz przez 100. Jak ten procent ma sie do efektow z literatury (typowo 10-25%)?",
            "Zagraj raz w wersji zagraj i raz w wersji syntetyczne. Porownaj wyniki -- czy syntetyczne dane wypadaja podobnie do Twoich? Jak bardzo roznia sie profile poznawcze? Co to mowi o typowym uczestniku eksperymentu?",
        ],
    },
    "en": {
        "theory": [
            "Why compare cognitive tasks? Each task measures a different aspect of the mind: simple reaction time captures pure sensorimotor speed; Stroop measures executive control; Flanker measures selective attention; Go/No-Go measures impulse inhibition. Comparing them side by side reveals a cognitive profile.",
            "The Stroop Effect -- word vs. colour interference. When the ink colour conflicts with the word's meaning (e.g. the word RED printed in green ink), the brain must actively suppress automatic reading. The RT difference between incongruent and congruent trials measures executive control. Typically 50-100 ms.",
            "The Flanker Effect -- selective attention cost. When flanking arrows point opposite to the central target, RT increases. This tells us the brain processes the whole display area, not just the focus point. The Flanker effect is usually smaller than Stroop (30-60 ms).",
            "Go/No-Go -- inhibition as a separate component. You wait for a green circle (Go) and withhold a press for red (No-Go). False alarms -- pressing on No-Go -- measure impulsivity. Hit rate measures speed and sensitivity. These are different abilities from interference control.",
            "Why is RT the baseline? Simple reaction time (one stimulus, one response, no conflict) gives us a floor -- the minimum sensorimotor processing time. Stroop and Flanker effects are measured relative to this baseline. A higher baseline means all cognitive abilities are globally slower.",
        ],
        "notes": [
            "Task order matters. Cognitive effects can be larger at the start of a session (cold brain) or at the end (fatigue). In professional research, order is randomised across participants. In our dashboard, you choose the order -- experiment!",
            "8 trials is too few for certainty. In real research, each task has at least 30-60 trials for a statistically stable mean RT. With 8 trials you can see your tendencies, but don't treat the result as a definitive verdict on your abilities.",
            "Individual differences are large and normal. Someone may have a large Stroop effect and a small Flanker effect -- that is fine. Cognitive profiles are part of individual variability. Age, fatigue, coffee, and practice influence results far more than raw intelligence.",
        ],
        "tasks": [
            "Compare your Stroop and Flanker effects: which is larger? Why do you think that is? Are words harder to ignore than arrow directions?",
            "Calculate your attention cost -- by what percentage are you slower in incongruent than congruent conditions? Divide the effect (ms) by mean congruent RT and multiply by 100. How does this compare to typical literature values (usually 10-25%)?",
            "Play once with Play mode and once with Synthetic data. Compare the profiles -- do the synthetic results resemble yours? How different are the cognitive profiles? What does this say about the typical experimental participant?",
        ],
    },
}

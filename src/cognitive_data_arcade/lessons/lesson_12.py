# src/cognitive_data_arcade/lessons/lesson_12.py
"""Lesson 12 - Comparing Cognitive Tasks (Cognitive Dashboard)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Po co porównywać zadania poznawcze? Każde zadanie mierzy inny aspekt umysłu: prosty czas reakcji to czysty czas motoryczny i sensoryczny; Stroop mierzy kontrolę wykonawczą; Flanker - selektywną uwagę; Go/No-Go - hamowanie impulsów. Zestawiając je razem, możemy zobaczyć profil poznawczy danej osoby.",
            "Efekt Stroopa - interferencja słowo vs. kolor. Kiedy kolor atramentu nie zgadza się ze znaczeniem słowa (np. słowo CZERWONY napisane zielonym atramentem), mózg musi aktywnie hamować automatyczne czytanie. Różnica RT między warunkiem niezgodnym a zgodnym to miara kontroli wykonawczej. Typowo wynosi 50-100 ms.",
            "Efekt Flankera - koszty uwagi selektywnej. Kiedy strzałki flankujące wskazują w przeciwnym kierunku niż strzałka centralna, czas reakcji rośnie. Mówi to, że mózg przetwarza cały wyświetlany obszar, nie tylko punkt centralny. Efekt Flankera jest zazwyczaj mniejszy niż efekt Stroopa (30-60 ms).",
            "Go/No-Go - hamowanie jako osobny komponent. W tym zadaniu czekasz na zielone koło (Go) i powstrzymujesz się przed naciśnięciem przy czerwonym (No-Go). Fałszywe alarmy - naciśnięcia na No-Go - mierzą impulsywność. Hit rate mierzy szybkość i czułość. To inne zdolności niż interferencja.",
            "Dlaczego RT jest punktem odniesienia? Prosty czas reakcji (jeden bodziec, jedna odpowiedź, brak konfliktu) daje nam baseline - minimalny czas przetwarzania sensoryczno-motorycznego. Efekty Stroopa i Flankera mierzone są względem tego baseline. Im wyższy baseline, tym wolniej działają wszystkie zdolności.",
        ],
        "notes": [
            "Kolejność zadań ma znaczenie. Efekty poznawcze mogą być większe na początku sesji (zimny mózg) lub pod koniec (zmęczenie). W profesjonalnych badaniach kolejność jest randomizowana między uczestnikami. W naszym dashboardzie możesz wybrać kolejność - eksperymentuj!",
            "8 prób to za mało na pewne wnioski. W prawdziwych badaniach każde zadanie ma minimum 30-60 prób, żeby średnia RT była stabilna statystycznie. Z 8 prób możesz zobaczyć swoje tendencje, ale nie traktuj wyniku jako ostatecznego orzeczenia o swoich zdolnościach.",
            "Różnice między ludźmi są duże i normalne. Ktoś może mieć duży efekt Stroopa i mały efekt Flankera - i to OK. Profile poznawcze są częścią indywidualnej zmienności. Wiek, zmęczenie, kawa i trening wpływają na wyniki bardziej niż inteligencja.",
        ],
        "tasks": [
            "Porównaj swój efekt Stroopa i efekt Flankera: który jest większy? Jak myślisz, dlaczego? Czy słowa są trudniejsze do zignorowania niż kierunki strzałek?",
            "Oblicz swój koszt uwagi - o ile procent wolniejszy jesteś w warunkach niezgodnych niż zgodnych? Podziel efekt (ms) przez średni RT w warunku zgodnym i pomnóż przez 100. Jak ten procent ma się do efektów z literatury (typowo 10-25%)?",
            "Zagraj raz w wersji zagraj i raz w wersji syntetyczne. Porównaj wyniki - czy syntetyczne dane wypadają podobnie do Twoich? Jak bardzo różnią się profile poznawcze? Co to mówi o typowym uczestniku eksperymentu?",
        ],
    },
    "en": {
        "theory": [
            "Why compare cognitive tasks? Each task measures a different aspect of the mind: simple reaction time captures pure sensorimotor speed; Stroop measures executive control; Flanker measures selective attention; Go/No-Go measures impulse inhibition. Comparing them side by side reveals a cognitive profile.",
            "The Stroop Effect - word vs. colour interference. When the ink colour conflicts with the word's meaning (e.g. the word RED printed in green ink), the brain must actively suppress automatic reading. The RT difference between incongruent and congruent trials measures executive control. Typically 50-100 ms.",
            "The Flanker Effect - selective attention cost. When flanking arrows point opposite to the central target, RT increases. This tells us the brain processes the whole display area, not just the focus point. The Flanker effect is usually smaller than Stroop (30-60 ms).",
            "Go/No-Go - inhibition as a separate component. You wait for a green circle (Go) and withhold a press for red (No-Go). False alarms - pressing on No-Go - measure impulsivity. Hit rate measures speed and sensitivity. These are different abilities from interference control.",
            "Why is RT the baseline? Simple reaction time (one stimulus, one response, no conflict) gives us a floor - the minimum sensorimotor processing time. Stroop and Flanker effects are measured relative to this baseline. A higher baseline means all cognitive abilities are globally slower.",
        ],
        "notes": [
            "Task order matters. Cognitive effects can be larger at the start of a session (cold brain) or at the end (fatigue). In professional research, order is randomised across participants. In our dashboard, you choose the order - experiment!",
            "8 trials is too few for certainty. In real research, each task has at least 30-60 trials for a statistically stable mean RT. With 8 trials you can see your tendencies, but don't treat the result as a definitive verdict on your abilities.",
            "Individual differences are large and normal. Someone may have a large Stroop effect and a small Flanker effect - that is fine. Cognitive profiles are part of individual variability. Age, fatigue, coffee, and practice influence results far more than raw intelligence.",
        ],
        "tasks": [
            "Compare your Stroop and Flanker effects: which is larger? Why do you think that is? Are words harder to ignore than arrow directions?",
            "Calculate your attention cost - by what percentage are you slower in incongruent than congruent conditions? Divide the effect (ms) by mean congruent RT and multiply by 100. How does this compare to typical literature values (usually 10-25%)?",
            "Play once with Play mode and once with Synthetic data. Compare the profiles - do the synthetic results resemble yours? How different are the cognitive profiles? What does this say about the typical experimental participant?",
        ],
    },
}

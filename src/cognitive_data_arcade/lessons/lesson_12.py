"""Lesson 12 - Comparing Cognitive Tasks (Cognitive Dashboard)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Po co porównywać zadania poznawcze? Każde zadanie mierzy inny aspekt umysłu: prosty czas reakcji to czysty czas motoryczny i sensoryczny; Stroop mierzy kontrolę wykonawczą; Flanker - selektywną uwagę; Go/No-Go - hamowanie impulsów. Zestawiając je razem, można zobaczyć profil poznawczy danej osoby.",
            "Bateria testów neuropsychologicznych - podejście to wywodzi sie z baterii Halsteada-Reitana (1955), jednego z pierwszych standaryzowanych zestawów testów oceniających funkcje mózgu. Luria w ZSRR rozwijał podobne podejście kliniczne niezależnie. Współczesne baterie komputerowe (np. Cambridge Neuropsychological Test Automated Battery, CANTAB) mogą mierzyć kilkanaście funkcji w ciągu godziny.",
            "Efekt Stroopa - interferencja słowo vs. kolor. Gdy kolor atramentu nie zgadza sie ze znaczeniem słowa (np. słowo CZERWONY napisane zielonym atramentem), mózg musi aktywnie hamować automatyczne czytanie. Różnica RT między warunkiem niezgodnym a zgodnym mierzy kontrolę wykonawczą. Typowo 50-100 ms.",
            "Efekt Flankera - koszty uwagi selektywnej. Gdy strzałki flankujące wskazują w przeciwnym kierunku niż strzałka centralna, RT rośnie. Efekt Flankera jest zazwyczaj mniejszy niż efekt Stroopa (30-60 ms).",
            "Go/No-Go - hamowanie jako osobny komponent. Fałszywe alarmy - naciśniecia na No-Go - mierzą impulsywność. Hit rate mierzy szybkość i czułość. To inne zdolności niż interferencja.",
            "Jedność i różnorodność funkcji wykonawczych (Friedman i in., 2008) - badanie bliźniąt jednojajowych wykazało, że trzy komponenty EF (hamowanie, monitorowanie, przełączanie) mają wspólny czynnik genetyczny (ok. 99% genów wspólnych), ale każdy ma też unikalny komponent. Wysoki wynik w jednym zadaniu EF nie gwarantuje wysokiego wyniku w innym.",
            "Dlaczego RT jest punktem odniesienia? Prosty czas reakcji (jeden bodziec, jedna odpowiedź, brak konfliktu) daje baseline - minimalny czas przetwarzania sensoryczno-motorycznego. Efekty Stroopa i Flankera mierzone są względem tego baseline.",
        ],
        "notes": [
            "Kolejność zadań ma znaczenie. Efekty poznawcze mogą być większe na początku sesji (zimny mózg) lub pod koniec (zmęczenie). W profesjonalnych badaniach kolejność jest randomizowana między uczestnikami.",
            "8 prób to za mało na pewne wnioski. W prawdziwych badaniach każde zadanie ma minimum 30-60 prób, żeby średnia RT była stabilna statystycznie. Z 8 prób widać tendencje, ale nie trafność diagnozy.",
            "Różnice między ludźmi są duże i normalne. Ktoś może mieć duży efekt Stroopa i mały efekt Flankera. Profile poznawcze są częścią indywidualnej zmienności. Wiek, zmęczenie, kofeina i trening wpływają na wyniki bardziej niż ogólna inteligencja.",
        ],
        "tasks": [
            "Porównaj efekt Stroopa i efekt Flankera: który jest większy? Dlaczego słowa mogą być trudniejsze do zignorowania niż kierunki strzałek?",
            "Oblicz koszt uwagi - o ile procent wolniejszy jest czas reakcji w warunkach niezgodnych niż zgodnych? Podziel efekt (ms) przez średni RT w warunku zgodnym i pomnóż przez 100. Jak ten procent wypada na tle typowych wartości z literatury (ok. 10-25%)?",
            "Zagraj raz w trybie rzeczywistym i raz z danymi syntetycznymi. Porównaj profile - czy syntetyczne dane przypominają wyniki rzeczywiste? Jak różnią sie profile poznawcze?",
        ],
    },
    "en": {
        "theory": [
            "Why compare cognitive tasks? Each task measures a different aspect of the mind: simple reaction time captures pure sensorimotor speed; Stroop measures executive control; Flanker measures selective attention; Go/No-Go measures impulse inhibition. Comparing them side by side reveals a cognitive profile.",
            "Neuropsychological test batteries - this approach traces back to the Halstead-Reitan Battery (1955), one of the first standardised assessments of brain function. Luria developed a parallel clinical approach in the USSR independently. Modern computerised batteries (e.g. Cambridge Neuropsychological Test Automated Battery, CANTAB) can measure a dozen functions within an hour.",
            "The Stroop Effect - word vs. colour interference. When the ink colour conflicts with the word's meaning (e.g. the word RED printed in green ink), the brain must actively suppress automatic reading. The RT difference between incongruent and congruent trials measures executive control. Typically 50-100 ms.",
            "The Flanker Effect - selective attention cost. When flanking arrows point opposite to the central target, RT increases. The Flanker effect is usually smaller than Stroop (30-60 ms).",
            "Go/No-Go - inhibition as a separate component. False alarms - pressing on No-Go - measure impulsivity. Hit rate measures speed and sensitivity. These are different abilities from interference control.",
            "Unity and diversity of executive functions (Friedman et al., 2008) - a study of monozygotic twins found that three EF components (inhibition, monitoring, shifting) share a common genetic factor (approximately 99% shared genes), but each also has a unique component. A high score on one EF task does not guarantee a high score on another.",
            "Why is RT the baseline? Simple reaction time (one stimulus, one response, no conflict) provides a floor - the minimum sensorimotor processing time. Stroop and Flanker effects are measured relative to this baseline.",
        ],
        "notes": [
            "Task order matters. Cognitive effects can be larger at the start of a session (cold brain) or at the end (fatigue). In professional research, order is randomised across participants.",
            "8 trials is too few for certainty. In real research, each task has at least 30-60 trials for a statistically stable mean RT. With 8 trials tendencies are visible, but not diagnostic accuracy.",
            "Individual differences are large and normal. Someone may have a large Stroop effect and a small Flanker effect. Cognitive profiles are part of individual variability. Age, fatigue, caffeine, and practice influence results far more than general intelligence.",
        ],
        "tasks": [
            "Compare the Stroop and Flanker effects: which is larger? Why might words be harder to ignore than arrow directions?",
            "Calculate the attention cost - by what percentage is RT slower in incongruent than congruent conditions? Divide the effect (ms) by mean congruent RT and multiply by 100. How does this compare to typical literature values (usually 10-25%)?",
            "Run once in play mode and once with synthetic data. Compare the profiles - do the synthetic results resemble real results? How different are the cognitive profiles?",
        ],
    },
}

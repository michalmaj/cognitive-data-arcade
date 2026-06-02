"""Lesson 09 — Response Inhibition (Go/No-Go Guard)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Zadanie Go/No-Go — przy bodźcu Go (częsty) naciśnij klawisz jak najszybciej. Przy bodźcu No-Go (rzadki) powstrzymaj się. Mierzy hamowanie motoryczne — zdolność do zatrzymania przygotowanej odpowiedzi.",
            "Fałszywy alarm (FA) — naciśnięcie klawisza przy bodźcu No-Go to wskaźnik impulsywności. FA rate 5–15% to norma. Powyżej 25% sygnalizuje trudności z hamowaniem odpowiedzi.",
            "Poprawne odrzucenie — powstrzymanie się przy No-Go to aktywny proces hamowania, nie brak odpowiedzi. Wymaga wykrycia bodźca, rozpoznania go jako No-Go i zablokowania przygotowanej reakcji.",
            "Signal Detection Theory — d' (d-prime) mierzy zdolność do rozróżnienia Go od No-Go niezależnie od strategii odpowiadania. Wysokie d' = dobra czułość percepcyjna.",
            "Zastosowania kliniczne — Go/No-Go używany jest w ocenie ADHD (wysoki FA), impulsywności, zdolności do prowadzenia pojazdów i monitorowaniu efektów leków na funkcje wykonawcze.",
        ],
        "notes": [
            "FA rate vs. miss rate — fałszywy alarm (naciśnięcie przy No-Go) i opuszczenie (brak reakcji przy Go) to dwa różne błędy. FA mierzy impulsywność. Miss mierzy spowolnienie lub rozproszenie uwagi.",
            "Hamowanie słabnie z czasem — FA rate często rośnie pod koniec bloku. Hamowanie to zasób, który się wyczerpuje. Wzrost FA w końcówce sesji to normalny efekt zmęczenia hamowania.",
            "Proporcja No-Go ma znaczenie — im więcej bodźców No-Go, tym łatwiej hamować (rzadsze Go = mniejsza automatyczność naciśnięcia). Wyniki porównuj tylko przy tej samej proporcji Go/No-Go.",
        ],
        "tasks": [
            "Jaki jest Twój FA rate? Oblicz: (liczba FA) / (liczba prób No-Go) × 100%. Czy mieścisz się w normie 5–15%? Co wyższy lub niższy wynik mówi o Twojej kontroli impulsów?",
            "Czy Twój FA rate rośnie w późniejszych blokach? Jeśli tak — o ile? Co to mówi o Twoim hamowaniu pod wpływem zmęczenia poznawczego?",
            "Porównaj swój RT w próbach Go z wynikami z RT Lab (Lekcja 02). Czy dodanie zadania hamowania (No-Go) zmieniło Twój czas reakcji na bodźce Go?",
        ],
    },
    "en": {
        "theory": [
            "The Go/No-Go task — on a Go stimulus (frequent) press the key as fast as possible. On a No-Go stimulus (rare) withhold. It measures motor inhibition — the ability to stop a prepared response.",
            "False alarm (FA) — pressing the key on a No-Go stimulus is an index of impulsivity. FA rate of 5–15% is normal. Above 25% signals difficulty inhibiting responses.",
            "Correct rejection — withholding on No-Go is an active inhibition process, not the absence of a response. It requires detecting the stimulus, recognising it as No-Go, and blocking the prepared action.",
            "Signal Detection Theory — d' (d-prime) measures the ability to discriminate Go from No-Go independently of response strategy. High d' = good perceptual sensitivity.",
            "Clinical applications — Go/No-Go is used in assessment of ADHD (high FA), impulsivity, driving fitness, and monitoring medication effects on executive functions.",
        ],
        "notes": [
            "FA rate vs. miss rate — a false alarm (pressing on No-Go) and a miss (failing to press on Go) are two different errors. FA measures impulsivity. Miss measures slowing or inattention.",
            "Inhibition depletes over time — FA rate often rises towards the end of a block. Inhibition is a resource that is consumed. A rise in FA towards the end of a session is a normal fatigue effect.",
            "The No-Go proportion matters — the more No-Go stimuli there are, the easier it is to inhibit (fewer Go stimuli = less automaticity of pressing). Only compare results with the same Go/No-Go ratio.",
        ],
        "tasks": [
            "What is your FA rate? Calculate: (number of FAs) / (number of No-Go trials) × 100%. Are you within the 5–15% norm? What does a higher or lower result say about your impulse control?",
            "Does your FA rate increase in later blocks? If so — by how much? What does this say about your inhibition under cognitive fatigue?",
            "Compare your RT on Go trials with results from RT Lab (Lesson 02). Did adding the inhibition task (No-Go) change your reaction time to Go stimuli?",
        ],
    },
}

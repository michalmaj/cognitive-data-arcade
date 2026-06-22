"""Lesson 09 - Response Inhibition (Go/No-Go Guard)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Zadanie Go/No-Go - przy bodźcu Go (częsty) naciśnij klawisz jak najszybciej. Przy bodźcu No-Go (rzadki) powstrzymaj sie. Mierzy hamowanie motoryczne - zdolność do zatrzymania przygotowanej odpowiedzi.",
            "Fałszywy alarm (FA) - naciśniecie klawisza przy bodźcu No-Go to wskaźnik impulsywności. FA rate 5-15% to norma. Powyżej 25% sygnalizuje trudności z hamowaniem odpowiedzi.",
            "Paradygmat sygnału stopu (Logan, 1984) - bardziej zaawansowana wersja hamowania: po bodźcu Go pojawia sie opcjonalny sygnał stopu z różnym opóźnieniem. Mierzy SSRT (Stop-Signal Reaction Time) - czas potrzebny do zablokowania już rozpoczętej odpowiedzi. Typowa wartość SSRT wynosi 200-250 ms.",
            "Poprawne odrzucenie - powstrzymanie sie przy No-Go to aktywny proces hamowania, nie brak odpowiedzi. Wymaga wykrycia bodźca, rozpoznania go jako No-Go i zablokowania przygotowanej reakcji.",
            "Signal Detection Theory - d' (d-prime) mierzy zdolność do rozróżnienia Go od No-Go niezależnie od strategii odpowiadania. Wysokie d' = dobra czułość percepcyjna.",
            "Neurobiologia hamowania - uszkodzenie kory oczodołowo-czołowej (OFC) sprawia, że pacjenci nie mogą hamować odpowiedzi nawet gdy wiedzą, że powinni (Bechara i in., 1994). Niski poziom dopaminy w korze przedczołowej koreluje z wysokim FA rate; metylofenidat (Ritalin) obniża FA rate w ADHD.",
            "Zastosowania kliniczne - Go/No-Go używany jest w ocenie ADHD (wysoki FA), impulsywności, zdolności do prowadzenia pojazdów i monitorowaniu efektów leków na funkcje wykonawcze.",
        ],
        "notes": [
            "FA rate vs. miss rate - fałszywy alarm (naciśniecie przy No-Go) i opuszczenie (brak reakcji przy Go) to dwa różne błędy. FA mierzy impulsywność. Miss mierzy spowolnienie lub rozproszenie uwagi.",
            "Hamowanie słabnie z czasem - FA rate często rośnie pod koniec bloku. Hamowanie to zasób, który sie wyczerpuje. Wzrost FA w końcówce sesji to normalny efekt zmęczenia hamowania.",
            "Proporcja No-Go ma znaczenie - im więcej bodźców No-Go, tym łatwiej hamować (rzadsze Go = mniejsza automatyczność naciśniecia). Wyniki porównuje sie tylko przy tej samej proporcji Go/No-Go.",
        ],
        "tasks": [
            "Jaki jest FA rate? Oblicz: (liczba FA) / (liczba prób No-Go) x 100%. Czy mieści sie w normie 5-15%?",
            "Czy FA rate rośnie w późniejszych blokach? Jeśli tak - o ile? Co to mówi o hamowaniu pod wpływem zmęczenia poznawczego?",
            "Porównaj RT w próbach Go z wynikami z RT Lab (lekcja 02). Czy dodanie zadania hamowania (No-Go) wpłynęło na czas reakcji na bodźce Go?",
        ],
    },
    "en": {
        "theory": [
            "The Go/No-Go task - on a Go stimulus (frequent) press the key as fast as possible. On a No-Go stimulus (rare) withhold. It measures motor inhibition - the ability to stop a prepared response.",
            "False alarm (FA) - pressing the key on a No-Go stimulus is an index of impulsivity. FA rate of 5-15% is normal. Above 25% signals difficulty inhibiting responses.",
            "Stop-signal paradigm (Logan, 1984) - a more sophisticated inhibition version: after a Go stimulus, an optional stop signal appears with variable delay. It measures SSRT (Stop-Signal Reaction Time) - the time needed to cancel an already-initiated response. Typical SSRT is 200-250 ms.",
            "Correct rejection - withholding on No-Go is an active inhibition process, not the absence of a response. It requires detecting the stimulus, recognising it as No-Go, and blocking the prepared action.",
            "Signal Detection Theory - d' (d-prime) measures the ability to discriminate Go from No-Go independently of response strategy. High d' = good perceptual sensitivity.",
            "Neurobiology of inhibition - damage to the orbitofrontal cortex (OFC) prevents patients from inhibiting responses even when they know they should (Bechara et al., 1994). Low dopamine in the prefrontal cortex correlates with high FA rate; methylphenidate (Ritalin) reduces FA rate in ADHD.",
            "Clinical applications - Go/No-Go is used in assessment of ADHD (high FA), impulsivity, driving fitness, and monitoring medication effects on executive functions.",
        ],
        "notes": [
            "FA rate vs. miss rate - a false alarm (pressing on No-Go) and a miss (failing to press on Go) are two different errors. FA measures impulsivity. Miss measures slowing or inattention.",
            "Inhibition depletes over time - FA rate often rises towards the end of a block. Inhibition is a resource that is consumed. A rise in FA towards the end of a session is a normal fatigue effect.",
            "The No-Go proportion matters - the more No-Go stimuli there are, the easier it is to inhibit (fewer Go stimuli = less automaticity of pressing). Results are only comparable with the same Go/No-Go ratio.",
        ],
        "tasks": [
            "What is the FA rate? Calculate: (number of FAs) / (number of No-Go trials) x 100%. Does it fall within the 5-15% norm?",
            "Does the FA rate increase in later blocks? If so - by how much? What does this say about inhibition under cognitive fatigue?",
            "Compare RT on Go trials with results from RT Lab (Lesson 02). Did adding the inhibition task (No-Go) change reaction time to Go stimuli?",
        ],
    },
}

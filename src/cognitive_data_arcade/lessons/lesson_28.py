"""Lesson 28 - Misinformation Spread (SIR misinformation in social networks)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Dezinformacja rozchodzi się w sieciach społecznych jak epidemia biologiczna. "
            "Model SIR (S=podatny, I=zarażony, R=odporny) dobrze opisuje oba procesy. "
            "Każdy zarażony węzeł infekuje sąsiadów z prawdop. p_infect i sam 'ozdrowieje' "
            "(przestaje aktywnie siać) z prawdop. p_recover.",
            "Huby (węzły o bardzo wysokim stopniu) są kluczowymi wzmacniaczami. "
            "Gdy hub jest patient-zero, dezinformacja dociera do niemal wszystkich węzłów "
            "w ciągu kilku kroków SIR - zanim fact-checker zdąży zareagować. "
            "To tłumaczy, dlaczego wielcy influencerzy są tak niebezpieczni jako źródło fake-newsów.",
            "Asymetria spreader vs fact-checker wynika z dwóch efektów: "
            "spreader działa ekspansywnie (każdy zarażony tworzy nowych zarażonych), "
            "a fact-checker działa zastępczo (jeden klik leczy tylko jeden węzeł, "
            "a SIR nie zatrzymuje się). "
            "W sieci bezskalowej asymetria jest dramatycznie większa niż w sieci losowej.",
            "Interwencje platformowe targetują huby: weryfikacja kont z dużym zasięgiem, "
            "obniżone algorytmiczne wzmocnienie, szybsze moderowanie. "
            "Alternatywa - prebunking (szczepienie kognitywne) - uodparnia użytkowników "
            "zanim zetkną się z dezinformacją, co odpowiada szczepieniu huba przed epidemią.",
        ],
        "notes": [
            "Vosoughi i in. 2018 (Science): fałszywe newsy rozchodzą się na Twitterze "
            "6x szybciej i dalej niż prawdziwe - ludzie chętniej udostępniają novelty. "
            "To efekt społeczny, nie algorytmiczny.",
            "Prebunking (teoria inokulacji) jest skuteczniejszy niż debunking post-factum: "
            "wyjaśnienie, jak działa manipulacja, zwiększa odporność kognitywną. "
            "Taktyki prebunkingu: pokazywanie przykładów manipulacyjnych nagłówków, "
            "uwydatnianie bot-patterns, ćwiczenia z rozpoznawania dezinformacji.",
        ],
        "tasks": [
            "Porównaj swoje wyniki ze Spreadera w rundzie 1 (sieć losowa) "
            "i rundzie 3 (sieć bezskalowa). "
            "Dlaczego asymetria spreader/fact-checker rośnie razem z 'bezskalowością'?",
            "Pomyśl o realnym przykładzie moderowania huba: "
            "usuwanie kont influencerów, ograniczanie zasięgu postów, "
            "etykiety fact-checkowe na treściach o dużym zasięgu. "
            "Co mówiłyby dane o efektywności każdej z tych metod?",
            "Policz, ile kliknięć potrzebował Spreader, a ile Fact-Checker, "
            "żeby osiągnąć swój cel w rundzie 3. "
            "Co ta różnica mówi o kosztach zwalczania dezinformacji?",
        ],
    },
    "en": {
        "theory": [
            "Misinformation spreads through social networks like a biological epidemic. "
            "The SIR model (S=susceptible, I=infected, R=recovered) describes both well. "
            "Each infected node infects neighbors with probability p_infect and "
            "recovers (stops actively spreading) with probability p_recover.",
            "Hubs (very high-degree nodes) are key amplifiers. "
            "When a hub is patient-zero, misinformation reaches nearly all nodes "
            "within a few SIR steps - before fact-checkers can react. "
            "This explains why large influencers are so dangerous as fake-news sources.",
            "The spreader vs fact-checker asymmetry has two causes: "
            "spreading is expansive (every infected creates new infected), "
            "while fact-checking is substitutive (one click cures one node, "
            "and SIR keeps running). "
            "In scale-free networks the asymmetry is dramatically larger than in random networks.",
            "Platform interventions target hubs: verification of high-reach accounts, "
            "reduced algorithmic amplification, faster moderation. "
            "Prebunking (cognitive inoculation) immunizes users "
            "before they encounter misinformation - analogous to vaccinating hubs before an epidemic.",
        ],
        "notes": [
            "Vosoughi et al. 2018 (Science): false news spreads 6x faster and further "
            "on Twitter than true news - people prefer to share novelty. "
            "This is a social effect, not an algorithmic one.",
            "Prebunking (inoculation theory) outperforms debunking after the fact: "
            "explaining how manipulation works increases cognitive resistance. "
            "Prebunking tactics: showing examples of manipulative headlines, "
            "highlighting bot patterns, misinformation recognition exercises.",
        ],
        "tasks": [
            "Compare your Spreader scores in round 1 (random network) "
            "and round 3 (scale-free network). "
            "Why does the spreader/fact-checker asymmetry grow with scale-freeness?",
            "Think of a real-world hub moderation example: "
            "removing influencer accounts, limiting post reach, "
            "fact-check labels on high-reach content. "
            "What would data say about the effectiveness of each method?",
            "Count how many clicks Spreader vs Fact-Checker needed to reach their goals "
            "in round 3. "
            "What does that difference say about the cost of combating misinformation?",
        ],
    },
}

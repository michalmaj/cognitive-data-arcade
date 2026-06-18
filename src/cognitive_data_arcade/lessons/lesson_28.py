"""Lesson 28 -- Misinformation Spread (SIR misinformation in social networks)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Dezinformacja rozchodzi sie w sieciach spolecznych jak epidemia biologiczna. "
            "Model SIR (S=podatny, I=zarazony, R=odporny) dobrze opisuje oba procesy. "
            "Kazdy zarazony wezel infekuje sasiadow z prawdop. p_infect i sam 'ozdrowieje' "
            "(przestaje aktywnie siac) z prawdop. p_recover.",
            "Huby (wezly o bardzo wysokim stopniu) sa kluczowymi wzmacniaczami. "
            "Gdy hub jest patient-zero, dezinformacja dociera do niemal wszystkich wezlow "
            "w ciagu kilku krokow SIR -- zanim fact-checker zdazy zareagowac. "
            "To tlumaczy, dlaczego wielcy influencerzy sa tak niebezpieczni jako zrodlo fake-newsow.",
            "Asymetria spreader vs fact-checker wynika z dwoch efektow: "
            "spreader dziala ekspansywnie (kazdy zarazony tworzy nowych zarazonych), "
            "a fact-checker dziala zastepujaco (jeden klik leczy tylko jeden wezel, "
            "a SIR nie zatrzymuje sie). "
            "W sieci bezskalowej asymetria jest dramatycznie wieksza niz w sieci losowej.",
            "Interwencje platformowe targetuja huby: weryfikacja kont z duzym zasiegiem, "
            "obnizone algorytmiczne wzmocnienie, szybsze moderowanie. "
            "Alternatywa -- prebunking (szczepienie kognitywne) -- uodparnia uzytkownikow "
            "zanim zetkna sie z dezinformacja, co odpowiada szczepieniu huba przed epidemia.",
        ],
        "notes": [
            "Vosoughi i in. 2018 (Science): falszywe newsy rozchodza sie na Twitterze "
            "6x szybciej i dalej niz prawdziwe -- ludzie chetniej udostepniaja novelty. "
            "To efekt spoleczny, nie algorytmiczny.",
            "Prebunking (teoria inokulacji) jest skuteczniejszy niz debunking post-factum: "
            "wyjasnienie, jak dziala manipulacja, zwieksza odpornosc kognitywna. "
            "Taktyki prebunkingu: pokazywanie przykladow manipulacyjnych naglowkow, "
            "uwydatnianie bot-patterns, cwiczenia z rozpoznawania dezinformacji.",
        ],
        "tasks": [
            "Porownaj swoje wyniki ze Spreadera w rundzie 1 (siec losowa) "
            "i rundzie 3 (siec bezskalowa). "
            "Dlaczego asymetria spreader/fact-checker rosnie razem z 'bezskalowoscia'?",
            "Pomysl o realnym przykladzie moderowania huba: "
            "usuwanie kont influencerow, ograniczanie zasięgu postow, "
            "etykiety fact-checkowe na tresciach o duzym zasiegu. "
            "Co mowilyby dane o efektywnosci kazdej z tych metod?",
            "Policz, ile klikniec potrzebal Spreader, a ile Fact-Checker, "
            "zeby osiagnac swoj cel w rundzie 3. "
            "Co ta roznica mowi o kosztach zwalczania dezinformacji?",
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
            "within a few SIR steps -- before fact-checkers can react. "
            "This explains why large influencers are so dangerous as fake-news sources.",
            "The spreader vs fact-checker asymmetry has two causes: "
            "spreading is expansive (every infected creates new infected), "
            "while fact-checking is substitutive (one click cures one node, "
            "and SIR keeps running). "
            "In scale-free networks the asymmetry is dramatically larger than in random networks.",
            "Platform interventions target hubs: verification of high-reach accounts, "
            "reduced algorithmic amplification, faster moderation. "
            "Prebunking (cognitive inoculation) immunizes users "
            "before they encounter misinformation -- analogous to vaccinating hubs before an epidemic.",
        ],
        "notes": [
            "Vosoughi et al. 2018 (Science): false news spreads 6x faster and further "
            "on Twitter than true news -- people prefer to share novelty. "
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

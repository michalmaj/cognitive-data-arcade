"""Lesson 30 -- Bias Blind Spot (algorithmic bias and fairness impossibility)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Bias algorytmiczny to nie błąd programisty -- to historia zakodowana w danych. "
            "Algorytm kredytowy uczy się na historycznych decyzjach banków, które przez "
            "dziesięciolecia odmawiały kredytów mieszkańcom konkretnych dzielnic (redlining). "
            "Nawet bez atrybutu 'rasa' model odtwarza te wzorce, bo uczy się z danych "
            "które same są skutkiem dyskryminacji.",
            "Proxy features to cechy, które nie są chronionym atrybutem, ale silnie "
            "korelują z przynależnością do grupy chronionej. Przykład: kod pocztowy "
            "koreluje z rasą ze względu na historyczne praktyki segregacji mieszkaniowej. "
            "Usunięcie atrybutu 'rasa' z modelu nie usuwa dyskryminacji, bo 'kod pocztowy' "
            "niesie tę samą informację (r=0.71). Wskaźnik zadłużenia jest kolejnym proxy (r=0.41) -- "
            "bo historycznie mniejszości miały większe trudności z budowaniem historii kredytowej.",
            "Trade-off bias vs dokładność: usunięcie proxy features zmniejsza bias, "
            "ale również zmniejsza zdolność modelu do rozróżniania ryzyka. "
            "Usunięcie kodu pocztowego obniży bias z 33pp do 21pp, ale dokładność spadnie "
            "z 79% do 76%. Usunięcie kolejnych proxy może obniżyć bias do 9pp, "
            "ale dokładność może spaść do 58%. To nie jest błąd implementacji -- "
            "to matematyczny kompromis wynikający z korelacji cech z wynikiem.",
            "Twierdzenie niemożliwości sprawiedliwości (Chouldechova 2017, Kleinberg 2016): "
            "gdy bazowe wskaźniki są różne w dwóch grupach (tj. jedna grupa ma historycznie "
            "gorsze wyniki), nie istnieje algorytm, który jednocześnie spełnia: "
            "(1) parytet demograficzny -- równe wskaźniki zatwierdzenia, "
            "(2) równe szanse -- równy wskaźnik fałszywie odrzuconych (FPR), "
            "(3) kalibrację -- jeśli model mówi 70%, faktycznie 70% spłaci kredyt. "
            "Spełnienie jednego kryterium matematycznie wyklucza pozostałe dwa. "
            "Ta decyzja jest polityczna, nie techniczna.",
        ],
        "notes": [
            "COMPAS (USA): algorytm do oceny ryzyka recydywizmu używany w sądach. "
            "Badanie ProPublica (2016) wykazało, że fałszywie klasyfikuje czarnych "
            "pozwanych jako wysokie ryzyko 2x częściej niż białych. "
            "Northpointe (twórca COMPAS) odpowiedział, że model jest skalibrowany -- "
            "jeśli model mówi 70%, 70% recydywuje, niezależnie od rasy. "
            "Obaj mieli rację: to jest przykład twierdzenia niemożliwości w praktyce. "
            "Przy różnych bazowych wskaźnikach recydywizmu, kalibracja i równy FPR "
            "są niemożliwe do jednoczesnego spełnienia.",
            "EU AI Act (2024): algorytmy do oceny kredytowej należą do kategorii wysokiego "
            "ryzyka (Annex III, pkt 5b). Wymagania: dokumentacja techniczna, ocena ryzyka, "
            "logging, nadzór ludzki i prawo do wyjaśnienia dla osoby, która dostała odmowę. "
            "Ustawa nie narzuca konkretnego kryterium sprawiedliwości -- pozostawia to "
            "dostawcy. To sprawia, że 'compliance' nie rozwiązuje problemu politycznego wyboru "
            "między metrykami sprawiedliwości.",
        ],
        "tasks": [
            "W grze usunąłeś kod pocztowy i wskaźnik długu, a mimo to bias nie zniknął "
            "całkowicie. Jakie inne cechy mogłyby być proxy features w danych "
            "o kredytach? Wymień dwie i uzasadnij, dlaczego mogłyby korelować "
            "z przynależnością do grupy chronionej.",
            "W Akcie 3 wybierałeś kryterium sprawiedliwości. Które z trzech kryteriów "
            "(parytet demograficzny, równe szanse, kalibracja) wybrałby bank? "
            "Rzecznik równości? Osoba składająca wniosek kredytowy z grupy mniejszościowej? "
            "Uzasadnij każdy wybór z perspektywy interesu danego aktora.",
            "Znajdź jeden realny przykład algorytmu używanego w decyzjach o wpływie "
            "na życie ludzi (kredyty, rekrutacja, sądy, służba zdrowia), w którym "
            "pojawiły się oskarżenia o bias. Które kryterium sprawiedliwości było "
            "naruszone? Czy problem wynikał z proxy features czy z historycznych danych?",
        ],
    },
    "en": {
        "theory": [
            "Algorithmic bias is not a programmer error -- it is history encoded in data. "
            "A credit algorithm learns from historical bank decisions that for decades denied "
            "loans to residents of specific neighborhoods (redlining). "
            "Even without a 'race' attribute, the model reproduces these patterns because it "
            "learns from data that is itself the product of discrimination.",
            "Proxy features are attributes that are not themselves protected, but strongly "
            "correlate with protected group membership. Example: zip code correlates with race "
            "due to historical residential segregation. Removing 'race' from the model does not "
            "remove discrimination, because 'zip code' carries the same information (r=0.71). "
            "Debt ratio is another proxy (r=0.41) -- because historically minorities had more "
            "difficulty building credit history.",
            "Bias vs accuracy trade-off: removing proxy features reduces bias but also reduces "
            "the model's ability to distinguish risk. Removing zip code lowers bias from 33pp "
            "to 21pp, but accuracy falls from 79% to 76%. Removing further proxies may lower "
            "bias to 9pp, but accuracy may fall to 58%. This is not an implementation error -- "
            "it is a mathematical trade-off arising from features correlating with outcome.",
            "Fairness impossibility theorem (Chouldechova 2017, Kleinberg 2016): when base rates "
            "differ between two groups (i.e., one group has historically worse outcomes), no "
            "algorithm can simultaneously satisfy: "
            "(1) demographic parity -- equal approval rates, "
            "(2) equal opportunity -- equal false positive rate (FPR), "
            "(3) calibration -- if model says 70%, actually 70% will repay. "
            "Satisfying one criterion mathematically excludes the other two. "
            "This decision is political, not technical.",
        ],
        "notes": [
            "COMPAS (USA): a recidivism risk scoring algorithm used in courts. "
            "A ProPublica study (2016) found it falsely classifies Black defendants as high risk "
            "2x more often than white defendants. Northpointe (COMPAS creator) responded that "
            "the model is calibrated -- if it says 70%, 70% actually recidivate, regardless of race. "
            "Both were correct: this is an example of the impossibility theorem in practice. "
            "With different base recidivism rates, calibration and equal FPR cannot both be met.",
            "EU AI Act (2024): credit scoring algorithms belong to the high-risk category "
            "(Annex III, point 5b). Requirements: technical documentation, risk assessment, "
            "logging, human oversight, and right to explanation for anyone who receives a denial. "
            "The law does not impose a specific fairness criterion -- it leaves that to the provider. "
            "This means 'compliance' does not resolve the political choice between fairness metrics.",
        ],
        "tasks": [
            "In the game you removed zip code and debt ratio, yet bias did not disappear completely. "
            "What other features could be proxy features in credit data? "
            "Name two and explain why they might correlate with protected group membership.",
            "In Act 3 you chose a fairness criterion. Which of the three criteria "
            "(demographic parity, equal opportunity, calibration) would a bank choose? "
            "An equality advocate? A minority group loan applicant? "
            "Justify each choice from the perspective of each actor's interests.",
            "Find one real-world example of an algorithm used in life-affecting decisions "
            "(credit, hiring, courts, healthcare) where bias allegations arose. "
            "Which fairness criterion was violated? Did the problem stem from proxy features "
            "or historical data?",
        ],
    },
}

"""Lesson 30 - Bias Blind Spot (algorithmic bias and fairness impossibility)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Bias algorytmiczny to nie błąd programisty - to historia zakodowana w danych. Algorytm kredytowy uczy się na historycznych decyzjach banków, które przez dziesięciolecia odmawiały kredytów mieszkańcom konkretnych dzielnic (redlining). Termin pochodzi od HOLC (Home Owners' Loan Corporation, 1933-1954), która kolorowała mapy dzielnic na czerwono - odmowy kredytów w tych strefach trwały przez pokolenia. Nawet bez atrybutu 'rasa' model odtwarza te wzorce, bo uczy się z danych, które same są skutkiem dyskryminacji.",
            "Proxy features to cechy, które nie są chronionym atrybutem, ale silnie korelują z przynależnością do grupy chronionej. Przykład: kod pocztowy koreluje z rasą ze względu na historyczne praktyki segregacji mieszkaniowej. Usunięcie atrybutu 'rasa' z modelu nie usuwa dyskryminacji, bo 'kod pocztowy' niesie tę samą informację (r=0.71). Joy Buolamwini (MIT, Gender Shades 2018) pokazała, że komercyjne systemy rozpoznawania twarzy popełniały błędy o 34.7 pp częściej dla ciemnoskórych kobiet niż dla jasnoskórych mężczyzn - żadna z firm nie używała płci ani rasy jako cech modelu, a mimo to bias był systemowy.",
            "Trade-off bias vs dokładność: usunięcie proxy features zmniejsza bias, ale również zmniejsza zdolność modelu do rozróżniania ryzyka. Usunięcie kodu pocztowego obniża bias z 33pp do 21pp, ale dokładność spada z 79% do 76%. Usunięcie kolejnych proxy może obniżyć bias do 9pp, ale dokładność może spaść do 58%. To nie jest błąd implementacji - to matematyczny kompromis wynikający z korelacji cech z wynikiem.",
            "Twierdzenie niemożliwości sprawiedliwości (Chouldechova 2017, Kleinberg i in. 2016): gdy bazowe wskaźniki są różne w dwóch grupach (tj. jedna grupa ma historycznie gorsze wyniki), nie istnieje algorytm, który jednocześnie spełnia: (1) parytet demograficzny - równe wskaźniki zatwierdzenia, (2) równe szanse - równy wskaźnik fałszywie negatywni (FNR), (3) kalibrację - jeśli model mówi 70%, faktycznie 70% spłaci kredyt. Spełnienie jednego kryterium matematycznie wyklucza pozostałe dwa. Oba artykuły ukazały się niezależnie w tym samym roku - to klasyczny przykład równoczesnego odkrycia.",
            "COMPAS (Correctional Offender Management Profiling for Alternative Sanctions) - algorytm oceny ryzyka recydywizmu używany w ponad 400 sądach w USA. Badanie ProPublica (Angwin i in., 2016) wykazało, że fałszywie klasyfikuje czarnych oskarżonych jako wysokie ryzyko 2x częściej niż białych. Northpointe (twórca COMPAS) odpowiedział, że model jest skalibrowany. Obaj mieli rację: to jest przykład twierdzenia niemożliwości w praktyce - przy różnych bazowych wskaźnikach recydywizmu, kalibracja i równy FPR są niemożliwe do jednoczesnego spełnienia.",
            "EU AI Act (2024): algorytmy do oceny kredytowej należą do kategorii wysokiego ryzyka (Annex III, pkt 5b). Wymagania: dokumentacja techniczna, ocena ryzyka, logging, nadzór ludzki i prawo do wyjaśnienia dla osoby, która dostała odmowę. Ustawa nie narzuca konkretnego kryterium sprawiedliwości - pozostawia to dostawcy. To sprawia, że 'compliance' nie rozwiązuje problemu politycznego wyboru między metrykami sprawiedliwości.",
        ],
        "notes": [
            "Amazon (2015-2018) używała wewnętrznego algorytmu rekrutacyjnego opartego na 10-letniej historii zatrudnień. Model nauczył się penalizować CV zawierające słowo 'kobiece' i nazwy uczelni żeńskich - bo historycznie rekrutowano głównie mężczyzn. Amazon wycofał algorytm w 2018 roku po tym jak problem ujawniła Reuters. To przykład, jak historyczne dane mogą zakodować przeszłą dyskryminację w przyszłych decyzjach.",
            "Fairness przez grupy: bias mierzony na poziomie grup może ukrywać bias na poziomie podgrup (subgroup fairness). Model może być 'sprawiedliwy' dla kobiet i dla osób ciemnoskórych oddzielnie, ale znacznie gorzej działać dla ciemnoskórych kobiet - to tzw. intersectionality w kontekście ML. Kearns i in. (2018) wprowadzili pojęcie 'rich subgroup fairness' dla audytu na wszystkich możliwych podgrupach.",
        ],
        "tasks": [
            "Po usunięciu kodu pocztowego i wskaźnika długu bias nie zniknął całkowicie. Jakie inne cechy mogłyby być proxy features w danych o kredytach? Wymień dwie i uzasadnij, dlaczego mogłyby korelować z przynależnością do grupy chronionej.",
            "W Akcie 3 dostępne są trzy kryteria sprawiedliwości. Które z trzech (parytet demograficzny, równe szanse, kalibracja) wybrałby bank? Rzecznik równości? Osoba składająca wniosek kredytowy z grupy mniejszościowej? Uzasadnij każdy wybór z perspektywy interesu danego aktora.",
            "Znajdź jeden realny przykład algorytmu użytego w decyzjach o wpływie na życie ludzi (kredyty, rekrutacja, sądy, służba zdrowia), w którym pojawiły się oskarżenia o bias. Które kryterium sprawiedliwości było naruszone? Czy problem wynikał z proxy features czy z historycznych danych?",
        ],
    },
    "en": {
        "theory": [
            "Algorithmic bias is not a programmer error - it is history encoded in data. A credit algorithm learns from historical bank decisions that for decades denied loans to residents of specific neighborhoods (redlining). The term comes from the HOLC (Home Owners' Loan Corporation, 1933-1954), which color-coded neighborhood maps in red - loan denials in those zones persisted for generations. Even without a 'race' attribute, the model reproduces these patterns because it learns from data that is itself the product of discrimination.",
            "Proxy features are attributes that are not themselves protected but strongly correlate with protected group membership. Example: zip code correlates with race due to historical residential segregation. Removing 'race' from the model does not remove discrimination, because 'zip code' carries the same information (r=0.71). Joy Buolamwini (MIT, Gender Shades 2018) showed that commercial face recognition systems made errors 34.7 pp more often for dark-skinned women than for light-skinned men - none of the companies used gender or race as model features, yet the bias was systemic.",
            "Bias vs accuracy trade-off: removing proxy features reduces bias but also reduces the model's ability to distinguish risk. Removing zip code lowers bias from 33pp to 21pp, but accuracy falls from 79% to 76%. Removing further proxies may lower bias to 9pp, but accuracy may fall to 58%. This is not an implementation error - it is a mathematical trade-off arising from features correlating with outcome.",
            "Fairness impossibility theorem (Chouldechova 2017, Kleinberg et al. 2016): when base rates differ between two groups (i.e., one group has historically worse outcomes), no algorithm can simultaneously satisfy: (1) demographic parity - equal approval rates, (2) equal opportunity - equal false negative rate (FNR), (3) calibration - if the model says 70%, actually 70% will repay. Satisfying one criterion mathematically excludes the other two. Both papers appeared independently in the same year - a classic simultaneous discovery.",
            "COMPAS (Correctional Offender Management Profiling for Alternative Sanctions) - a recidivism risk scoring algorithm used in over 400 US courts. A ProPublica study (Angwin et al., 2016) found it falsely classifies Black defendants as high risk 2x more often than white defendants. Northpointe (COMPAS creator) responded that the model is calibrated. Both were correct: this is the impossibility theorem in practice - with different base recidivism rates, calibration and equal FPR cannot both be satisfied.",
            "EU AI Act (2024): credit scoring algorithms belong to the high-risk category (Annex III, point 5b). Requirements: technical documentation, risk assessment, logging, human oversight, and right to explanation for anyone who receives a denial. The law does not impose a specific fairness criterion - it leaves that to the provider. This means 'compliance' does not resolve the political choice between fairness metrics.",
        ],
        "notes": [
            "Amazon (2015-2018) used an internal recruitment algorithm trained on 10 years of hiring history. The model learned to penalize CVs containing the word 'women's' and names of women's colleges - because historically mostly men had been hired. Amazon withdrew the algorithm in 2018 after Reuters broke the story. This illustrates how historical data can encode past discrimination into future decisions.",
            "Group fairness can hide subgroup bias. A model may be 'fair' for women and for dark-skinned people separately, but perform much worse for dark-skinned women - this is intersectionality in ML. Kearns et al. (2018) introduced 'rich subgroup fairness' for auditing across all possible subgroups defined by combinations of attributes.",
        ],
        "tasks": [
            "After removing zip code and debt ratio, bias did not disappear completely. What other features could be proxy features in credit data? Name two and explain why they might correlate with protected group membership.",
            "In Act 3 three fairness criteria are available. Which of the three (demographic parity, equal opportunity, calibration) would a bank choose? An equality advocate? A minority group loan applicant? Justify each choice from the perspective of each actor's interests.",
            "Find one real-world example of an algorithm used in life-affecting decisions (credit, hiring, courts, healthcare) where bias allegations arose. Which fairness criterion was violated? Did the problem stem from proxy features or historical data?",
        ],
    },
}

REFLECTION = {
    "pl": {
        "title": "Bias Blind Spot — Refleksja",
        "cards": [
            {
                "label": "Proxy features",
                "color": "indigo",
                "text": "Kod pocztowy koreluje z rasą (r=0.71) ze względu na historyczny redlining (HOLC 1933-54). Usunięcie atrybutu chronionego nie usuwa dyskryminacji. Buolamwini (2018): 34.7 pp więcej błędów dla ciemnoskórych kobiet.",
            },
            {
                "label": "Twierdzenie niemożliwości",
                "color": "orange",
                "text": "Chouldechova (2017) i Kleinberg (2016): gdy grupy mają różne rozkłady bazowe, parytet demograficzny, równe szanse i kalibracja są wzajemnie sprzeczne. Wybór kryterium to decyzja polityczna, nie techniczna.",
            },
            {
                "label": "COMPAS",
                "color": "green",
                "text": "ProPublica (2016): algorytm sądowy klasyfikował czarnych oskarżonych jako 'wysokie ryzyko' 2× częściej (45% vs 24% false positives). Northpointe: kalibracja równa między grupami. Obaj mieli rację — twierdzenie niemożliwości w praktyce.",
            },
        ],
        "question": "Model kredytowy: 79% dokładności, 33 pp dysproporcji odmów. Usunięcie kodu pocztowego: dysproporcja 9 pp, accuracy 58%. Jakie kryterium sprawiedliwości wybierzesz i jak uzasadnisz tę decyzję?",
    },
    "en": {
        "title": "Bias Blind Spot — Reflection",
        "cards": [
            {
                "label": "Proxy features",
                "color": "indigo",
                "text": "Postcode correlates with race (r=0.71) due to historical redlining (HOLC 1933–54). Removing the protected attribute does not remove discrimination. Buolamwini (2018): 34.7 pp more errors for dark-skinned women.",
            },
            {
                "label": "Impossibility theorem",
                "color": "orange",
                "text": "Chouldechova (2017) and Kleinberg (2016): when groups have different base rates, demographic parity, equal opportunity, and calibration are mutually exclusive. The choice of criterion is a political, not a technical, decision.",
            },
            {
                "label": "COMPAS",
                "color": "green",
                "text": "ProPublica (2016): the court algorithm classified Black defendants as 'high risk' 2× more often (45% vs 24% false positives). Northpointe: calibration equal between groups. Both were mathematically correct — the impossibility theorem in practice.",
            },
        ],
        "question": "Credit model: 79% accuracy, 33 pp disparity in rejections. Removing postcode: 9 pp disparity, 58% accuracy. Which fairness criterion do you choose and how do you justify that decision?",
    },
}

"""Lesson 32 - The Architect's Trial (AI ethics and algorithmic decision-making)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Algorytmiczne podejmowanie decyzji (ADM) pojawia się w sytuacjach, gdy system AI zastępuje lub wspiera człowieka w decyzjach o wysokich stawkach: kto dostanie kredyt, kto trafi do więzienia, kto zostanie zatrudniony. EU AI Act (uchwalony kwiecień 2024, wdrożenie fazowe 2024-2027) definiuje 'systemy wysokiego ryzyka' i nakłada na nie obowiązek dokumentacji, audytu i nadzoru ludzkiego.",
            "Matematyczna niemożliwość: nie można jednocześnie spełnić trzech najpopularniejszych definicji sprawiedliwości algorytmicznej. Parytet demograficzny (równe wskaźniki aprobaty między grupami), równe szanse (równe TPR między grupami) i kalibracja (równe prawdopodobieństwa predykcyjne) są wzajemnie sprzeczne gdy grupy mają różne rozkłady bazowe. Chouldechova (2017) i Kleinberg i in. (2016) udowodnili tę niemożliwość niezależnie - klasyczny przykład równoczesnego odkrycia. Wybór kryterium to decyzja polityczna, nie techniczna.",
            "EU AI Act klasyfikuje systemy AI według ryzyka. Systemy 'wysokiego ryzyka' (rekrutacja, edukacja, opieka społeczna, wymiar sprawiedliwości) muszą mieć: dokumentację techniczną, rejestr zdarzeń, mechanizm nadzoru ludzkiego, przejrzyste informowanie osób, których dotyczą decyzje. Brak compliance może skutkować karą do 30 mln EUR lub 6% obrotu. W USA analog to NIST AI Risk Management Framework (2023) - dobrowolny, ale referowany w umowach rządowych.",
            "Efekt Goodharta: 'Kiedy miara staje się celem, przestaje być dobrą miarą' (Charles Goodhart, Bank of Anglii, 1975, oryginalnie o polityce monetarnej). Marilyn Strathern uogólniła w 1997: 'Każda obserwowana regularność statystyczna, na której się polega, ulega rozpadowi, gdy się na niej wywiera naciski regulacyjne'. Klasyczne przykłady w AI: system rekrutacyjny optymalizowany pod retencję zaczyna odrzucać kandydatów ze złożonym życiorysem; algorytm rekomendacji optymalizowany pod engagement maksymalizuje outrage, bo outrage trzyma użytkowników dłużej.",
            "Cathy O'Neil 'Weapons of Math Destruction' (2016): autorka, matematyczka i była analityczka hedge-fund, opisuje jak pozornie neutralne modele matematyczne wzmacniają nierówności społeczne. Trzy cechy 'broni': nieprzejrzystość (black box), skala (miliony decyzji), destrukcyjność (dotykają najbardziej wrażliwe grupy). Przykładem jest Value-Added Model (VAM) do oceny nauczycieli: użyty w USA w 2011, prowadził do zwolnień na podstawie wyników, które zmieniły się o 20-30 pp z roku na rok - przy tych samych nauczycielach. Sąd w Nowym Jorku orzekł w 2015, że wyniki nie mogą być używane jako podstawa zwolnień.",
        ],
        "notes": [
            "COMPAS (Correctional Offender Management Profiling for Alternative Sanctions) - algorytm używany w ponad 400 sądach w USA do oceny ryzyka recydywizmu. ProPublica (Angwin i in., 2016) wykazała: algorytm fałszywie klasyfikuje czarnych oskarżonych jako 'wysokie ryzyko' dwukrotnie częściej niż białych (45% vs 24% false positives). Northpointe odpowiedział: accuracy jest równa między grupami. Obaj mieli rację matematyczną - to właśnie twierdzenie niemożliwości w praktyce.",
            "Zasada ELSI (Ethical, Legal, Social Implications) - sformalizowana przy projekcie genomu ludzkiego (NIH, 1990). 3-5% budżetu projektu przeznaczono na badania ELSI - pierwsza instytucjonalizacja etyki technologicznej w nauce. Dzięki ELSI zidentyfikowano zagrożenia prywatności danych genetycznych, patentowania genów i kwestie równości dostępu do terapii genowych jeszcze przed opublikowaniem genomu w 2003.",
        ],
        "tasks": [
            "Który wybór projektowy z gry najbardziej zaskakuje konsekwencjami? Na jakich przesłankach - co wydawało się oczywiste lub bezpieczne przy podejmowaniu tej decyzji?",
            "W scenariuszu z systemem ADM: osoba z grupy demograficznej, która 'przegrała' na ocenianym systemie, nie zna ani cech modelu, ani kryteriów decyzji. Co to oznacza dla prawa do odwołania? Czy wymóg 'prawa do wyjaśnienia' z EU AI Act wystarczyłoby do naprawienia tej asymetrii?",
            "Czy istnieje kombinacja decyzji projektowych, która zaspokaja jednocześnie wszystkich trzech sędziów komisji? Co wynika z dodatkowej rozgrywki o naturze kompromisów w projektowaniu systemów AI?",
        ],
    },
    "en": {
        "theory": [
            "Algorithmic Decision Making (ADM) arises when an AI system replaces or assists humans in high-stakes decisions: who gets credit, who goes to prison, who gets hired. The EU AI Act (passed April 2024, phased implementation 2024-2027) defines 'high-risk systems' and imposes documentation, auditing, and human oversight requirements on them.",
            "Mathematical impossibility: it is impossible to simultaneously satisfy the three most popular definitions of algorithmic fairness. Demographic parity (equal approval rates across groups), equal opportunity (equal TPR across groups), and calibration (equal predictive probabilities) are mutually exclusive when groups have different base rates. Chouldechova (2017) and Kleinberg et al. (2016) proved this impossibility independently - a classic simultaneous discovery. Choosing a criterion is a political, not technical, decision.",
            "The EU AI Act classifies AI systems by risk. 'High-risk' systems (recruitment, education, social services, justice) must have: technical documentation, event logs, human oversight, and transparent notification of affected individuals. Non-compliance can result in fines up to EUR 30 million or 6% of turnover. In the US, the analog is the NIST AI Risk Management Framework (2023) - voluntary, but referenced in government contracts.",
            "Goodhart's Law: 'When a measure becomes a target, it ceases to be a good measure' (Charles Goodhart, Bank of England, 1975, originally about monetary policy). Marilyn Strathern generalized in 1997: 'Any observed statistical regularity will tend to collapse once pressure is placed upon it for control purposes'. Classic AI examples: a recruitment system optimized for retention starts rejecting candidates with complex CVs; a recommendation algorithm optimized for engagement maximizes outrage because outrage keeps users on the platform longer.",
            "Cathy O'Neil 'Weapons of Math Destruction' (2016): the author, a mathematician and former hedge-fund analyst, describes how seemingly neutral mathematical models amplify social inequalities. Three features of 'weapons': opacity (black box), scale (millions of decisions), destructiveness (disproportionately affecting vulnerable groups). The Value-Added Model (VAM) for teacher evaluation used in the US in 2011 led to dismissals based on scores that shifted 20-30 pp year-on-year for the same teachers. A New York court ruled in 2015 that scores could not be used as the basis for dismissal.",
        ],
        "notes": [
            "COMPAS (Correctional Offender Management Profiling for Alternative Sanctions) - used in over 400 US courts for recidivism risk assessment. ProPublica (Angwin et al., 2016) showed: the algorithm misclassifies Black defendants as 'high risk' twice as often as white defendants (45% vs 24% false positives). Northpointe responded: accuracy is equal across groups. Both claims are mathematically true - this is precisely the impossibility theorem in practice.",
            "The ELSI principle (Ethical, Legal, Social Implications) was formalized during the Human Genome Project (NIH, 1990). 3-5% of the project budget was allocated to ELSI research - the first institutionalization of technology ethics in science. ELSI identified genetic privacy risks, gene patenting, and equitable access concerns before the genome was published in 2003.",
        ],
        "tasks": [
            "Which design choice in the game is most surprising in its consequences? On what reasoning did that choice seem obvious or safe at the time it was made?",
            "In an ADM scenario: a person from the demographic group that 'lost' under the evaluated system does not know the model's features or decision criteria. What does this mean for the right to appeal? Would the 'right to explanation' requirement in the EU AI Act be sufficient to correct this asymmetry?",
            "Is there a combination of design decisions that satisfies all three committee judges simultaneously? What does an additional playthrough reveal about the nature of tradeoffs in AI system design?",
        ],
    },
}

REFLECTION = {
    "pl": {
        "title": "The Architect's Trial — Refleksja",
        "cards": [
            {
                "label": "EU AI Act",
                "color": "indigo",
                "text": "Maj 2024: systemy 'wysokiego ryzyka' (rekrutacja, edukacja, wymiar sprawiedliwości) wymagają dokumentacji technicznej, logowania, nadzoru ludzkiego i prawa do wyjaśnienia. Kara: do 30M EUR lub 6% obrotu.",
            },
            {
                "label": "Efekt Goodharta",
                "color": "orange",
                "text": "Goodhart (1975): 'kiedy miara staje się celem, przestaje być dobrą miarą'. Algorytm optymalizowany pod engagement maksymalizuje outrage — bo outrage trzyma użytkowników dłużej. Cel mierzalny ≠ cel rzeczywisty.",
            },
            {
                "label": "Weapons of Math Destruction",
                "color": "green",
                "text": "O'Neil (2016): model matematyczny wzmacnia nierówności gdy jest nieprzejrzysty, działa w skali milionów decyzji i dotyka najbardziej wrażliwych grup. Brak mechanizmu odwołania to trzecia cecha 'broni'.",
            },
        ],
        "question": "System rekrutacyjny zaczyna odrzucać kandydatów ze złożonym CV — optymalizuje retencję. Jak odkryjesz ten bias zanim skrzywdzi kandydatów? Jakie mechanizmy nadzoru wbudujesz w system zgodny z EU AI Act?",
    },
    "en": {
        "title": "The Architect's Trial — Reflection",
        "cards": [
            {
                "label": "EU AI Act",
                "color": "indigo",
                "text": "May 2024: 'high-risk' systems (recruitment, education, justice) require technical documentation, logging, human oversight, and the right to an explanation. Penalty: up to EUR 30M or 6% of turnover.",
            },
            {
                "label": "Goodhart's law",
                "color": "orange",
                "text": "Goodhart (1975): 'when a measure becomes a target, it ceases to be a good measure'. An algorithm optimised for engagement maximises outrage — because outrage keeps users engaged longer. Measurable goal ≠ real goal.",
            },
            {
                "label": "Weapons of Math Destruction",
                "color": "green",
                "text": "O'Neil (2016): a mathematical model amplifies inequality when it is opaque, operates at the scale of millions of decisions, and affects the most vulnerable groups. The absence of an appeal mechanism is the third feature of a 'weapon'.",
            },
        ],
        "question": "A recruitment system starts rejecting candidates with complex CVs — it is optimising for retention. How do you detect this bias before it harms candidates? What oversight mechanisms do you build into an EU AI Act high-risk system?",
    },
}

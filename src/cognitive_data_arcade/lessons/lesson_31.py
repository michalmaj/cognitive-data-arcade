# src/cognitive_data_arcade/lessons/lesson_31.py
"""Lesson 31 - You Were the Dataset (behavioural data, observer effect, privacy)."""

from __future__ import annotations

from cognitive_data_arcade.lessons.provenance import Claim

PROVENANCE: dict[str, Claim] = {
    "hawthorne_effect_narrative": Claim(
        type="empirical",
        note=(
            "The standard Hawthorne narrative (output rose whenever conditions changed) "
            "is an oversimplification. Levitt & List (2011, American Economic Journal) "
            "reanalysed the original data and found the effect far weaker than reported. "
            "Content now correctly qualifies this."
        ),
        source="Levitt & List (2011), American Economic Journal: Applied Economics",
        updated="2026-08-18",
    ),
    "reidentification_accuracy": Claim(
        type="empirical",
        note=(
            ">95% re-identification accuracy claims are specific to controlled laboratory "
            "conditions with large reference databases (long-term trace data). "
            "Not a general property of any behavioural dataset. "
            "Content now correctly scopes this claim."
        ),
        source="Kosinski et al. (2013, PNAS); Youyou et al. (2015, PNAS)",
        updated="2026-08-18",
    ),
    "cambridge_analytica_user_count": Claim(
        type="empirical",
        note=(
            "87 million Facebook profiles figure is from Facebook's own disclosure (2018). "
            "Accurate as of that disclosure; treat as a reported figure from the company, "
            "not an independently verified count."
        ),
        updated="2026-08-18",
    ),
    "gdpr_fine_amounts": Claim(
        type="empirical",
        note=(
            "GDPR fine amounts (Meta EUR 1.2B, Amazon EUR 746M) are accurate as of 2023-2024. "
            "Figures may change on appeal; treat as approximate reference values."
        ),
        updated="2026-08-18",
    ),
}

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Dane behawioralne to dane zbierane przez rejestrowanie zachowania, nie deklaracji. Każde naciśnięcie klawisza, każdy czas reakcji, każda odpowiedź w eksperymencie - to dane behawioralne. W tradycyjnej kognitywistyce badacz celowo zbiera te dane od uczestnika. W świecie big data zbierają je aplikacje, platformy i urządzenia - często bez świadomości użytkownika.",
            "Efekt Hawthorne'a: zachowanie zmienia się, gdy wiemy, że jesteśmy obserwowani. Nazwa pochodzi od eksperymentów przemysłowych w zakładach Western Electric Hawthorne Works, Chicago (Mayo, 1924-1932), w których wydajność zdawała się rosnąć za każdym razem, gdy zmieniano warunki pracy. Jednak późniejsza reanaliza oryginalnych danych (Levitt i List, 2011, American Economic Journal) wykazała, że wzorzec był znacznie słabszy niż powszechnie opisywano — standardowa narracja o tym efekcie to uproszczenie. Co badania te rzeczywiście ilustrują, to realne wyzwanie: sama świadomość, że dane są zbierane, może zmieniać badane zachowanie. W tym kursie uczestnicy są informowani o zbieraniu danych przez ekran wprowadzający — jednak nawet wiedza o rejestrowaniu może kształtować zaangażowanie w zadania, co jest centralnym wyzwaniem etyki badań.",
            "Dane behawioralne mogą być zaskakująco identyfikujące. Długoterminowe ślady — dynamika pisania, sekwencje kliknięć, historia przeglądania — mogą osiągać wysoką dokładność re-identyfikacji w kontrolowanych warunkach laboratoryjnych z dużymi bazami referencyjnymi; twierdzenia o >95% dokładności należy odczytywać jako specyficzne dla takich warunków, nie jako ogólną własność każdych danych behawioralnych. Kosiński i in. (2013, PNAS) wykazali, że lajki na Facebooku pozwalają przewidywać cechy osobowości OCEAN ze znaczącą trafnością; Youyou i in. (2015, PNAS) rozwinęli to, pokazując że przy 300 lajkach model przewyższa przewidywania małżonka. Badania te dowodzą, że zagregowane cyfrowe ślady niosą bogatą informację psychologiczną — nie że kilka prób RT z jednej sesji tworzy stabilny odcisk tożsamości.",
            "Cambridge Analytica (2018): firma zebrała dane behawioralne z lajków 87 milionów użytkowników Facebooka bez ich wiedzy i użyła ich do psychograficznego targetowania politycznego podczas wyborów w USA i Brexit. Dane pozyskano przez aplikację GSR (Global Science Research) - użytkownik wyrażał zgodę, ale obejmowała ona również znajomych. Christopher Wylie, sygnalizator wewnętrzny, ujawnił działania firmy w 2018. To przykład, jak dane behawioralne agregowane na skalę miliardów użytkowników mogą wpływać na demokratyczne procesy.",
            "Prywatność danych behawioralnych jest regulowana przez RODO od 2018 roku. Dane o zachowaniu użytkownika (czas reakcji, wzorce kliknięć, historia przeglądania) są danymi osobowymi i wymagają podstawy prawnej do przetwarzania. Wiele platform zbiera je w sposób niejawny jako 'dane analityczne'. Najwyższe kary RODO: Meta 1,2 mld euro (2023, DPC Irlandia - transfer danych do USA), Amazon 746 mln euro (2021). Granica między 'anonimowymi danymi analitycznymi' a danymi osobowymi jest znacznie cieńsza niż większość firm przyznaje.",
        ],
        "notes": [
            "Badanie 'You Are What You Like' (Youyou, Kosiński, Stillwell, PNAS 2015): na podstawie 300 lajków model komputerowy przewidywał cechy osobowości dokładniej niż małżonek osoby badanej. Na podstawie 10 lajków - dokładniej niż współpracownicy. To badanie bezpośrednio zainspirowało model psychograficzny Cambridge Analytica. Kosiński sam nie współpracował z CA - jedynie opublikował metodę, którą inni wykorzystali bez jego wiedzy.",
            "RODO (Ogólne Rozporządzenie o Ochronie Danych, 2018): każde przetwarzanie danych osobowych wymaga podstawy prawnej (zgoda, umowa, uzasadniony interes). Prawo do bycia zapomnianym (art. 17 RODO) pozwala osobom fizycznym żądać usunięcia ich danych, ale RODO przewiduje wyjątki — badania naukowe, interes publiczny, wolność wyrazu, roszczenia prawne — i nie jest to bezwarunkowe prawo do usunięcia wszystkich danych w każdej sytuacji. EU AI Act (2024) nakłada dodatkowe wymogi na systemy AI wysokiego ryzyka w zakresie transparentności i audytowalności.",
        ],
        "tasks": [
            "Na podstawie kognitywnego profilu zebranego w kursie - co jest najbardziej zaskakujące? Czy wyniki zgadzają się z subiektywnym poczuciem własnych zdolności? Co efekt Stroopa mówi o tym, jak mózg przetwarza sprzeczne informacje?",
            "Firma reklamowa ma dostęp do 1000 naciśnięć klawiszy dziennie podczas typowej pracy. Jakie cechy osobowości lub zachowania można z nich wywnioskować? Czy taka wymiana - dane w zamian za bezpłatną aplikację - jest uczciwa?",
            "W tym kursie dane zbierane są lokalnie - tylko na komputerze uczestnika. Jak zmieniłoby się uczestnictwo, gdyby dane trafiły na serwer? A gdyby były anonimowe? A gdyby były publiczne? Gdzie przebiega granica między akceptowalnym a nieakceptowalnym zbieraniem danych?",
        ],
    },
    "en": {
        "theory": [
            "Behavioural data is collected by recording behaviour, not declarations. Every keypress, every reaction time, every response in an experiment - that is behavioural data. In traditional cognitive science a researcher deliberately collects this data from a participant. In the big-data world apps, platforms, and devices collect it - often without the user's awareness.",
            "The Hawthorne effect: behaviour changes when people know they are being observed. The name comes from industrial experiments at Western Electric's Hawthorne Works, Chicago (Mayo, 1924-1932), in which output appeared to rise whenever working conditions changed. However, subsequent reanalysis of the original data (Levitt & List, 2011, American Economic Journal) found the pattern far weaker than commonly claimed — the standard Hawthorne narrative is an oversimplification. What the studies do illustrate is a real challenge: even awareness that data is being collected can alter the behaviour under study. In this course participants are informed about data collection through the onboarding screen — yet the act of being informed may still shape how they engage with the tasks, which is a core challenge in research ethics.",
            "Behavioural data can be unexpectedly identifying. Long-term traces — typing dynamics, mouse-click sequences, browsing history — can reach high re-identification accuracy in controlled laboratory conditions with large reference databases; claims of >95% accuracy should be read as specific to those conditions, not as a general property of any behavioural data. Kosinski et al. (2013, PNAS) showed that Facebook likes predict OCEAN personality traits with meaningful accuracy; Youyou et al. (2015, PNAS) extended this, showing that with 300 likes a model outperforms a spouse's predictions. These studies demonstrate that aggregate digital traces carry rich psychological signal — not that a few RT trials from a single session constitute a stable identity fingerprint.",
            "Cambridge Analytica (2018): the company harvested behavioural data from 87 million Facebook users' likes without their knowledge and used it for psychographic political targeting in the US election and Brexit. Data was obtained through the GSR (Global Science Research) app - users consented but the consent covered their friends too. Whistleblower Christopher Wylie exposed the company's operations in 2018. This is an example of how behavioural data aggregated at billions-user scale can influence democratic processes.",
            "Privacy of behavioural data has been regulated by GDPR since 2018. User behaviour data (reaction time, click patterns, browsing history) is personal data and requires a legal basis for processing. Many platforms collect it covertly as 'analytics data'. Largest GDPR fines: Meta EUR 1.2 billion (2023, Irish DPC - US data transfer), Amazon EUR 746 million (2021). The boundary between 'anonymous analytics' and personal data is much thinner than most companies admit.",
        ],
        "notes": [
            "The study 'You Are What You Like' (Youyou, Kosinski, Stillwell, PNAS 2015): based on 300 likes, a computer model predicted personality traits more accurately than a spouse. Based on 10 likes - more accurately than coworkers. This research directly inspired the Cambridge Analytica psychographic model. Kosinski himself did not work with CA - he merely published the method, which others then applied without his knowledge.",
            "GDPR (General Data Protection Regulation, 2018): every processing of personal data requires a legal basis (consent, contract, legitimate interest). The right to erasure (Article 17) allows individuals to request deletion of their data, but GDPR includes exceptions for scientific research, public interest, freedom of expression, and legal claims — it is not an unconditional right to delete all data in all circumstances. The EU AI Act (2024) adds further transparency and auditability requirements for high-risk AI systems.",
        ],
        "tasks": [
            "Looking at the cognitive profile collected in this course - what is most surprising? Do the results match a subjective sense of one's own abilities? What does the Stroop effect say about how the brain processes conflicting information?",
            "An advertising company has access to 1000 keypresses per day during typical office work. What personality traits or behaviours could be inferred? Is such an exchange - data for a free app - fair?",
            "In this course data is collected locally - only on the participant's computer. How would participation change if data went to a server? What if it were anonymous? What if it were public? Where is the boundary between acceptable and unacceptable data collection?",
        ],
    },
}

REFLECTION = {
    "pl": {
        "title": "You Were the Dataset — Refleksja",
        "cards": [
            {
                "label": "Odcisk poznawczy",
                "color": "indigo",
                "text": "Długoterminowe ślady behawioralne (dynamika pisania, historia przeglądania) mogą osiągać wysoką re-identyfikację w kontrolowanych warunkach z bazami referencyjnymi. Kilka prób RT z jednej sesji jest znacznie mniej identyfikujące. Kosiński i in. (2013, PNAS): lajki na Facebooku przewidują cechy osobowości OCEAN — to twierdzenie o sygnale psychologicznym, nie o rozpoznaniu tożsamości.",
            },
            {
                "label": "Efekt Hawthorne'a",
                "color": "orange",
                "text": "Mayo (1924-1932): zachowanie zmienia się gdy jesteśmy obserwowani — choć oryginalne dowody z badań Hawthorne są słabsze niż powszechnie podawano (Levitt i List, 2011). W tym kursie uczestnicy są informowani o zbieraniu danych; nawet tak wiedza o rejestrowaniu może wpływać na zaangażowanie — to sedno wyzwania etyki badań.",
            },
            {
                "label": "Cambridge Analytica",
                "color": "green",
                "text": "87 milionów profili Facebooka zebrano bez wiedzy użytkowników przez aplikację GSR. Zgoda obejmowała też znajomych. RODO (2018): dane behawioralne (RT, wzorce kliknięć) = dane osobowe wymagające podstawy prawnej.",
            },
        ],
        "question": "Twoje dane RT z tego kursu stanowią ślad behawioralny. Co oznacza 'anonimizacja' w kontekście danych behawioralnych? Kiedy 'anonimowe dane analityczne' stają się danymi osobowymi według RODO?",
    },
    "en": {
        "title": "You Were the Dataset — Reflection",
        "cards": [
            {
                "label": "Cognitive fingerprint",
                "color": "indigo",
                "text": "Long-term behavioural traces (typing dynamics, browsing history) can reach high re-identification accuracy in controlled conditions with reference databases. A few RT trials from one session are far less identifying. Kosinski et al. (2013, PNAS): Facebook likes predict OCEAN personality traits — a claim about psychological signal, not identity recognition.",
            },
            {
                "label": "Hawthorne effect",
                "color": "orange",
                "text": "Mayo (1924-1932): behaviour changes when we know we are observed — though the original Hawthorne evidence is weaker than commonly cited (Levitt & List, 2011). In this course participants are informed about data collection; even so, knowing data is being recorded may influence engagement — that is the core challenge of research ethics.",
            },
            {
                "label": "Cambridge Analytica",
                "color": "green",
                "text": "87 million Facebook profiles were collected without users' knowledge via the GSR app. Consent covered friends too. GDPR (2018): behavioural data (RT, click patterns) = personal data requiring a legal basis.",
            },
        ],
        "question": "Your RT data from this course forms a behavioural trace. What does 'anonymisation' mean for behavioural data? When do 'anonymous analytics data' become personal data under the GDPR?",
    },
}

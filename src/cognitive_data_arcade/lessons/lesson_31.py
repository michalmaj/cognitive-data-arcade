# src/cognitive_data_arcade/lessons/lesson_31.py
"""Lesson 31 - You Were the Dataset (behavioural data, observer effect, privacy)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Dane behawioralne to dane zbierane przez rejestrowanie zachowania, nie deklaracji. Każde naciśnięcie klawisza, każdy czas reakcji, każda odpowiedź w eksperymencie - to dane behawioralne. W tradycyjnej kognitywistyce badacz celowo zbiera te dane od uczestnika. W świecie big data zbierają je aplikacje, platformy i urządzenia - często bez świadomości użytkownika.",
            "Efekt Hawthorne'a: zachowanie zmienia się, gdy wiemy, że jesteśmy obserwowani. Termin pochodzi od eksperymentów Eltona Mayo (1924-1932) w zakładach Western Electric Hawthorne Works koło Chicago - robotnicy pracowali wydajniej za każdym razem, gdy zmieniano warunki oświetlenia, niezależnie od kierunku zmiany. Henry Landsberger skuł termin 'Hawthorne effect' w 1958. W tym kursie uczestnicy nie byli informowani explicite, że każda gra zapisuje dane do pliku CSV - ten paradoks leży u podstaw każdej etyki badań naukowych.",
            "Dane behawioralne są nieoczekiwanie identyfikujące. Efekt Stroopa, czasy reakcji i wzorce błędów razem tworzą unikalny 'odcisk poznawczy'. Badania pokazują, że styl pisania na klawiaturze (typing dynamics), wzorce kliknięć myszy czy czas spędzony na każdym elemencie strony mogą identyfikować osobę z dokładnością przekraczającą 95% - nawet bez żadnych danych osobowych. Michał Kosiński (Cambridge, 2013) pokazał, że 150 lajków na Facebooku pozwala przewidzieć cechy osobowości OCEAN dokładniej niż znajomi, 300 lajków - dokładniej niż partner.",
            "Cambridge Analytica (2018): firma zebrała dane behawioralne z lajków 87 milionów użytkowników Facebooka bez ich wiedzy i użyła ich do psychograficznego targetowania politycznego podczas wyborów w USA i Brexit. Dane pozyskano przez aplikację GSR (Global Science Research) - użytkownik wyrażał zgodę, ale obejmowała ona również znajomych. Christopher Wylie, sygnalizator wewnętrzny, ujawnił działania firmy w 2018. To przykład, jak dane behawioralne agregowane na skalę miliardów użytkowników mogą wpływać na demokratyczne procesy.",
            "Prywatność danych behawioralnych jest regulowana przez RODO od 2018 roku. Dane o zachowaniu użytkownika (czas reakcji, wzorce kliknięć, historia przeglądania) są danymi osobowymi i wymagają podstawy prawnej do przetwarzania. Wiele platform zbiera je w sposób niejawny jako 'dane analityczne'. Najwyższe kary RODO: Meta 1,2 mld euro (2023, DPC Irlandia - transfer danych do USA), Amazon 746 mln euro (2021). Granica między 'anonimowymi danymi analitycznymi' a danymi osobowymi jest znacznie cieńsza niż większość firm przyznaje.",
        ],
        "notes": [
            "Badanie 'You Are What You Like' (Youyou, Kosiński, Stillwell, PNAS 2015): na podstawie 300 lajków model komputerowy przewidywał cechy osobowości dokładniej niż małżonek osoby badanej. Na podstawie 10 lajków - dokładniej niż współpracownicy. To badanie bezpośrednio zainspirowało model psychograficzny Cambridge Analytica. Kosiński sam nie współpracował z CA - jedynie opublikował metodę, którą inni wykorzystali bez jego wiedzy.",
            "RODO (Ogólne Rozporządzenie o Ochronie Danych, 2018): każde przetwarzanie danych osobowych wymaga podstawy prawnej (zgoda, umowa, uzasadniony interes). Prawo do bycia zapomnianym oznacza prawo do żądania usunięcia wszystkich danych. EU AI Act (2024) nakłada dodatkowe wymogi na systemy AI wysokiego ryzyka w zakresie transparentności i audytowalności.",
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
            "The Hawthorne effect: behaviour changes when people know they are being observed. The term comes from experiments by Elton Mayo (1924-1932) at Western Electric's Hawthorne Works near Chicago - workers became more productive every time conditions changed, regardless of the direction of the change. Henry Landsberger coined 'Hawthorne effect' in 1958. In this course participants were not explicitly informed that every game writes data to a CSV file - this paradox underpins all research ethics.",
            "Behavioural data is unexpectedly identifying. The Stroop effect, reaction times, and error patterns together form a unique 'cognitive fingerprint'. Research shows that typing dynamics, mouse-click sequences, or dwell time per page element can identify a person with over 95% accuracy - even with no personal data. Michal Kosinski (Cambridge, 2013) showed that 150 Facebook likes predict OCEAN personality traits more accurately than friends, and 300 likes more accurately than a partner.",
            "Cambridge Analytica (2018): the company harvested behavioural data from 87 million Facebook users' likes without their knowledge and used it for psychographic political targeting in the US election and Brexit. Data was obtained through the GSR (Global Science Research) app - users consented but the consent covered their friends too. Whistleblower Christopher Wylie exposed the company's operations in 2018. This is an example of how behavioural data aggregated at billions-user scale can influence democratic processes.",
            "Privacy of behavioural data has been regulated by GDPR since 2018. User behaviour data (reaction time, click patterns, browsing history) is personal data and requires a legal basis for processing. Many platforms collect it covertly as 'analytics data'. Largest GDPR fines: Meta EUR 1.2 billion (2023, Irish DPC - US data transfer), Amazon EUR 746 million (2021). The boundary between 'anonymous analytics' and personal data is much thinner than most companies admit.",
        ],
        "notes": [
            "The study 'You Are What You Like' (Youyou, Kosinski, Stillwell, PNAS 2015): based on 300 likes, a computer model predicted personality traits more accurately than a spouse. Based on 10 likes - more accurately than coworkers. This research directly inspired the Cambridge Analytica psychographic model. Kosinski himself did not work with CA - he merely published the method, which others then applied without his knowledge.",
            "GDPR (General Data Protection Regulation, 2018): every processing of personal data requires a legal basis (consent, contract, legitimate interest). The right to be forgotten means the right to demand deletion of all data. The EU AI Act (2024) adds further transparency and auditability requirements for high-risk AI systems.",
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
                "text": "Wzorce RT, błędów i stylu pisania mogą identyfikować osobę z dokładnością >95% — bez żadnych danych osobowych. Kosiński (2013): 150 lajków na Facebooku przewiduje osobowość OCEAN dokładniej niż znajomi.",
            },
            {
                "label": "Efekt Hawthorne'a",
                "color": "orange",
                "text": "Mayo (1924-1932): zachowanie zmienia się gdy jesteśmy obserwowani. W tym kursie: uczestnicy nie wiedzieli, że każda gra zapisuje CSV. Paradoks badań — poinformowanie uczestnika zmienia to, co mierzysz.",
            },
            {
                "label": "Cambridge Analytica",
                "color": "green",
                "text": "87 milionów profili Facebooka zebrano bez wiedzy użytkowników przez aplikację GSR. Zgoda obejmowała też znajomych. RODO (2018): dane behawioralne (RT, wzorce kliknięć) = dane osobowe wymagające podstawy prawnej.",
            },
        ],
        "question": "Twoje dane RT z tego kursu mogą cię identyfikować. Co oznacza 'anonimizacja' w kontekście danych behawioralnych? Kiedy 'anonimowe dane analityczne' stają się danymi osobowymi według RODO?",
    },
    "en": {
        "title": "You Were the Dataset — Reflection",
        "cards": [
            {
                "label": "Cognitive fingerprint",
                "color": "indigo",
                "text": "Patterns of RT, errors, and typing style can identify a person with >95% accuracy — with no personal data at all. Kosinski (2013): 150 Facebook likes predict OCEAN personality more accurately than friends.",
            },
            {
                "label": "Hawthorne effect",
                "color": "orange",
                "text": "Mayo (1924–1932): behaviour changes when we know we are observed. In this course: participants did not know every game writes a CSV file. Research paradox — informing the participant changes what you measure.",
            },
            {
                "label": "Cambridge Analytica",
                "color": "green",
                "text": "87 million Facebook profiles were collected without users' knowledge via the GSR app. Consent covered friends too. GDPR (2018): behavioural data (RT, click patterns) = personal data requiring a legal basis.",
            },
        ],
        "question": "Your RT data from this course can identify you. What does 'anonymisation' mean for behavioural data? When do 'anonymous analytics data' become personal data under the GDPR?",
    },
}

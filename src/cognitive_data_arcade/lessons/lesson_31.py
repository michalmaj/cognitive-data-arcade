# src/cognitive_data_arcade/lessons/lesson_31.py
"""Lesson 31 - You Were the Dataset (behavioural data, observer effect, privacy)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Dane behawioralne to dane zbierane przez rejestrowanie zachowania, nie deklaracji. Kazde nacisnieccie klawisza, kazdy czas reakcji, kazda odpowiedz w eksperymencie - to dane behawioralne. W tradycyjnej kognitywistyce badacz celowo zbiera te dane od uczestnika. W swiecie big data zbieraja je aplikacje, platformy i urzadzenia - czesto bez swiadomosci uzytkownika.",
            "Efekt Hawthorne'a: zachowanie zmienia sie, gdy wiemy ze jestesmy obserwowani. Termin pochodzi od eksperymentow Eltona Mayo (1924-1932) w zakladach Western Electric Hawthorne Works kolo Chicago - robotnicy pracowali wydajniej za kazdym razem, gdy zmieniano warunki oswietlenia, niezaleznie od kierunku zmiany. Henry Landsberger skul termin 'Hawthorne effect' w 1958. W tym kursie uczestnicy nie byli informowani explicite, ze kazda gra zapisuje dane do pliku CSV - ten paradoks lezy u podstaw kazdej etyki badan naukowych.",
            "Dane behawioralne sa nieoczekiwanie identyfikujace. Efekt Stroopa, czasy reakcji i wzorce bledow razem tworza unikalny 'odcisk poznawczy'. Badania pokazuja, ze styl pisania na klawiaturze (typing dynamics), wzorce klikniec myszy czy czas spedzony na kazdym elemencie strony moga identyfikowac osobe z dokladnoscia przekraczajaca 95% - nawet bez zadnych danych osobowych. Michal Kosinski (Cambridge, 2013) pokazal, ze 150 lajkow na Facebooku pozwala przewidziec cechy osobowosci OCEAN dokladniej niz znajomi, 300 lajkow - dokladniej niz partner.",
            "Cambridge Analytica (2018): firma zebrala dane behawioralne z lajkow 87 milionow uzytkownikow Facebooka bez ich wiedzy i uzyla ich do psychograficznego targetowania politycznego podczas wyborow w USA i Brexit. Dane pozyskano przez aplikacje GSR (Global Science Research) - uzytkownik wyrazal zgode, ale obejmowala ona rowniez znajomych. Christopher Wylie, sygnalizator wewnetrzny, ujawnil dzialania firmy w 2018. To przyklad jak dane behawioralne agregowane na skale miliardow uzytkownikow moga wplywac na demokratyczne procesy.",
            "Prywatnosc danych behawioralnych jest regulowana przez RODO od 2018 roku. Dane o zachowaniu uzytkownika (czas reakcji, wzorce klikniec, historia przegladania) sa danymi osobowymi i wymagaja podstawy prawnej do przetwarzania. Wiele platform zbiera je w sposob niejawny jako 'dane analityczne'. Najwyzsze kary RODO: Meta 1,2 mld euro (2023, DPC Irlandia - transfer danych do USA), Amazon 746 mln euro (2021). Granica miedzy 'anonimowymi danymi analitycznymi' a danymi osobowymi jest znacznie ciensza niz wiekszoscia firm przyznaje.",
        ],
        "notes": [
            "Badanie 'You Are What You Like' (Youyou, Kosinski, Stillwell, PNAS 2015): na podstawie 300 lajkow model komputerowy przewidywal cechy osobowosci dokladniej niz male-zonek osoby badanej. Na podstawie 10 lajkow - dokladniej niz wspolpracownicy. To badanie bezposrednio zainspirowalo model psychograficzny Cambridge Analytica. Kosinski sam nie wspolpracowal z CA - jedynie opublikowal metode, ktora inni wykorzystali bez jego wiedzy.",
            "RODO (Ogolne Rozporzadzenie o Ochronie Danych, 2018): kazde przetwarzanie danych osobowych wymaga podstawy prawnej (zgoda, umowa, uzasadniony interes). Prawo do bycia zapomnianym oznacza prawo do zadania usuniecia wszystkich danych. EU AI Act (2024) naklada dodatkowe wymogi na systemy AI wysokiego ryzyka w zakresie transparentnosci i audytowalnosci.",
        ],
        "tasks": [
            "Na podstawie kognitywnego profilu zebranego w kursie - co jest najbardziej zaskakujace? Czy wyniki zgadzaja sie z subiektywnym poczuciem wlasnych zdolnosci? Co efekt Stroopa mowi o tym, jak mozg przetwarza sprzeczne informacje?",
            "Firma reklamowa ma dostep do 1000 nacisniec klawiszy dziennie podczas typowej pracy. Jakie cechy osobowosci lub zachowania mozna z nich wywnioskowac? Czy taka wymiana - dane w zamian za bezplatna aplikacje - jest uczciwa?",
            "W tym kursie dane zbierane sa lokalnie - tylko na komputerze uczestnika. Jak zmienioby sie uczestnictwo, gdyby dane trafily na serwer? A gdyby byly anonimowe? A gdyby byly publiczne? Gdzie przebiega granica miedzy akceptowalnym a nieakceptowalnym zbieraniem danych?",
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

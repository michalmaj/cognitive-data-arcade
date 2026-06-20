# src/cognitive_data_arcade/lessons/lesson_31.py
"""Lesson 31 -- You Were the Dataset (behavioural data, observer effect, privacy)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Dane behawioralne to dane zbierane przez rejestrowanie zachowania, "
            "nie deklaracji. Każde naciśnięcie klawisza, każdy czas reakcji, każda "
            "odpowiedź w eksperymencie — to dane behawioralne. W tradycyjnej "
            "kognitywistyce badacz celowo zbiera te dane od uczestnika. "
            "W świecie big data zbierają je aplikacje, platformy i urządzenia — "
            "często bez świadomości użytkownika.",
            "Efekt obserwatora (Efekt Hawthorne'a): zachowanie zmienia się, "
            "gdy wiemy że jesteśmy obserwowani. W tym kursie nie informowaliśmy "
            "explicite, że każda gra zapisuje Twoje dane do pliku CSV. "
            "Teraz wiesz. Jak by zmieniło się Twoje zachowanie, gdybyś wiedział "
            "od początku? Ten paradoks leży u podstaw każdej etyki badań naukowych.",
            "Dane behawioralne są nieoczekiwanie identyfikujące. Twój efekt Stroopa, "
            "czas reakcji i wzorzec błędów razem tworzą unikalny 'odcisk poznawczy'. "
            "Badania pokazują, że styl pisania na klawiaturze, wzorce kliknięć myszy "
            "czy czas spędzony na każdym elemencie strony mogą identyfikować osobę "
            "z dokładnością przekraczającą 95% — nawet bez żadnych danych osobowych.",
            "Prywatność danych behawioralnych jest regulowana przez RODO od 2018 roku. "
            "Dane o zachowaniu użytkownika (czas reakcji, wzorce kliknięć, historia "
            "przeglądania) są danymi osobowymi i wymagają podstawy prawnej do przetwarzania. "
            "Jednak wiele platform zbiera je w sposób niejawny jako 'dane analityczne'. "
            "Granica między 'anonimowymi danymi analitycznymi' a danymi osobowymi "
            "jest znacznie cieńsza niż większość firm przyznaje.",
        ],
        "notes": [
            "Cambridge Analytica (2018): firma zebrała dane behawioralne z lajków "
            "na Facebooku (87 milionów użytkowników) bez ich wiedzy i użyła ich "
            "do psychograficznego targetowania politycznego podczas wyborów w USA i Brexit. "
            "Dane behawioralne (co lubisz, jak długo patrzysz na post, co ignorujesz) "
            "okazały się wystarczające do przewidywania cech osobowości i poglądów "
            "politycznych z wyższą dokładnością niż opinie znajomych lub partnera.",
            "RODO (Ogólne Rozporządzenie o Ochronie Danych, 2018): każde przetwarzanie "
            "danych osobowych wymaga podstawy prawnej (zgoda, umowa, uzasadniony interes). "
            "Dane behawioralne (wzorce kliknięć, czas spędzony na stronie, historia "
            "wyszukiwania) są uznawane za dane osobowe. Prawo do bycia zapomnianym "
            "oznacza że możesz zażądać usunięcia wszystkich danych o Tobie. "
            "EU AI Act (2024) nakłada dodatkowe wymogi na systemy AI wysokiego ryzyka "
            "w zakresie transparentności i audytowalności.",
        ],
        "tasks": [
            "Patrząc na swój kognitywny profil — co Cię najbardziej zaskoczyło? "
            "Czy wyniki zgadzają się z Twoim subiektywnym poczuciem własnych zdolności? "
            "Co mówi efekt Stroopa o tym jak Twój mózg przetwarza sprzeczne informacje?",
            "Wyobraź sobie, że firma reklamowa ma dostęp do 1000 naciśnięć klawiszy "
            "dziennie podczas pracy. Jakie cechy osobowości lub zachowania mogłaby "
            "z nich wywnioskować? Czy zgodziłbyś się na takie zbieranie danych "
            "w zamian za bezpłatną aplikację?",
            "W tym kursie zbieraliśmy Twoje dane lokalnie — tylko na Twoim komputerze. "
            "Jak zmieniłoby się Twoje uczestnictwo, gdybyś od początku wiedział "
            "że dane idą na serwer? A gdyby były anonimowe? A gdyby były publiczne? "
            "Narysuj granicę między akceptowalnym a nieakceptowalnym zbieraniem danych.",
        ],
    },
    "en": {
        "theory": [
            "Behavioural data is collected by recording behaviour, not declarations. "
            "Every keypress, every reaction time, every response in an experiment — "
            "that is behavioural data. In traditional cognitive science a researcher "
            "deliberately collects this data from a participant. In the big-data world "
            "apps, platforms, and devices collect it — often without the user's awareness.",
            "The observer effect (Hawthorne effect): behaviour changes when we know "
            "we are being observed. In this course we did not explicitly inform you "
            "that every game writes your data to a CSV file. Now you know. "
            "How would your behaviour have changed if you had known from the start? "
            "This paradox underpins all research ethics.",
            "Behavioural data is unexpectedly identifying. Your Stroop effect, "
            "reaction time, and error pattern together form a unique 'cognitive fingerprint'. "
            "Research shows that typing patterns, mouse-click sequences, or dwell time "
            "per page element can identify a person with over 95% accuracy — "
            "even with no personal data whatsoever.",
            "Privacy of behavioural data has been regulated by GDPR since 2018. "
            "Data about user behaviour (reaction time, click patterns, browsing history) "
            "is personal data and requires a legal basis for processing. "
            "Yet many platforms collect it covertly as 'analytics data'. "
            "The boundary between 'anonymous analytics' and personal data "
            "is much thinner than most companies admit.",
        ],
        "notes": [
            "Cambridge Analytica (2018): the company harvested behavioural data from "
            "87 million Facebook users' likes without their knowledge and used it "
            "for psychographic political targeting in the US election and Brexit. "
            "Behavioural data (what you like, how long you look at a post, what you ignore) "
            "proved sufficient to predict personality traits and political views "
            "more accurately than the opinions of friends or a partner.",
            "GDPR (General Data Protection Regulation, 2018): every processing of "
            "personal data requires a legal basis (consent, contract, legitimate interest). "
            "Behavioural data (click patterns, dwell time, search history) is classified "
            "as personal data. The right to be forgotten means you can request deletion "
            "of all data about you. The EU AI Act (2024) adds further requirements "
            "on high-risk AI systems regarding transparency and auditability.",
        ],
        "tasks": [
            "Looking at your cognitive profile — what surprised you most? "
            "Do the results match your subjective sense of your own abilities? "
            "What does the Stroop effect say about how your brain processes conflicting information?",
            "Imagine an advertising company has access to 1000 of your keypresses "
            "per day while you work. What personality traits or behaviours could they infer? "
            "Would you agree to such data collection in exchange for a free app?",
            "In this course we collected your data locally — only on your computer. "
            "How would your participation have changed if you had known from the start "
            "that data goes to a server? What if it were anonymous? What if it were public? "
            "Draw the line between acceptable and unacceptable data collection.",
        ],
    },
}

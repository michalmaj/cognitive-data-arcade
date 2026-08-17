# Wkład w projekt Cognitive Data Arcade

## Cele wersji beta

Bieżącym celem stabilizacji jest wydanie wersji beta nadającej się do użytku na zajęciach **10 października 2026 r.**

Celem nie jest maksymalizacja liczby zmienionych linii kodu. Celem jest uczynienie projektu:

- **stabilnym** — bez crashów P0, blokad nawigacji ani utraty danych,
- **odpowiedzialnym naukowo** — bez niepopartych norm, bez języka diagnostycznego dla krótkich zadań behawioralnych,
- **użytecznym dydaktycznie** — pojęcia wyjaśnione klarownie i z odpowiednią niepewnością,
- **przejrzystym w kwestii lokalnych danych** — studenci wiedzą, co jest przechowywane i jak to usunąć,
- **łatwiejszym w utrzymaniu** — ścieżki uruchamiania, ścieżki danych i metadane lekcji są skonsolidowane,
- **przewidywalnym do testowania i pakowania** — CI działa niezawodnie; spakowana aplikacja uruchamia się z czystego katalogu.

### Jawnie przesunięte poza beta

To są poprawne ulepszenia, które nie będą blokować wydania beta:

- pełna migracja treści lekcji do Markdown lub YAML,
- typowanie całej warstwy UI Pygame,
- eliminacja wszystkich testów dotykających prywatnych składowych,
- nowe gry lub moduły,
- refaktory kosmetyczne i przeprojektowania wizualne,
- ogólne abstrakcje storage bez konkretnej korzyści dla beta.

W razie presji harmonogramu: najpierw odcinamy te elementy — nigdy poprawności naukowej ani przejrzystości prywatności.

---

## Bramki jakości

### P0 — blokady beta

Projekt nie może zostać otagowany jako beta, dopóki którakolwiek z poniższych kwestii pozostaje otwarta:

- Menu i ścieżki uruchamiania modułów korzystają z jednego kanonicznego mechanizmu tworzenia gier.
- Restart gry tworzy świeży stan rozgrywki (bez ponownego użycia zmutowanej sceny).
- Ścieżki danych użytkownika nie zależą od bieżącego katalogu roboczego.
- Zbieranie danych lokalnych jest wyraźnie ujawnione studentowi.
- Student może zrozumieć, co jest przechowywane lokalnie, i usunąć dane z rozgrywki.
- Panel kognitywny nie przedstawia wyników krótkich gier jako diagnoz ani stabilnych cech osobowości lub zdolności kognitywnych.
- Nieobsługiwane uniwersalne „normy" i pseudonormatywne progi zostały usunięte lub prawidłowo zacytowane i skontekstualizowane.
- Treści edukacyjne wysokiego ryzyka przeszły audyt merytoryczny.
- Spakowana aplikacja uruchamia się poprawnie i ma dostęp do swoich zasobów.
- Kluczowe przepływy smoke dla beta przechodzą.
- Nie pozostaje żaden znany crash P0, błąd utraty danych, blokada nawigacji ani wprowadzające w błąd twierdzenie naukowe.

### P1 — oczekiwane dla beta

Naprawić przed tagiem beta; jawnie udokumentować, jeśli odłożone:

- Teksty edukacyjne sprawdzone pod kątem nadmiernej pewności siebie w stylu LLM.
- Ważne twierdzenia edukacyjne mają metadane źródłowe tam, gdzie to stosowne.
- Duplikacja logowania prób jest zredukowana.
- Dokumentacja odpowiada rzeczywistemu zachowaniu aplikacji.
- Konfiguracja Ruff jest silniejsza niż w alpha.
- Rdzenne moduły non-Pygame mają ukierunkowane typowanie statyczne.
- Główne zmodyfikowane obszary mają testy na poziomie zachowania, a nie tylko testy metod prywatnych.

### P2 — odłożyć swobodnie

Elementy wymienione w sekcji „jawnie przesunięte poza beta" powyżej.

---

## Konwencje commitów

### Prefiksy

Używaj jednego z tych konwencjonalnych prefiksów przy każdym commicie:

```
test:      dodanie lub aktualizacja testów
fix:       naprawa błędu
feat:      dodanie nowego zachowania
refactor:  restrukturyzacja bez zamierzonej zmiany zachowania
content:   zmiana tekstu edukacyjnego lub treści lekcji
docs:      aktualizacja dokumentacji
tooling:   dodanie lub aktualizacja narzędzia developerskiego lub skryptu
build:     zmiana konfiguracji budowania lub pakowania
ci:        zmiana konfiguracji CI/CD
typing:    dodanie lub poprawa adnotacji typów
style:     tylko formatowanie (zazwyczaj z ruff)
chore:     konserwacja (gitignore, bump wersji itp.)
release:   przygotowanie wydania
```

### Granularność

Dąż do **4–10 sensownych commitów na normalny PR**. Każdy commit powinien być:

- zrozumiały sam w sobie,
- możliwy do przejrzenia w izolacji,
- odwracalny przez `git revert`,
- użyteczny przez `git bisect`.

Dla zmian behawioralnych preferuj tę kolejność:

```
test:     odtwórz lub utrwal bieżące zachowanie
refactor: przygotuj strukturę bez zamierzonej zmiany zachowania
fix/feat: zaimplementuj zachowanie
test:     pokryj przypadki brzegowe i regresje
docs:     zsynchronizuj dokumentację
```

### Czego unikać

```
fix stuff
oops
fix typo
actually fix
more cleanup
```

Nie ściskaj dobrze ustrukturyzowanej sekwencji test/refactor/fix/docs w jeden gigantyczny commit.

### Zakres PR

Jeden PR powinien rozwiązywać **jeden spójny problem**. Przykłady dobrego zakresu:

- konsolidacja ścieżek uruchamiania,
- centralizacja ścieżek aplikacji,
- korekta języka interpretacji panelu,
- audyt zestawu powiązanych lekcji.

Nie łącz refaktorów architektonicznych, przepisywania lekcji i poprawek UI w jednym PR.

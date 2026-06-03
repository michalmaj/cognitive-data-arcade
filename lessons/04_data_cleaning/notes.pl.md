# Notatki dla prowadzącego — Czyszczenie danych

## Przewodnik czasowy

| Aktywność | Czas | Uwagi |
|---|---|---|
| Czytanie teorii (własnym tempem) | 25–30 min | Zadać przed zajęciami; podkreślić sekcje 3 i 6 (kryteria wykluczenia i odtwarzalne czyszczenie) |
| Zadania 1–3 (liczenie i wyszukiwanie wartości odstających) | 15–20 min | Studenci pracują z tym samym plikiem CSV co w Lekcji 03 |
| Zadanie 4 (fragment kodu Python) | 10 min | Opcjonalne; zademonstrować na żywo, jeśli większość studentów nie ma doświadczenia z Pythonem |
| Dyskusja | 20–25 min | Zob. wskazówki do pytań poniżej |
| **Razem** | **~70–85 min** | |

## Oczekiwane obserwacje podczas zadań

Studenci przeglądający CSV z typowej krótkiej sesji gry (20–40 prób) mogą nie znaleźć żadnych wartości odstających — to oczekiwany i prawidłowy wynik. Jeśli nie zostaną znalezione żadne wartości odstające, nakieruj studentów na rozumowanie o wskaźniku wykluczenia (0%) i co to oznacza (czysta sesja, uczestnik stosujący się do zadania). Jest to użyteczny kontrast z typowym założeniem, że „czyszczenie zawsze coś znajdzie".

Dla studentów, którzy grali wyjątkowo długo lub niedbale, mogą pojawić się wolne próby powyżej 2 000 ms. Są to najbardziej pouczające przypadki — poproś tych studentów o podzielenie się danymi z klasą.

Zadanie z fragmentem kodu Python jest najbardziej technicznie wymagające. Jeśli większość studentów nie ma doświadczenia z Pythonem, uruchom kod na żywo jako demonstrację, a studenci śledzą, czytając wynik, zamiast pisać kod samodzielnie.

## Wskazówki do pytań dyskusyjnych

**Pytanie 1 — Dlaczego nie można po prostu usunąć wierszy z wartościami odstającymi w Excelu?**
Kluczowe punkty: (1) usunięcie nie jest nigdzie zapisane — nie można odtworzyć, co zostało usunięte; (2) surowy plik jest trwale zmodyfikowany i nie można wrócić do stanu przed zmianą; (3) współpracownik korzystający ze skryptu nie może zweryfikować Twojej pracy. Kontrast z udokumentowanym skryptem Python powinien być wyraźny: skrypt jest ścieżką audytu.

**Pytanie 2 — Czy przekroczenie limitu czasu to to samo co bardzo wolna odpowiedź?**
Oczekiwana odpowiedź: nie. Przekroczenie limitu czasu oznacza, że uczestnik nie odpowiedział w oknie — może to oznaczać rozproszenie uwagi, dezorientację co do zadania lub awarię techniczną. Wolna odpowiedź (np. 1 800 ms) oznacza, że odpowiedział, ale wolno. Niosą różne informacje o przetwarzaniu poznawczym. Studenci czasem je utożsamiają, bo oba są „złymi" wynikami; nakieruj ich na rozróżnienie mechanizmu.

**Pytanie 3 — Jeśli prerejestracja jest taka ważna, dlaczego nie wszyscy badacze ją stosują?**
Spodziewaj się różnych odpowiedzi: brak świadomości, dodatkowy koszt czasowy, obawa, że recenzenci ukarzą pracę eksploracyjną, normy kulturowe w niektórych subdyscyplinach. Ważne jest, że prerejestracja nie polega na braku zaufania do badaczy — chodzi o stworzenie ścieżki dokumentacyjnej, która sprawia, że wyniki są bardziej wiarygodne dla czytelników, w tym przyszłych replikatorów.

## Częste błędy i nieporozumienia

- **„Czyszczenie oznacza usunięcie wszystkich prób, w których uczestnik popełnił błąd."** Nieprawidłowe odpowiedzi to prawidłowe dane do analiz dokładności. Próby z błędami nie powinny być wykluczone z liczników dokładności; mogą być wykluczone z analiz RT (jeśli pytanie badawcze dotyczy tylko szybkości prawidłowych odpowiedzi), ale musi to być jawnie stwierdzone.
- **„Im więcej czyścisz, tym lepsze dane."** Agresywne czyszczenie redukuje wariancję i może sztucznie zmniejszyć pozorny rozkład RT. Czyszczenie powinno być motywowane zasadniczymi kryteriami, a nie chęcią uzyskania lepiej wyglądających wyników.
- **„Jeśli czyścisz tak samo jak inni w laboratorium, nie musisz tego zapisywać."** Konwencje laboratoryjne nie są publiczne. Czytelnik opublikowanego artykułu nie ma dostępu do konwencji laboratoryjnych. Każdy artykuł wymaga własnego raportu czyszczenia.
- **„Python jest wymagany do odtwarzalnego czyszczenia."** Każdy język skryptowy działa: R, MATLAB, Julia. Zasadnicze wymaganie to, że potok jest skryptem, a nie ręczną sekwencją kliknięć.

## Połączenie z następnymi lekcjami

Lekcja 05 i następne wprowadzają statystykę wnioskującą na danych RT. Przed tymi lekcjami studenci powinni rozumieć, że liczby, które wprowadzają do testów statystycznych, są wynikiem decyzji dotyczących czyszczenia. Statystycznie istotny efekt Stroopa ma znaczenie tylko wtedy, gdy analityk może wykazać, że wybory dotyczące czyszczenia nie stworzyły ani nie zniszczyły efektu. Ta lekcja jest fundamentem dla tej krytycznej perspektywy.

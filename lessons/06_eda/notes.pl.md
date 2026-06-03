# Notatki dla prowadzącego — Eksploracyjna analiza danych

## Harmonogram zajęć

| Aktywność | Czas | Uwagi |
|---|---|---|
| Czytanie teorii (własnym tempem) | 25–30 min | Zalecane przed zajęciami |
| Ćwiczenia z zadaniami | 25–30 min | Zademonstruj kroki 1–3 na żywo, potem studenci pracują samodzielnie |
| Dyskusja | 20 min | Patrz wskazówki poniżej |
| **Łącznie** | **~70–80 min** | |

## Cel pedagogiczny

EDA jest trudnym tematem do zmotywowania dla początkujących, bo wygląda jak „tylko patrzenie na dane". Kluczem jest pokazanie, że patrzenie ujawnia rzeczy, które liczby ukrywają.

**Zalecane otwarcie:** Przed pokazaniem jakiejkolwiek teorii zapytaj studentów: „Przeprowadziłeś eksperyment Stroopa. Średnie RT dla warunku niezgodnego wynosi 620 ms, a dla zgodnego 540 ms. Czy to realna różnica?" Większość studentów powie tak. Pokaż wtedy dwa scenariusze:
- Scenariusz A: rozkłady ledwo się nakładają — różnica jest realna.
- Scenariusz B: SD w każdym warunku wynosi 400 ms i rozkłady są prawie identyczne — średnie różnią się z powodu trzech skrajnych wartości odstających.

Oba scenariusze mają dokładnie te same średnie. To motywuje EDA.

## Wskazówki do pytań dyskusyjnych

**Pytanie 1 — Co histogram RT mówi Ci, czego średnia nie mówi?**
Kluczowe punkty: kształt (skośność, bimodalność), rozrzut, obecność i lokalizacja wartości odstających, efekty podłogowe (wiele odpowiedzi skupionych blisko minimum), efekty sufitowe (wiele odpowiedzi blisko górnej granicy). Średnia 580 ms może opisywać ciasny jednomodalny rozkład lub bimodalny rozkład z jednym skupieniem przy 400 ms i drugim przy 760 ms. Samej średniej nie można tego rozróżnić.

**Pytanie 2 — Kwartet Anscombe'a: czy to realny problem w kognitywistyce?**
Tak. Kanoniczny przykład: dwie grupy badawcze obliczają korelację między pojemnością pamięci roboczej a osiągnięciami szkolnymi jako r = 0,45. Wykres rozrzutu grupy A pokazuje czysty związek liniowy. Wykres rozrzutu grupy B pokazuje związek krzywoliniowy — korelacja jest napędzana przez efekt sufitowy przy wysokiej pojemności pamięci roboczej. Te same r, zupełnie różne implikacje. Zachęcaj studentów, by zawsze rysowali przed obliczaniem r.

**Pytanie 3 — Jeśli EDA ujawnia wzorzec, którego nie pre-rejestrowałeś, co powinieneś zrobić?**
To krytyczny związek z otwartą nauką. Wynik wyłaniający się z EDA jest **eksploracyjny** — może być prawdziwym efektem lub szumem. Uczciwe podejście:
1. Raportuj go jako eksploracyjny i wyraźnie go tak oznacz.
2. Zbierz nowe dane, aby przetestować hipotezę w pre-rejestrowanym badaniu konfirmacyjnym.
3. NIE przeformułowuj post factum odkrycia eksploracyjnego jako konfirmacyjnego (nazywa się to HARKing — Hypothesizing After Results are Known).

## Typowe błędy rozumowania

- **„EDA to tylko obliczanie statystyk opisowych."** EDA jest przede wszystkim wizualna. Tabela średnich mówi prawie nic w porównaniu z histogramem, wykresem skrzypcowym i wykresem porównania warunków razem wziętymi.
- **„Wykres Q-Q wyglądał dobrze, więc dane są normalne."** Żaden test nie potwierdza normalności; testy mogą ją tylko odrzucić. Wykres Q-Q wyglądający w przybliżeniu prosto oznacza, że założenie normalności *nie jest oczywiste naruszone* przy tej wielkości próby — nie że dane są normalne. Przy małych próbach nienormalne rozkłady mogą dawać proste wykresy Q-Q.
- **„Mój histogram wygląda jak dzwon, więc t-test jest w porządku."** Rozkłady RT nie są normalne nawet gdy wyglądają z grubsza jak dzwon. Prawy ogon jest zawsze dłuższy od lewego. Transformacja logarytmiczna jest zalecana dla analiz parametrycznych.

## Powiązanie z praktyką

Przepływ pracy EDA z sekcji 5 teorii (wczytaj → brakujące → describe → rozkłady → porównanie warunków → trendy czasowe → różnice indywidualne) powinien być przedstawiony jako **powtarzalna lista kontrolna**, którą studenci stosują do każdego nowego zbioru danych. Rozważ stworzenie drukowanej karty z listą kontrolną do laboratorium.

Powiązanie z Lekcją 05: studenci, którzy ukończyli zadania czyszczenia danych w Lekcji 05, powinni mieć gotowy oczyszczony plik CSV. Zadania tej lekcji działają najlepiej na oczyszczonych danych. Jeśli nie ukończyli jeszcze Lekcji 05, zaobserwują więcej skrajnych wartości odstających w swoich histogramach — co samo w sobie jest okazją do nauki.

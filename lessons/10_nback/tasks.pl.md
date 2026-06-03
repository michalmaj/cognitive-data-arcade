# Zadania — Pamiec robocza: N-Back Memory Grid

Wykonaj ponizsze kroki podczas lekcji. Zapisuj dane w zeszycie lub udostepnionym dokumencie zgodnie ze wskazowkami prowadzacego.

## Krok 1: Uruchom aplikacje

Otworz terminal w katalogu projektu i wykonaj polecenie:

```
uv run cognitive-data-arcade
```

## Krok 2: Otworz Lekcje 10

Przejdz do pozycji **Lekcja 10 — N-Back Memory Grid** za pomoca klawiszy strzalek i nacisnij **ENTER**.

Przeczytaj slajdy wprowadzajace, aby zrozumiec zasady zadania przed rozpoczeciem. Zwroc szczegolna uwage na wyjasnienie, co w praktyce oznacza "dopasowanie sprzed n krokow".

## Krok 3: Graj na poziomie 1-Back

Wybierz **1-Back** z menu sesji. Ukonczyj jedna pelna sesje.

Zasady:
- Bodziec pojawia sie w pozycji na siatce (i/lub wyswietlana lub wypowiadana jest litera).
- Nacisnij **SPACJE** (lub wyznaczony klawisz dopasowania), jezeli biezacy bodziec pasuje do bodzcca **sprzed 1 kroku**.
- Nic nie rob, jesli nie pasuje.

Na koncu sesji zapisz nastepujace wartosci z ekranu wynikow:

| Miara (1-Back) | Twoj wynik |
|---|---|
| Lacznie prob dopasowania (Go) | |
| Lacznie prob niedopasowania (No-Go) | |
| Prawidlowe dopasowania (trafienia) | |
| Pominiete dopasowania (chybienia) | |
| Bledne dopasowania (falszywe alarmy) | |
| Prawidlowe niedopasowania (prawidlowe odrzucenia) | |
| Sredni czas reakcji w probach dopasowania (ms) | |

## Krok 4: Graj na poziomie 2-Back

Wrocz do menu sesji i wybierz **2-Back**. Ukonczyj jedna pelna sesje. Zapisz te same miary co w Kroku 3 w drugim wierszu.

| Miara (2-Back) | Twoj wynik |
|---|---|
| Lacznie prob dopasowania | |
| Lacznie prob niedopasowania | |
| Prawidlowe dopasowania (trafienia) | |
| Pominiete dopasowania (chybienia) | |
| Bledne dopasowania (falszywe alarmy) | |
| Prawidlowe niedopasowania (prawidlowe odrzucenia) | |
| Sredni czas reakcji w probach dopasowania (ms) | |

## Krok 5: Oblicz d' dla 1-Back i 2-Back

Dla kazdego poziomu oblicz:

```
Wskaznik trafien = Prawidlowe dopasowania / Lacznie prob dopasowania
Wskaznik FA = Bledne dopasowania / Lacznie prob niedopasowania
d' = Z(wskaznik trafien) - Z(wskaznik FA)
```

Uzyj tabeli wartosci z w theory.pl.md. Wypelnij tabele porownawcza:

| Poziom n | Wskaznik trafien | Wskaznik FA | d' |
|---|---|---|---|
| 1-Back | | | |
| 2-Back | | | |

Jak zmienilo sie d' miedzy 1-Back a 2-Back? O ile?

## Krok 6: Graj w trybie Adaptacyjnym

Wybierz **Adaptacyjny** z menu sesji. Zagraj co najmniej dwie kolejne sesje bez zamykania aplikacji miedzy nimi.

System dynamicznie dostosowuje n na podstawie Twojej trafnosci:
- Jesli Twoja trafnosc przekracza ~85%, n wzrasta o 1.
- Jesli Twoja trafnosc spada ponizej ~65%, n maleje o 1.
- Cel to okolo 75% trafnosci.

Zapisz:
- Poziom n na poczatku sesji 1
- Koncowy poziom n na koncu sesji 1
- Koncowy poziom n na koncu sesji 2
- Czy n wzroslo, spalo, czy pozostalo stabilne?

## Krok 7: Pytania refleksyjne

Napisz krotkie odpowiedzi na ponizsze pytania — moga stanowic podstawe dyskusji grupowej:

1. Na ktorym poziomie n wyniki poczuly sie jakosiowo inne (nie tylko trudniejsze, ale inny rodzaj zadania)? Czy potrafisz opisac, co sie zmienilo?
2. Czy Twoj wskaznik trafien czy wskaznik falszywych alarmow zmienil sie bardziej miedzy 1-Back a 2-Back? Co to sugeruje o tym, ktory rodzaj bledu staje sie trudniejszy do kontrolowania przy wyzszym n?
3. Po dwoch sesjach Adaptacyjnych — przy jakim poziomie n ustabilizował sie system? Czy sadzisz, ze odzwierciedla to Twoja rzeczywista pojemnosc WM, czy jest pod wplywem innych czynnikow (zmeczenie, znajomosc zadania, motywacja)?
4. Gdyby badacz twierdził, ze granie 30 minut n-back dziennie przez 4 tygodnie podniesie Twoje IQ o 5 punktow, co musialabys/musialabys zobaczyc, zanim uwierzysz temu twierdzeniu? Wymien co najmniej trzy konkretne wymagania metodologiczne.
5. Porownaj sredni czas reakcji w probach dopasowania w 1-Back i 2-Back. Dlaczego czas reakcji jest wolniejszy przy 2-Back, nawet w prawidlowych probach?

## Pytania dyskusyjne

Przyniés swoje wartosci d' i poziomy sesji Adaptacyjnych na dyskusje grupowa:

1. **Czym jest pamiec robocza i dlaczego rozni sie od "dobrej pamieci"?** Odpowiedz uzywajac modelu Baddeleya.
2. **Twierdzenie Jaeggi (2008): dlaczego nie zostalo zreplikowane?** Jakie czynniki metodologiczne wyjasnaja rozbieznosc miedzy pierwotnym wynikiem a kolejnymi metaanalizami?
3. **Roznice indywidualne:** Czy rozni studenci w Twojej grupie ustabilizowali sie na roznych poziomach Adaptacyjnych? Jakie czynniki (inne niz pojemnosc WM) moga tlumaczac te zmiennosc?

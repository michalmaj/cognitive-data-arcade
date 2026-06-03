# Zadania — Pamięć robocza: N-Back Memory Grid

Wykonaj poniższe kroki podczas lekcji. Zapisuj dane w zeszycie lub udostępnionym dokumencie zgodnie ze wskazówkami prowadzącego.

## Krok 1: Uruchom aplikację

Otwórz terminal w katalogu projektu i wykonaj polecenie:

```
uv run cognitive-data-arcade
```

## Krok 2: Otwórz Lekcję 10

Przejdź do pozycji **Lekcja 10 — N-Back Memory Grid** za pomocą klawiszy strzałek i naciśnij **ENTER**.

Przeczytaj slajdy wprowadzające, aby zrozumieć zasady zadania przed rozpoczęciem. Zwróć szczególną uwagę na wyjaśnienie, co w praktyce oznacza "dopasowanie sprzed n kroków".

## Krok 3: Graj na poziomie 1-Back

Wybierz **1-Back** z menu sesji. Ukończ jedną pełną sesję.

Zasady:
- Bodziec pojawia się w pozycji na siatce (i/lub wyświetlana lub wypowiadana jest litera).
- Naciśnij **SPACJĘ** (lub wyznaczony klawisz dopasowania), jeżeli bieżący bodziec pasuje do bodźca **sprzed 1 kroku**.
- Nic nie rób, jeśli nie pasuje.

Na końcu sesji zapisz następujące wartości z ekranu wyników:

| Miara (1-Back) | Twój wynik |
|---|---|
| Łącznie prób dopasowania (Go) | |
| Łącznie prób niedopasowania (No-Go) | |
| Prawidłowe dopasowania (trafienia) | |
| Pominięte dopasowania (chybienia) | |
| Błędne dopasowania (fałszywe alarmy) | |
| Prawidłowe niedopasowania (prawidłowe odrzucenia) | |
| Średni czas reakcji w próbach dopasowania (ms) | |

## Krok 4: Graj na poziomie 2-Back

Wróć do menu sesji i wybierz **2-Back**. Ukończ jedną pełną sesję. Zapisz te same miary co w Kroku 3 w drugim wierszu.

| Miara (2-Back) | Twój wynik |
|---|---|
| Łącznie prób dopasowania | |
| Łącznie prób niedopasowania | |
| Prawidłowe dopasowania (trafienia) | |
| Pominięte dopasowania (chybienia) | |
| Błędne dopasowania (fałszywe alarmy) | |
| Prawidłowe niedopasowania (prawidłowe odrzucenia) | |
| Średni czas reakcji w próbach dopasowania (ms) | |

## Krok 5: Oblicz d' dla 1-Back i 2-Back

Dla każdego poziomu oblicz:

```
Wskaźnik trafień = Prawidłowe dopasowania / Łącznie prób dopasowania
Wskaźnik FA = Błędne dopasowania / Łącznie prób niedopasowania
d' = Z(wskaźnik trafień) - Z(wskaźnik FA)
```

Użyj tabeli wartości z w theory.pl.md. Wypełnij tabelę porównawczą:

| Poziom n | Wskaźnik trafień | Wskaźnik FA | d' |
|---|---|---|---|
| 1-Back | | | |
| 2-Back | | | |

Jak zmieniło się d' między 1-Back a 2-Back? O ile?

## Krok 6: Graj w trybie Adaptacyjnym

Wybierz **Adaptacyjny** z menu sesji. Zagraj co najmniej dwie kolejne sesje bez zamykania aplikacji między nimi.

System dynamicznie dostosowuje n na podstawie Twojej trafności:
- Jeśli Twoja trafność przekracza ~85%, n wzrasta o 1.
- Jeśli Twoja trafność spada poniżej ~65%, n maleje o 1.
- Cel to około 75% trafności.

Zapisz:
- Poziom n na początku sesji 1
- Końcowy poziom n na końcu sesji 1
- Końcowy poziom n na końcu sesji 2
- Czy n wzrosło, spadło, czy pozostało stabilne?

## Krok 7: Pytania refleksyjne

Napisz krótkie odpowiedzi na poniższe pytania — mogą stanowić podstawę dyskusji grupowej:

1. Na którym poziomie n wyniki poczuły się jakościowo inne (nie tylko trudniejsze, ale inny rodzaj zadania)? Czy potrafisz opisać, co się zmieniło?
2. Czy Twój wskaźnik trafień czy wskaźnik fałszywych alarmów zmienił się bardziej między 1-Back a 2-Back? Co to sugeruje o tym, który rodzaj błędu staje się trudniejszy do kontrolowania przy wyższym n?
3. Po dwóch sesjach Adaptacyjnych — przy jakim poziomie n ustabilizował się system? Czy sądzisz, że odzwierciedla to Twoją rzeczywistą pojemność WM, czy jest pod wpływem innych czynników (zmęczenie, znajomość zadania, motywacja)?
4. Gdyby badacz twierdził, że granie 30 minut n-back dziennie przez 4 tygodnie podniesie Twoje IQ o 5 punktów, co musiałbyś/musiałabyś zobaczyć, zanim uwierzysz temu twierdzeniu? Wymień co najmniej trzy konkretne wymagania metodologiczne.
5. Porównaj średni czas reakcji w próbach dopasowania w 1-Back i 2-Back. Dlaczego czas reakcji jest wolniejszy przy 2-Back, nawet w prawidłowych próbach?

## Pytania dyskusyjne

Przynieś swoje wartości d' i poziomy sesji Adaptacyjnych na dyskusję grupową:

1. **Czym jest pamięć robocza i dlaczego różni się od "dobrej pamięci"?** Odpowiedź używając modelu Baddeleya.
2. **Twierdzenie Jaeggi (2008): dlaczego nie zostało zreplikowane?** Jakie czynniki metodologiczne wyjaśniają rozbieżność między pierwotnym wynikiem a kolejnymi metaanalizami?
3. **Różnice indywidualne:** Czy różni studenci w Twojej grupie ustabilizowali się na różnych poziomach Adaptacyjnych? Jakie czynniki (inne niż pojemność WM) mogą tłumaczyć tę zmienność?

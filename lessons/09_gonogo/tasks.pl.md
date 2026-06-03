# Zadania — Hamowanie odpowiedzi: Go/No-Go Guard

Wykonaj poniższe kroki podczas lekcji. Zapisuj dane w zeszycie lub udostępnionym dokumencie zgodnie ze wskazówkami prowadzącego.

## Krok 1: Uruchom aplikację

Otwórz terminal w katalogu projektu i wykonaj polecenie:

```
uv run cognitive-data-arcade
```

## Krok 2: Otwórz Lekcję 09

Przejdź do pozycji **Lekcja 09 — Go/No-Go Guard** za pomocą klawiszy strzałek i naciśnij **ENTER**.

Przeczytaj slajdy wprowadzające (klawisze strzałek lub SPACJA, aby przejść dalej). Zwróć uwagę na rozróżnienie między bodźcami Go i No-Go dla bieżącej sesji.

## Krok 3: Graj na poziomie Średnim

Wybierz **Sesja standardowa, poziom Średni** z menu sesji. Daje to około 80 prób z 75% bodźcami Go i oknem odpowiedzi 1,0 sekundy.

- Naciśnij **SPACJĘ**, gdy zobaczysz bodziec Go.
- **Nie** naciskaj nic, gdy zobaczysz bodziec No-Go.

Na końcu sesji zapisz następujące wartości wyświetlone na ekranie wyników:

| Miara | Twój wynik |
|---|---|
| Łącznie prób Go | |
| Łącznie prób No-Go | |
| Prawidłowe odpowiedzi Go (trafienia) | |
| Pominięte odpowiedzi Go (chybienia) | |
| Odpowiedzi na No-Go (błędy komisji / fałszywe alarmy) | |
| Prawidłowe powstrzymania No-Go (prawidłowe odrzucenia) | |
| Średni czas reakcji w próbach Go (ms) | |

## Krok 4: Oblicz wskaźnik trafień i wskaźnik fałszywych alarmów

Używając danych z Kroku 3:

```
Wskaźnik trafień = Prawidłowe odpowiedzi Go / Łącznie prób Go
Wskaźnik FA = Błędy komisji / Łącznie prób No-Go
```

Zapisz obie wartości jako ułamki dziesiętne (np. 0,88, nie 88%).

## Krok 5: Oblicz d'

Użyj tabeli wartości z w theory.pl.md, aby odczytać Z(wskaźnik trafień) i Z(wskaźnik FA).

```
d' = Z(wskaźnik trafień) - Z(wskaźnik FA)
```

Zapisz swoje d'. Porównaj z tabelą interpretacji w theory.pl.md — co Twoje d' mówi o Twojej zdolności do rozróżniania Go od No-Go?

## Krok 6: Graj na poziomie Trudnym

Wróć do menu sesji i wybierz poziom **Trudny** (60% Go, okno odpowiedzi 0,7 sekundy). Ukończ pełną sesję.

Po sesji zapisz te same miary co w Kroku 3. Oblicz wskaźnik błędów komisji (wskaźnik FA) i d' dla tej sesji.

**Pytania porównawcze:**
- Czy Twój wskaźnik błędów komisji wzrósł, spadł, czy pozostał taki sam w porównaniu do poziomu Średniego?
- Czy Twoje d' się zmieniło? W którą stronę?
- Czy Twój średni czas reakcji w próbach Go się zmienił? Dlaczego może tak być?

## Krok 7: Pytania refleksyjne

Napisz krótkie odpowiedzi na poniższe pytania — mogą stanowić podstawę dyskusji grupowej:

1. Czy Twoje błędy komisji były równomiernie rozłożone przez sesję, czy skupiały się pod koniec? Co może to sugerować o wyczerpaniu hamowania?
2. Jeśli koleżanka/kolega miał 90% trafień i 20% wskaźnik FA, a Ty 80% trafień i 5% wskaźnik FA — kto ma wyższe d'? Oblicz obydwa i porównaj.
3. Pacjent z uszkodzeniem płatów czołowych wykazuje wiele błędów komisji, ale normalny czas reakcji w próbach Go. Co ten wzorzec mówi nam o neuronalnym rozdzieleniu szybkości odpowiedzi i hamowania odpowiedzi?
4. Zadanie Go/No-Go i zadanie Stroopa (jeśli realizowałeś/aś Lekcję 07) są używane do pomiaru "funkcji wykonawczych". Na podstawie doświadczenia z oboma: co jest podobne, a co różne w wymaganiach poznawczych, które stawiają?

## Pytania dyskusyjne

Przynieś swoje obliczone wartości d' i wskaźniki błędów komisji na dyskusję grupową:

1. **Co odróżnia błąd komisji od błędu pominięcia?** Który z nich bardziej niepokoi klinicystę w kontekście ADHD i dlaczego?
2. **Dwoje studentów osiąga 85% trafności. Czy jedno może być impulsywne, a drugie nieuważne?** Skonstruuj konkretny przykład używając wskaźników trafień i fałszywych alarmów.
3. **Dlaczego hamowanie odpowiedzi rozwija się aż do 25. roku życia?** Jaka struktura mózgu jest zaangażowana i dlaczego jej dojrzewanie trwa tak długo?

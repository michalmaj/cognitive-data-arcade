# Zadania — Hamowanie odpowiedzi: Go/No-Go Guard

Wykonaj ponizsze kroki podczas lekcji. Zapisuj dane w zeszycie lub udostepnionym dokumencie zgodnie ze wskazowkami prowadzacego.

## Krok 1: Uruchom aplikacje

Otworz terminal w katalogu projektu i wykonaj polecenie:

```
uv run cognitive-data-arcade
```

## Krok 2: Otworz Lekcje 09

Przejdz do pozycji **Lekcja 09 — Go/No-Go Guard** za pomoca klawiszy strzalek i nacisnij **ENTER**.

Przeczytaj slajdy wprowadzajace (klawisze strzalek lub SPACJA, aby przejsc dalej). Zwroc uwage na rozroznienie miedzy bodzcami Go i No-Go dla biezacej sesji.

## Krok 3: Graj na poziomie Srednim

Wybierz **Sesja standardowa, poziom Sredni** z menu sesji. Daje to okolo 80 prob z 75% bodzcami Go i oknem odpowiedzi 1,0 sekundy.

- Nacisnij **SPACJE**, gdy zobaczysz bodziec Go.
- **Nie** naciskaj nic, gdy zobaczysz bodziec No-Go.

Na koncu sesji zapisz nastepujace wartosci wyswietlone na ekranie wynikow:

| Miara | Twoj wynik |
|---|---|
| Lacznie prob Go | |
| Lacznie prob No-Go | |
| Prawidlowe odpowiedzi Go (trafienia) | |
| Pominiete odpowiedzi Go (chybienia) | |
| Odpowiedzi na No-Go (bledy komisji / falszywe alarmy) | |
| Prawidlowe powstrzymania No-Go (prawidlowe odrzucenia) | |
| Sredni czas reakcji w probach Go (ms) | |

## Krok 4: Oblicz wskaznik trafien i wskaznik falszywych alarmow

Uzywajac danych z Kroku 3:

```
Wskaznik trafien = Prawidlowe odpowiedzi Go / Lacznie prob Go
Wskaznik FA = Bledy komisji / Lacznie prob No-Go
```

Zapisz obie wartosci jako ulamki dziesietne (np. 0,88, nie 88%).

## Krok 5: Oblicz d'

Uzyj tabeli wartosci z w theory.pl.md, aby odczytac Z(wskaznik trafien) i Z(wskaznik FA).

```
d' = Z(wskaznik trafien) - Z(wskaznik FA)
```

Zapisz swoje d'. Porownaj z tabela interpretacji w theory.pl.md — co Twoje d' mowi o Twojej zdolnosci do rozrozniania Go od No-Go?

## Krok 6: Graj na poziomie Trudnym

Wrocz do menu sesji i wybierz poziom **Trudny** (60% Go, okno odpowiedzi 0,7 sekundy). Ukonczyj pelna sesje.

Po sesji zapisz te same miary co w Kroku 3. Oblicz wskaznik bledow komisji (wskaznik FA) i d' dla tej sesji.

**Pytania porownawcze:**
- Czy Twoj wskaznik bledow komisji wzrosl, spal, czy pozostal taki sam w porownaniu do poziomu Sredniego?
- Czy Twoje d' sie zmienilo? W ktora strone?
- Czy Twoj sredni czas reakcji w probach Go sie zmienil? Dlaczego moze tak byc?

## Krok 7: Pytania refleksyjne

Napisz krotkie odpowiedzi na ponizsze pytania — moga stanowic podstawe dyskusji grupowej:

1. Czy Twoje bledy komisji byly rownomiernie rozlozone przez sesje, czy skupialy sie pod koniec? Co moze to sugerowac o wyczerpaniu hamowania?
2. Jesli kolega/koleżanka miala 90% trafien i 20% wskaznik FA, a Ty 80% trafien i 5% wskaznik FA — kto ma wyzsze d'? Oblicz obydwa i porownaj.
3. Pacjent z uszkodzeniem platow czolowych wykazuje wiele bledow komisji, ale normalny czas reakcji w probach Go. Co ten wzorzec mowi nam o neuronalnym rozdzieleniu szybkosci odpowiedzi i hamowania odpowiedzi?
4. Zadanie Go/No-Go i zadanie Stroopa (jesli realizowales/as Lekcje 07) sa uzywane do pomiaru "funkcji wykonawczych". Na podstawie doswiadczenia z oboma: co jest podobne, a co rozne w wymaganiach poznawczych, ktore stawiaja?

## Pytania dyskusyjne

Przyniés swoje obliczone wartosci d' i wskazniki bledow komisji na dyskusje grupowa:

1. **Co odróznia blad komisji od bledu pominiecia?** Ktory z nich bardziej niepokoi klinicyste w kontekscie ADHD i dlaczego?
2. **Dwoje studentow osiaga 85% trafnosci. Czy jedno moze byc impulsywne, a drugie nieuważne?** Skonstruuj konkretny przyklad uzywajac wskaznikow trafien i falszywych alarmow.
3. **Dlaczego hamowanie odpowiedzi rozwija sie az do 25. roku zycia?** Jaka struktura mozgu jest zaangazowana i dlaczego jej dojrzewanie trwa tak dlugo?

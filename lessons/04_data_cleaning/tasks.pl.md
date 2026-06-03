# Zadania — Czyszczenie danych

Wykonaj poniższe kroki podczas lekcji. Użyj tego samego pliku CSV, który przeglądałeś w Lekcji 03, lub najpierw wygeneruj nowy plik sesji (zob. Lekcja 03, Krok 1).

## Krok 1: Policz próby

Otwórz plik CSV i policz łączną liczbę wierszy danych (z wyłączeniem nagłówka). To jest Twoje **N_total**.

- N_total: _______

## Krok 2: Zidentyfikuj antycypacje (RT < 100 ms)

Przejrzyj kolumnę `response_time_ms` w poszukiwaniu wartości mniejszych niż 100. W aplikacji arkuszowej możesz użyć filtru (Dane → Filtr), aby wyświetlić tylko wiersze, w których `response_time_ms < 100`.

- Liczba prób antycypacyjnych: _______
- Jeśli znalazłeś jakieś: zapisz najmniejszą zaobserwowaną wartość RT. _______ ms

## Krok 3: Zidentyfikuj przerwy uwagi (RT > 2000 ms)

Zastosuj filtr, aby wyświetlić wiersze, w których `response_time_ms > 2000`.

- Liczba prób z przerwami uwagi: _______
- Jeśli znalazłeś jakieś: zapisz największą zaobserwowaną wartość RT. _______ ms

## Krok 4: Zidentyfikuj przekroczenia limitu czasu (brakujące RT)

Zastosuj filtr, aby wyświetlić wiersze, w których `response_time_ms` jest puste lub zawiera `NA`/`NaN`.

- Liczba prób z przekroczeniem limitu czasu: _______

## Krok 5: Oblicz wskaźnik wykluczenia

Wypełnij tabelę:

| Kategoria | Liczba | % z N_total |
|---|---|---|
| Antycypacje (< 100 ms) | | |
| Przerwy uwagi (> 2000 ms) | | |
| Przekroczenia limitu czasu (brak odpowiedzi) | | |
| **Łącznie wykluczone** | | |
| **Włączone** | | |

Czy łączny wskaźnik wykluczenia jest powyżej, czy poniżej 5%? _______

## Krok 6: Napisz fragment kodu czyszczącego w Pythonie

Otwórz interpreter Pythona (lub nową komórkę w notatniku Jupyter) i wpisz poniższy kod. Zastąp `"twoj_plik.csv"` rzeczywistą ścieżką do Twojego pliku CSV:

```python
import pandas as pd

raw = pd.read_csv("twoj_plik.csv")

mask_anticipation = raw["response_time_ms"] < 100
mask_lapse        = raw["response_time_ms"] > 2000
mask_timeout      = raw["response_time_ms"].isna()

excluded = raw[mask_anticipation | mask_lapse | mask_timeout]
cleaned  = raw[~(mask_anticipation | mask_lapse | mask_timeout)]

print(f"Razem: {len(raw)} | Wykluczone: {len(excluded)} ({100*len(excluded)/len(raw):.1f}%) | Wlaczone: {len(cleaned)}")
```

Czy liczby zgadzają się z tym, co znalazłeś ręcznie w Krokach 2–5?

## Pytania dyskusyjne

Omów poniższe pytania w grupie lub dostarcz pisemne odpowiedzi zgodnie z instrukcją:

1. **Dlaczego ręczne usuwanie wierszy w Excelu nie jest akceptowalną metodą czyszczenia zbioru danych?** Co konkretnie jest tracone przy takim podejściu?
2. **Twój wskaźnik wykluczenia wynosi 0%. Czy Twoje dane są czyste?** Wyjaśnij, co mówi Ci 0% wskaźnik wykluczenia, a czego nie mówi.
3. **Wyobraź sobie, że 8% prób to przerwy uwagi w warunku niezgodnym, ale tylko 1% w warunku zgodnym.** Co ta asymetria mówi Ci poza wartościami średnich RT? Czy powinieneś ją zaraportować?

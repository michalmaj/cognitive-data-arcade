# Zadania — Brakujące wartości i wartości odstające

Wykonaj poniższe kroki, korzystając z pliku CSV z sesji gry. Każdy plik sesji jest odpowiedni; zalecane są pliki Stroopa, ponieważ są generowane automatycznie przez aplikację.

## Krok 1: Znajdź plik sesji gry

Pliki sesji gry są przechowywane w `data/generated/`. Uruchom poniższe polecenie, aby wylistować dostępne pliki:

```
ls data/generated/stroop/
```

Jeśli nie ma żadnych plików, zagraj jedną sesję gry Stroop (Lekcja 07) i wróć.

## Krok 2: Policz próby z timeoutem

Otwórz Pythona (lub notatnik Jupyter) i wczytaj plik:

```python
import pandas as pd

df = pd.read_csv("data/generated/stroop/TWOJ_PLIK.csv")
print(df.head())
print(df.columns.tolist())
```

Zidentyfikuj kolumnę wskazującą timeout lub brakującą odpowiedź (może nazywać się `response`, `rt`, `timeout` lub podobnie). Policz wiersze z timeoutem:

```python
# Dostosuj warunek do rzeczywistej nazwy kolumny
timeouty = df[df["response"].isna() | (df["rt"] == 0)]
print(f"Łącznie prób: {len(df)}")
print(f"Próby z timeoutem: {len(timeouty)}")
print(f"Odsetek: {len(timeouty) / len(df):.1%}")
```

**Zanotuj:** Ile jest timeoutów? W którym warunku (zgodny, neutralny, niezgodny) pojawiają się najczęściej?

## Krok 3: Oblicz odsetek brakujących odpowiedzi według warunku

```python
kolumna_warunku = "condition"   # dostosuj w razie potrzeby
kolumna_rt = "rt"

brakujace_na_warunek = df.groupby(kolumna_warunku)[kolumna_rt].apply(
    lambda x: x.isna().mean()
)
print(brakujace_na_warunek)
```

**Pytanie:** Czy wskaźniki timeoutów są podobne we wszystkich warunkach, czy jeden warunek jest znacznie gorszy? Co nierównomierny wzorzec mówi o mechanizmie braków (MCAR a MNAR)?

## Krok 4: Porównaj średnią i medianę RT

Najpierw pracuj z wszystkimi wierszami (w tym z wartościami odstającymi):

```python
prawidlowe = df[df["rt"].notna() & (df["rt"] > 0)]

print("=== Z wszystkimi prawidłowymi próbami ===")
print(prawidlowe.groupby(kolumna_warunku)["rt"].agg(["mean", "median", "std"]))
```

**Zanotuj** średnią i medianę dla każdego warunku. Czy średnia jest większa od mediany? O ile? Co ta różnica mówi o kształcie rozkładu RT?

## Krok 5: Zastosuj regułę wartości odstających opartą na z-score

```python
from scipy import stats
import numpy as np

prawidlowe = prawidlowe.copy()
prawidlowe["z_rt"] = stats.zscore(prawidlowe["rt"])

przed = len(prawidlowe)
czyste = prawidlowe[prawidlowe["z_rt"].abs() <= 3]
po = len(czyste)

print(f"Usunięto {przed - po} prób ({(przed - po) / przed:.1%}) przez regułę z-score")
print("\n=== Po wykluczeniu z-score ===")
print(czyste.groupby(kolumna_warunku)["rt"].agg(["mean", "median", "std"]))
```

**Porównaj** średnie przed i po wykluczeniu. Czy efekt Stroopa (średnie RT niezgodny − średnie RT zgodny) się zmienił? O ile?

## Krok 6: Zastosuj regułę granic fizjologicznych

```python
czyste_fiz = prawidlowe[(prawidlowe["rt"] >= 100) & (prawidlowe["rt"] <= 3000)]
usuniete = len(prawidlowe) - len(czyste_fiz)

print(f"Usunięto {usuniete} prób ({usuniete / len(prawidlowe):.1%}) przez regułę granic fizjologicznych")
print("\n=== Po wykluczeniu fizjologicznym ===")
print(czyste_fiz.groupby(kolumna_warunku)["rt"].agg(["mean", "median", "std"]))
```

**Porównaj** z podejściem opartym na z-score. Czy obie metody zgadzają się co do tego, które próby wykluczyć? Która usuwa więcej prób? Która jest lepiej uzasadniona i dlaczego?

## Pytania dyskusyjne

Omów poniższe pytania z grupą lub złóż pisemne odpowiedzi:

1. Czy w Twoim zbiorze danych próby z timeoutem są równomiernie rozłożone między warunkami? Co to implikuje o mechanizmie braków?
2. O ile zmieniła się średnia RT po zastosowaniu wykluczenia opartego na z-score? O ile zmieniła się mediana? Która statystyka była bardziej stabilna i dlaczego?
3. Kolega twierdzi: „Zawsze usuwam RT poniżej 200 ms i powyżej 2 000 ms — to działa dla moich danych." Oceń to podejście. W jakich okolicznościach jest trafne? Jakich informacji brakuje w tej regule?

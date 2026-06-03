# Zadania — Eksploracyjna analiza danych

Wykonaj poniższe kroki, korzystając z pliku CSV sesji Stroopa z `data/generated/stroop/`. Jeśli oczyszczałeś dane w Lekcji 05, użyj oczyszczonej wersji.

## Krok 1: Wczytaj i sprawdź zbiór danych

```python
import pandas as pd
import numpy as np

df = pd.read_csv("data/generated/stroop/TWOJ_PLIK.csv")

print("Wymiary:", df.shape)
print("\nTypy kolumn:")
print(df.dtypes)
print("\nPierwsze 5 wierszy:")
print(df.head())
print("\nOstatnie 5 wierszy:")
print(df.tail())
```

**Zanotuj:** Ile wierszy i kolumn? Czy liczba wierszy odpowiada oczekiwanej liczbie prób? Czy są kolumny z nieoczekiwanymi typami?

## Krok 2: Oblicz statystyki opisowe

```python
print(df.describe())
```

Sprawdź uważnie wyniki:
- Czy minimalne RT wygląda wiarygodnie (powinno być powyżej 100 ms)?
- Czy maksymalne RT wygląda wiarygodnie (powinno być poniżej ~3 000 ms)?
- Jakie jest ogólne średnie RT?

Teraz oblicz statystyki według warunków:

```python
kolumna_warunku = "condition"   # dostosuj do rzeczywistej nazwy kolumny
kolumna_rt = "rt"

statystyki = df.groupby(kolumna_warunku)[kolumna_rt].agg(
    liczba="count",
    srednia="mean",
    mediana="median",
    std="std",
    q25=lambda x: x.quantile(0.25),
    q75=lambda x: x.quantile(0.75),
    skosnosc=lambda x: x.skew(),
)
print(statystyki.round(1))
```

**Zanotuj:** Który warunek ma najwyższą średnią? Najwyższą medianę? Czy średnia i mediana są podobne, czy średnia znacznie przekracza medianę? Co mówi Ci wartość skośności?

## Krok 3: Narysuj rozkład RT

```python
import matplotlib.pyplot as plt

warunki = df[kolumna_warunku].unique()
fig, osie = plt.subplots(1, len(warunki), figsize=(12, 4), sharey=True)

for os, warunek in zip(osie, sorted(warunki)):
    dane = df[df[kolumna_warunku] == warunek][kolumna_rt].dropna()
    os.hist(dane, bins=30, edgecolor="black", color="steelblue", alpha=0.7)
    os.axvline(dane.mean(), color="red", linestyle="--", label=f"Srednia={dane.mean():.0f}")
    os.axvline(dane.median(), color="green", linestyle="-", label=f"Mediana={dane.median():.0f}")
    os.set_title(warunek)
    os.set_xlabel("RT (ms)")
    os.legend(fontsize=8)

osie[0].set_ylabel("Liczba")
plt.tight_layout()
plt.savefig("eda_histogramy.png", dpi=150)
plt.show()
```

**Obserwuj:** Czy rozkład jest prawostronnie skośny (długi prawy ogon)? Czy średnia (czerwona przerywana) leży na prawo od mediany (zielona ciągła)? Czy kształt różni się między warunkami?

## Krok 4: Narysuj wykres pudełkowy i skrzypcowy

```python
fig, osie = plt.subplots(1, 2, figsize=(10, 5))

# Wykres pudełkowy
df.boxplot(column=kolumna_rt, by=kolumna_warunku, ax=osie[0])
osie[0].set_title("Wykres pudełkowy")
osie[0].set_xlabel("Warunek")
osie[0].set_ylabel("RT (ms)")

# Wykres skrzypcowy (wymaga matplotlib >= 3.7 lub seaborn)
try:
    import seaborn as sns
    sns.violinplot(data=df, x=kolumna_warunku, y=kolumna_rt, ax=osie[1], inner="box")
    osie[1].set_title("Wykres skrzypcowy")
except ImportError:
    osie[1].text(0.5, 0.5, "Zainstaluj seaborn dla wykresu skrzypcowego",
                 ha="center", va="center")

plt.tight_layout()
plt.savefig("eda_pudelkowy_skrzypcowy.png", dpi=150)
plt.show()
```

**Obserwuj:** Czy mediany są w oczekiwanej kolejności (zgodny < neutralny < niezgodny)? Czy pudełka się nakładają? Czy widoczne są punkty wartości odstających poza wąsami?

## Krok 5: Sprawdź normalność za pomocą wykresu Q-Q

```python
from scipy import stats

prawidlowe_rt = df[kolumna_rt].dropna()
fig, os = plt.subplots(figsize=(5, 5))
stats.probplot(prawidlowe_rt, dist="norm", plot=os)
os.set_title("Wykres Q-Q — wszystkie warunki razem")
plt.tight_layout()
plt.savefig("eda_wykres_qq.png", dpi=150)
plt.show()
```

**Obserwuj:** Czy punkty leżą na diagonalnej linii, czy odchylają się od niej w prawym górnym rogu (co wskazuje na prawostronną skośność — długi ogon RT)? Co to mówi o zastosowaniu standardowego t-testu na surowym RT?

## Krok 6: Porównaj warunki i oblicz efekt Stroopa

```python
srednie_warunki = df.groupby(kolumna_warunku)[kolumna_rt].mean()
print("Srednie wedlug warunków:")
print(srednie_warunki.round(1))

if "incongruent" in srednie_warunki and "congruent" in srednie_warunki:
    efekt_stroopa = srednie_warunki["incongruent"] - srednie_warunki["congruent"]
    print(f"\nEfekt Stroopa (srednia): {efekt_stroopa:.1f} ms")

mediany_warunki = df.groupby(kolumna_warunku)[kolumna_rt].median()
if "incongruent" in mediany_warunki and "congruent" in mediany_warunki:
    efekt_stroopa_mediana = mediany_warunki["incongruent"] - mediany_warunki["congruent"]
    print(f"Efekt Stroopa (mediana): {efekt_stroopa_mediana:.1f} ms")
```

**Porównaj:** Czy efekt Stroopa jest większy obliczony ze średnich czy z median? Któremu bardziej ufasz i dlaczego?

## Pytania dyskusyjne

1. Spójrz na swoje histogramy z Kroku 3. Czy rozkład RT w warunku niezgodnym jest po prostu przesunięty w prawo względem zgodnego, czy ma też inny kształt? Co by oznaczało, gdyby kształt był inny?
2. Wykres Q-Q pokazał odchylenie od normalności. Czy to oznacza, że nie możesz analizować danych statystycznie? Jakie istnieją alternatywy?
3. Na podstawie Twojej EDA sformułuj jedną konkretną, testowalną hipotezę dotyczącą efektu Stroopa w Twoich danych. Upewnij się, że hipoteza jest postawiona *przed* wykonaniem jakiegokolwiek testu wnioskowego.

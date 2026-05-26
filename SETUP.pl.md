# Przewodnik instalacji — Cognitive Data Arcade

Niniejszy przewodnik opisuje instalację i uruchomienie Cognitive Data Arcade na systemach Windows, macOS i Linux.

---

## Wymagania

- **Python 3.12 lub nowszy** — pobierz ze strony [python.org](https://www.python.org/downloads/)
- **uv** — szybki menedżer pakietów Python
- **git** — do sklonowania repozytorium

---

## Instalacja

### Krok 1: Zainstaluj uv

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Po instalacji należy zamknąć terminal i otworzyć go ponownie, a następnie sprawdzić:

```bash
uv --version
```

### Krok 2: Sklonuj repozytorium

```bash
git clone https://github.com/michalmaj/cognitive-data-arcade.git
cd cognitive-data-arcade
```

### Krok 3: Zainstaluj zależności

```bash
uv sync
```

Pobiera wszystkie wymagane pakiety. Przy pierwszym uruchomieniu może to potrwać 1–2 minuty.

---

## Uruchamianie aplikacji

```bash
uv run cognitive-data-arcade
```

Pojawi się okno z menu lekcji. Użyj **klawiszy strzałek** do nawigacji i **ENTER**, aby uruchomić lekcję.

---

## Aktualizacja

Gdy dostępna jest nowa wersja:

```bash
git pull
uv sync
```

---

## Rozwiązywanie problemów

### `uv: command not found`

Instalacja `uv` nie zaktualizowała zmiennej systemowej PATH. Należy całkowicie zamknąć terminal, otworzyć go ponownie i spróbować jeszcze raz. Na Windows należy ponownie uruchomić sesję PowerShell. Jeśli problem się powtarza, postępuj zgodnie z instrukcjami ścieżki ręcznej w dokumentacji uv.

### Czarny ekran na Linux

Niektóre konfiguracje wyświetlacza Linux wymagają jawnego ustawienia sterownika wideo. Uruchom:

```bash
SDL_VIDEODRIVER=x11 uv run cognitive-data-arcade
```

Jeśli aplikacja uruchomi się, dodaj `export SDL_VIDEODRIVER=x11` do pliku `~/.bashrc` lub `~/.zshrc`.

### `ModuleNotFoundError` podczas uruchamiania

Zależności nie zostały zainstalowane. Uruchom `uv sync` w katalogu projektu, a następnie spróbuj jeszcze raz.

### Wolne uruchamianie przy pierwszym uruchomieniu

Pierwsze uruchomienie pobiera i instaluje pakiety do lokalnego środowiska wirtualnego. To jest normalne i trwa 1–2 minuty. Kolejne uruchomienia start w ciągu kilku sekund.

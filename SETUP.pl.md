# Przewodnik instalacji — Cognitive Data Arcade

Niniejszy przewodnik opisuje instalację i uruchomienie Cognitive Data Arcade na systemach Windows, macOS i Linux.

---

## Opcja A — Pobierz gotową aplikację (zalecane dla studentów)

Nie wymaga Pythona ani terminala.

1. Przejdź na [stronę Releases](https://github.com/michalmaj/cognitive-data-arcade/releases/latest)
2. Pobierz plik odpowiedni dla Twojego systemu:
   - **Windows** → `CognitiveDataArcade-windows.exe`
   - **macOS** → `CognitiveDataArcade-macos`
   - **Linux** → `CognitiveDataArcade-linux`
3. Umieść plik obok folderu `assets/` (zapytaj prowadzącego o paczkę z zasobami)
4. Uruchom:
   - **Windows** — kliknij dwukrotnie plik `.exe`
   - **macOS** — otwórz terminal, wpisz `chmod +x CognitiveDataArcade-macos`, następnie `./CognitiveDataArcade-macos`
   - **Linux** — otwórz terminal, wpisz `chmod +x CognitiveDataArcade-linux`, następnie `./CognitiveDataArcade-linux`

> **Uwaga dla macOS:** Przy pierwszym uruchomieniu może pojawić się ostrzeżenie systemowe. Przejdź do Ustawień systemowych → Prywatność i bezpieczeństwo → kliknij „Otwórz mimo to".

### Wymagana struktura katalogu

Plik wykonywalny i folder `assets/` muszą znajdować się w **tym samym katalogu**:

```
moj-folder/
  CognitiveDataArcade        ← plik wykonywalny
  assets/                    ← dostarcza prowadzący
    audio/
    badges/
    fonts/
    images/
```

Dane użytkownika (wyniki sesji, profil) są zapisywane do `~/.cognitive_data_arcade` — nie muszą być w tym folderze.

---

## Opcja B — Uruchomienie ze źródła (deweloperzy / zaawansowani użytkownicy)

### Wymagania

- **Python 3.12 lub nowszy** — pobierz ze strony [python.org](https://www.python.org/downloads/)
- **uv** — szybki menedżer pakietów Python
- **git** — do sklonowania repozytorium

---

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

Pierwsze uruchomienie pobiera i instaluje pakiety do lokalnego środowiska wirtualnego. To jest normalne i trwa 1–2 minuty. Kolejne uruchomienia startują w ciągu kilku sekund.

---

## Opcja C — Samodzielne budowanie pliku wykonywalnego

Dla prowadzących lub deweloperów, którzy chcą samodzielnie zbudować nową wersję pliku wykonywalnego ze źródeł.

### Wymagania

- Wszystkie wymagania Opcji B (Python 3.12, uv, git)
- Kompilator C:
  - **Windows** — Visual Studio Build Tools
  - **macOS** — Xcode Command Line Tools (`xcode-select --install`)
  - **Linux** — `gcc` (zwykle preinstalowany; jeśli brak: `sudo apt install gcc`)

### Komenda do budowania

```bash
bash scripts/build.sh
```

Tworzy plik `dist/CognitiveDataArcade` (lub `.exe` na Windows).

### Weryfikacja przed dystrybucją

```bash
mkdir /tmp/cda-test
cp dist/CognitiveDataArcade /tmp/cda-test/
cp -r assets/ /tmp/cda-test/
cd /tmp/cda-test && ./CognitiveDataArcade
```

Aplikacja musi uruchamiac sie z pustego katalogu, ktory nie jest katalogiem repozytorium. Jesli poprawnie laduje zasoby i otwiera menu, build jest gotowy do dystrybucji.

### Co jest dystrybuowane

```
CognitiveDataArcade        ← zbudowany przez skrypt
assets/                    ← skopiowany z repozytorium
```

Dane uzytkownika sa zapisywane do `~/.cognitive_data_arcade` i nigdy nie sa przechowywane w folderze `assets/`.

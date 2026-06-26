# Setup Guide — Cognitive Data Arcade

This guide covers how to install and run the Cognitive Data Arcade on Windows, macOS, and Linux.

---

## Option A — Download the standalone app (recommended for students)

No Python or terminal required.

1. Go to the [Releases page](https://github.com/michalmaj/cognitive-data-arcade/releases/latest)
2. Download the file for your system:
   - **Windows** → `CognitiveDataArcade-windows.exe`
   - **macOS** → `CognitiveDataArcade-macos`
   - **Linux** → `CognitiveDataArcade-linux`
3. Place the file next to the `assets/` folder (ask your instructor for the assets package)
4. Run it:
   - **Windows** — double-click the `.exe` file
   - **macOS** — open a terminal, `chmod +x CognitiveDataArcade-macos`, then `./CognitiveDataArcade-macos`
   - **Linux** — open a terminal, `chmod +x CognitiveDataArcade-linux`, then `./CognitiveDataArcade-linux`

> **macOS note:** The first launch may show a security warning. Go to System Settings → Privacy & Security → click "Open Anyway".

---

## Option B — Run from source (developers / advanced users)

### Requirements

- **Python 3.12 or newer** — download from [python.org](https://www.python.org/downloads/)
- **uv** — a fast Python package manager
- **git** — for cloning the repository

---

### Step 1: Install uv

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, close and reopen the terminal, then verify:

```bash
uv --version
```

### Step 2: Clone the repository

```bash
git clone https://github.com/michalmaj/cognitive-data-arcade.git
cd cognitive-data-arcade
```

### Step 3: Install dependencies

```bash
uv sync
```

This downloads all required packages. On the first run, it may take 1–2 minutes.

---

## Running the App

```bash
uv run cognitive-data-arcade
```

A window appears with the lesson menu. Use **arrow keys** to navigate and **ENTER** to launch a lesson.

---

## Updating

When a new version is available:

```bash
git pull
uv sync
```

---

## Troubleshooting

### `uv: command not found`

The `uv` installation did not update the system PATH. Close the terminal completely, reopen it, and try again. On Windows, restart the PowerShell session. If the problem persists, follow the manual PATH instructions in the uv documentation.

### Black screen on Linux

Some Linux display configurations require an explicit video driver setting. Run:

```bash
SDL_VIDEODRIVER=x11 uv run cognitive-data-arcade
```

If the app starts, add `export SDL_VIDEODRIVER=x11` to `~/.bashrc` or `~/.zshrc`.

### `ModuleNotFoundError` on startup

The dependencies were not installed. Run `uv sync` in the project directory, then try again.

### Slow startup on the first run

The first run downloads and installs packages into a local virtual environment. This is normal and takes 1–2 minutes. Subsequent runs start within a few seconds.

#!/usr/bin/env python3
"""
Generate placeholder ambient background music for Cognitive Data Arcade.
Creates WAV files in assets/audio/music/ using numpy (already a project dependency).

Usage (run once after cloning, from the project root):
    python scripts/generate_audio.py

To use real music instead: drop OGG or MP3 files named menu.ogg / game.ogg
into assets/audio/music/ — they take priority over the generated WAVs.
"""
from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

DEST = Path("assets") / "audio" / "music"
SAMPLE_RATE = 44100
DURATION_S = 32  # seamless loop length


def _ambient_pad(root_hz: float, sr: int = SAMPLE_RATE, duration_s: int = DURATION_S) -> np.ndarray:
    n = int(sr * duration_s)
    t = np.linspace(0, duration_s, n, endpoint=False)

    # Fundamental + first three harmonics for a warm pad timbre
    sig = (
        0.30 * np.sin(2 * np.pi * root_hz * t)
        + 0.15 * np.sin(2 * np.pi * root_hz * 2 * t)
        + 0.08 * np.sin(2 * np.pi * root_hz * 3 * t)
        + 0.04 * np.sin(2 * np.pi * root_hz * 4 * t)
    )

    # Slow tremolo (0.2 Hz) for movement
    sig *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.2 * t)

    # 1-second crossfade at both ends for seamless looping
    fade = sr
    env = np.ones(n)
    env[:fade] = np.linspace(0.0, 1.0, fade)
    env[-fade:] = np.linspace(1.0, 0.0, fade)
    sig *= env

    # Normalise to 50 % full scale, convert to int16 stereo
    peak = np.max(np.abs(sig)) or 1.0
    mono = (sig / peak * 0.5 * 32767).astype(np.int16)
    return np.column_stack([mono, mono])


def _write_wav(path: Path, data: np.ndarray, sr: int = SAMPLE_RATE) -> None:
    with wave.open(str(path), "w") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes(data.tobytes())


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)

    # menu: A2 (110 Hz) — gentle, calming
    # game: C#3 (138.6 Hz) — slightly brighter, focused
    tracks = {"menu": 110.0, "game": 138.6}

    for name, freq in tracks.items():
        ogg = DEST / f"{name}.ogg"
        mp3 = DEST / f"{name}.mp3"
        wav = DEST / f"{name}.wav"

        if ogg.exists() or mp3.exists():
            print(f"  {name}: OGG/MP3 already present, skipping")
            continue
        if wav.exists():
            print(f"  {name}.wav already exists, skipping")
            continue

        print(f"  Generating {wav} …", end=" ", flush=True)
        _write_wav(wav, _ambient_pad(freq))
        print(f"{wav.stat().st_size // 1024} KB")

    print("\nDone.  Replace WAV files with OGG/MP3 tracks for better music quality.")


if __name__ == "__main__":
    main()

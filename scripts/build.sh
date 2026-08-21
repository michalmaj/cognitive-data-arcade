#!/usr/bin/env bash
# Build a standalone Cognitive Data Arcade executable with Nuitka.
#
# Usage:
#   bash scripts/build.sh                   # builds for the host platform
#   bash scripts/build.sh --output-dir dist # override output directory
#
# Prerequisites:
#   uv add --dev nuitka        (one-time)
#   A C compiler: gcc / clang / MSVC
#
# Output:
#   dist/CognitiveDataArcade[.exe]   — the standalone executable
#
# Distribution:
#   Ship the executable + the project's assets/ directory together.
#   The app resolves assets relative to the executable, so the layout must be:
#
#     CognitiveDataArcade        (or .exe on Windows)
#     assets/
#       audio/
#       badges/
#       fonts/
#       images/
#
# User data (profile.json, generated CSVs) is written to ~/.cognitive_data_arcade
# and never inside the assets/ directory.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${1:---output-dir}"
if [[ "$OUTPUT_DIR" == "--output-dir" ]]; then
    # No argument supplied: default to dist/
    OUTPUT_DIR="$REPO_ROOT/dist"
fi

mkdir -p "$OUTPUT_DIR"

echo "Building Cognitive Data Arcade → $OUTPUT_DIR"
echo "Repository root: $REPO_ROOT"

# Install nuitka into the project venv if not already present
uv run --with nuitka python -c "import nuitka" 2>/dev/null \
    || uv add --dev nuitka

uv run python -m nuitka \
    --onefile \
    --output-dir="$OUTPUT_DIR" \
    --output-filename=CognitiveDataArcade \
    --follow-imports \
    --include-package=cognitive_data_arcade \
    --include-package=pygame \
    --include-package=pandas \
    --include-package=matplotlib \
    --include-package=numpy \
    --include-package=sklearn \
    --include-package=scipy \
    --nofollow-import-to=tkinter \
    --assume-yes-for-downloads \
    -o "$OUTPUT_DIR/CognitiveDataArcade" \
    src/cognitive_data_arcade/__main__.py

echo ""
echo "Build complete: $OUTPUT_DIR/CognitiveDataArcade"
echo ""
echo "To distribute, copy the executable and the assets/ directory together:"
echo "  $OUTPUT_DIR/CognitiveDataArcade"
echo "  $REPO_ROOT/assets/  →  place next to the executable"
echo ""
echo "Verify the build works from an empty directory:"
echo "  mkdir /tmp/cda-test && cp $OUTPUT_DIR/CognitiveDataArcade /tmp/cda-test/"
echo "  cp -r $REPO_ROOT/assets/ /tmp/cda-test/"
echo "  cd /tmp/cda-test && ./CognitiveDataArcade"

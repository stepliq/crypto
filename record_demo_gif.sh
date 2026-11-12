#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /path/to/lab_with_demo.sh" >&2
  exit 1
fi

LAB_DIR="${1%/}"
LAB_DIR="$(cd "$LAB_DIR" && pwd)"
DEMO_SCRIPT="$LAB_DIR/demo.sh"

if [[ ! -f "$DEMO_SCRIPT" ]]; then
  echo "Missing: $DEMO_SCRIPT" >&2
  exit 1
fi

LAB_NAME="$(basename "$LAB_DIR")"
CAST="${CAST:-$LAB_DIR/$LAB_NAME.cast}"
GIF="${GIF:-$LAB_DIR/$LAB_NAME.gif}"
TITLE="${TITLE:-$LAB_NAME demo}"

export LAB_DEMO_PAUSE="${LAB_DEMO_PAUSE:-2.5}"

AGG_SPEED="${AGG_SPEED:-0.3}"
AGG_THEME="${AGG_THEME:-asciinema}"
AGG_LAST_FRAME="${AGG_LAST_FRAME:-8}"

AGG="${AGG:-$HOME/.cargo/bin/agg}"
if [[ ! -x "$AGG" ]]; then
  AGG="$(command -v agg 2>/dev/null || true)"
fi
if [[ -z "${AGG:-}" || ! -x "$AGG" ]]; then
  echo "agg not found. Install: cargo install --git https://github.com/asciinema/agg" >&2
  exit 1
fi

cd "$LAB_DIR"

echo "Lab: $LAB_DIR"
echo "Recording: $CAST (LAB_DEMO_PAUSE=$LAB_DEMO_PAUSE s)"
export LAB_DEMO_PAUSE
# asciinema 3.x: no -y; prefer asciicast-v2 for agg compatibility
asciinema record "$CAST" \
  --overwrite \
  -q \
  -f asciicast-v2 \
  -t "$TITLE" \
  -c "bash \"$DEMO_SCRIPT\"" \
  --headless \
  --window-size 100x30

echo "GIF: $GIF (agg --speed $AGG_SPEED)"
"$AGG" "$CAST" "$GIF" \
  --speed "$AGG_SPEED" \
  --theme "$AGG_THEME" \
  --last-frame-duration "$AGG_LAST_FRAME" \
  -q

echo "Done: $CAST + $GIF"

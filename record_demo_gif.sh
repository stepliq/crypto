#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Использование: $0 /путь/к/папке_с_demo.sh" >&2
  exit 1
fi

LAB_DIR="${1%/}"
LAB_DIR="$(cd "$LAB_DIR" && pwd)"
DEMO_SCRIPT="$LAB_DIR/demo.sh"

if [[ ! -f "$DEMO_SCRIPT" ]]; then
  echo "Нет файла: $DEMO_SCRIPT" >&2
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
  echo "Не найден agg. Установка: cargo install --git https://github.com/asciinema/agg" >&2
  exit 1
fi

cd "$LAB_DIR"

echo "Лабораторная: $LAB_DIR"
echo "Запись: $CAST (паузы LAB_DEMO_PAUSE=$LAB_DEMO_PAUSE с)"
export LAB_DEMO_PAUSE
asciinema rec "$CAST" --overwrite -y -q -t "$TITLE" -c "bash \"$DEMO_SCRIPT\""

echo "GIF: $GIF (agg --speed $AGG_SPEED)"
"$AGG" "$CAST" "$GIF" \
  --speed "$AGG_SPEED" \
  --theme "$AGG_THEME" \
  --last-frame-duration "$AGG_LAST_FRAME" \
  -q

echo "Готово: $CAST + $GIF"

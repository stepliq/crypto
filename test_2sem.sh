#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ -x .venv/bin/python ]]; then
  PY=.venv/bin/python
else
  echo "missing .venv — create it first:" >&2
  echo "  python3 -m venv .venv" >&2
  echo "  .venv/bin/pip install -r 2sem/lab1/requirements.txt -r 2sem/lab2/requirements.txt -r 2sem/lab3/requirements.txt -r 2sem/lab4/requirements.txt pytest" >&2
  exit 1
fi

exec "$PY" -m pytest 2sem/lab1 2sem/lab2 2sem/lab3 2sem/lab4 -v --tb=short "$@"

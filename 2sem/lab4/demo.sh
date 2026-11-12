#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

REPO_ROOT="$(cd ../.. && pwd)"
if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
  PY="${REPO_ROOT}/.venv/bin/python"
else
  PY="${PYTHON:-python3}"
fi

_demo_pause() {
  [[ -z "${LAB_DEMO_PAUSE:-}" ]] || sleep "${LAB_DEMO_PAUSE}"
}

echo ""
echo "=== Lab 2.4, Diffie-Hellman key distribution ==="
echo ""
_demo_pause

echo ""
echo "$ $PY keydist_lab.py -v --help"
"$PY" keydist_lab.py -v --help
echo ""
_demo_pause

SEED=$(date +%s)

echo "1. Generate keys for N users"
echo ""
echo "$ $PY keydist_lab.py setup -n 4 --seed $SEED"
"$PY" keydist_lab.py setup -n 4 --seed "$SEED"
echo ""
_demo_pause

echo "2. Shared key for a pair, with steps"
echo ""
echo "$ $PY keydist_lab.py pair U1 U3 -n 4 --seed $SEED"
"$PY" keydist_lab.py pair U1 U3 -n 4 --seed "$SEED"
echo ""
_demo_pause

echo "3. Another pair"
echo ""
echo "$ $PY keydist_lab.py pair U2 U4 -n 4 --seed $SEED"
"$PY" keydist_lab.py pair U2 U4 -n 4 --seed "$SEED"
echo ""
_demo_pause

echo "full demo"
echo ""
echo "$ $PY keydist_lab.py demo"
"$PY" keydist_lab.py demo
echo ""
_demo_pause

echo "tests"
echo ""
echo "$ $PY -m pytest test_keydist_lab.py -v --tb=short"
"$PY" -m pytest test_keydist_lab.py -v --tb=short

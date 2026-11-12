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
echo "=== Lab 2.1, PKI trust chains ==="
echo ""
_demo_pause

echo ""
echo "$ $PY pki_lab.py -v --help"
"$PY" pki_lab.py -v --help
echo ""
_demo_pause

echo "1. Hierarchical PKI"
echo ""
echo "$ $PY pki_lab.py hierarchical --leaf Alice"
"$PY" pki_lab.py hierarchical --leaf Alice
echo ""
_demo_pause

echo "2. Network PKI"
echo ""
echo "$ $PY pki_lab.py network --anchor CA1 --target Bob"
"$PY" pki_lab.py network --anchor CA1 --target Bob
echo ""
_demo_pause

echo "both variants"
echo ""
echo "$ $PY pki_lab.py demo"
"$PY" pki_lab.py demo
echo ""
_demo_pause

echo "tests"
echo ""
echo "$ $PY -m pytest test_pki_lab.py -v --tb=short"
"$PY" -m pytest test_pki_lab.py -v --tb=short

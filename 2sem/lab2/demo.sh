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
echo "=== Lab 2.2, elliptic curves ==="
echo ""
_demo_pause

echo ""
echo "$ $PY ecc_lab.py -v --help"
"$PY" ecc_lab.py -v --help
echo ""
_demo_pause

echo "1. Residue mult table, P=7"
echo ""
echo "$ $PY ecc_lab.py mult-table 7"
"$PY" ecc_lab.py mult-table 7
echo ""
_demo_pause

echo "2. Element orders / generators, P=7"
echo ""
echo "$ $PY ecc_lab.py orders-mod 7"
"$PY" ecc_lab.py orders-mod 7
echo ""
_demo_pause

echo "3. Scalar multiplication"
echo ""
echo "$ $PY ecc_lab.py scalar"
"$PY" ecc_lab.py scalar
echo ""
_demo_pause

echo "4. EC group law over F7"
echo ""
echo "$ $PY ecc_lab.py ec-table"
"$PY" ecc_lab.py ec-table
echo ""
_demo_pause

echo "5. EC point orders"
echo ""
echo "$ $PY ecc_lab.py ec-orders"
"$PY" ecc_lab.py ec-orders
echo ""
_demo_pause

echo "tests"
echo ""
echo "$ $PY -m pytest test_ecc_lab.py -v --tb=short"
"$PY" -m pytest test_ecc_lab.py -v --tb=short

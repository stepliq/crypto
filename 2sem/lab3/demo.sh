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
echo "=== Lab 2.3, MAC / HMAC ==="
echo ""
_demo_pause

echo ""
echo "$ $PY mac_lab.py -v --help"
"$PY" mac_lab.py -v --help
echo ""
_demo_pause

echo "1. HMAC-SHA256"
echo ""
echo "$ $PY mac_lab.py tag "transfer 100 to Bob" --key demo-secret-key"
TAG=$("$PY" mac_lab.py tag "transfer 100 to Bob" --key demo-secret-key)
echo "$TAG"
echo "$ $PY mac_lab.py verify "transfer 100 to Bob" <tag> --key demo-secret-key"
"$PY" mac_lab.py verify "transfer 100 to Bob" "$TAG" --key demo-secret-key
echo ""
_demo_pause

echo "2. File integrity"
mkdir -p samples
for i in 1 2 3 4 5; do
  echo "demo content $i" > "samples/file$i.txt"
done
echo ""
echo "$ $PY mac_lab.py protect samples/file*.txt"
"$PY" mac_lab.py protect samples/file1.txt samples/file2.txt samples/file3.txt samples/file4.txt samples/file5.txt
echo ""
echo "$ $PY mac_lab.py check"
"$PY" mac_lab.py check
echo ""
echo "tamper samples/file1.txt, expect FAIL"
echo TAMPERED > samples/file1.txt
set +e
"$PY" mac_lab.py check
set -e
echo ""
echo "restore samples/file1.txt after demo"
echo "demo content 1" > samples/file1.txt
"$PY" mac_lab.py protect samples/file1.txt samples/file2.txt samples/file3.txt samples/file4.txt samples/file5.txt >/dev/null
echo ""
_demo_pause

echo "tests"
echo ""
echo "$ $PY -m pytest test_mac_lab.py -v --tb=short"
"$PY" -m pytest test_mac_lab.py -v --tb=short

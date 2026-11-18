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
echo "=== Лабораторная 5, SHA-256 и парадокс дней рождения ==="
echo ""
_demo_pause

echo ""
echo '$ $PY hash_lab.py -v --help'
"$PY" hash_lab.py -v --help
echo ""
_demo_pause

echo "Задача 1. Полный хеш SHA-256"
echo ""
echo '$ $PY hash_lab.py hash-hex "lab5"'
"$PY" hash_lab.py hash-hex "lab5"
echo '$ $PY hash_lab.py hash-hex "Hash functions lab5 demo text."'
"$PY" hash_lab.py hash-hex "Hash functions lab5 demo text."
echo ""
_demo_pause

echo "Задача 2. Усеченный хеш: берем только первые биты"
echo ""
echo '$ $PY hash_lab.py truncate "collision" --bits 32'
"$PY" hash_lab.py truncate "collision" --bits 32
echo ""
_demo_pause

echo "Задача 3. Парадокс дней рождения для усеченного хеша"
echo "Покажем на bits=20, что коллизия находится намного раньше, чем 2^20 переборов"
echo ""
echo '$ $PY hash_lab.py birthday-search --bits 20'
"$PY" hash_lab.py birthday-search --bits 20
echo ""
_demo_pause

echo "Встроенное демо с подробным пояснением"
echo ""
echo '$ $PY hash_lab.py demo'
"$PY" hash_lab.py demo
echo ""
_demo_pause

echo "Запускаем тесты"
echo ""
echo '$ $PY -m pytest test_hash_lab.py -v --tb=short'
"$PY" -m pytest test_hash_lab.py -v --tb=short

echo ""
_demo_pause
echo "Готово"

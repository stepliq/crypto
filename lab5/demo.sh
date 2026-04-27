#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

_demo_pause() {
  [[ -z "${LAB_DEMO_PAUSE:-}" ]] || sleep "${LAB_DEMO_PAUSE}"
}

echo ""
echo "=== Лабораторная 5, SHA-256 и парадокс дней рождения ==="
echo ""
_demo_pause

echo ""
echo '$ python3 hash_lab.py -v --help'
python3 hash_lab.py -v --help
echo ""
_demo_pause

echo "Задача 1. Полный хеш SHA-256"
echo ""
echo '$ python3 hash_lab.py hash-hex "lab5"'
python3 hash_lab.py hash-hex "lab5"
echo '$ python3 hash_lab.py hash-hex "Hash functions lab5 demo text."'
python3 hash_lab.py hash-hex "Hash functions lab5 demo text."
echo ""
_demo_pause

echo "Задача 2. Усеченный хеш: берем только первые биты"
echo ""
echo '$ python3 hash_lab.py truncate "collision" --bits 32'
python3 hash_lab.py truncate "collision" --bits 32
echo ""
_demo_pause

echo "Задача 3. Парадокс дней рождения для усеченного хеша"
echo "Покажем на bits=20, что коллизия находится намного раньше, чем 2^20 переборов"
echo ""
echo '$ python3 hash_lab.py birthday-search --bits 20'
python3 hash_lab.py birthday-search --bits 20
echo ""
_demo_pause

echo "Встроенное демо с подробным пояснением"
echo ""
echo '$ python3 hash_lab.py demo'
python3 hash_lab.py demo
echo ""
_demo_pause

echo "Запускаем тесты"
echo ""
echo '$ python3 -m pytest test_hash_lab.py -v --tb=short'
python3 -m pytest test_hash_lab.py -v --tb=short

echo ""
_demo_pause
echo "Готово"

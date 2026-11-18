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
echo "=== Лабораторная 6, быстрое возведение в степень по модулю ==="
echo ""
_demo_pause

echo ""
echo '$ $PY modexp_lab.py -v --help'
"$PY" modexp_lab.py -v --help
echo ""
_demo_pause

echo "Задача 1. Считаем a^x mod p быстрым алгоритмом + счётчик умножений"
echo ""
echo '$ $PY modexp_lab.py compute 5 701 11'
"$PY" modexp_lab.py compute 5 701 11
echo ""
_demo_pause

echo "Задача 2. Подробная трассировка вычисления Y = 5^701 mod 11"
echo ""
echo '$ $PY modexp_lab.py trace 5 701 11'
"$PY" modexp_lab.py trace 5 701 11
echo ""
_demo_pause

echo "Ещё один пример для самопроверки: Y = 3^800 mod 13"
echo ""
echo '$ $PY modexp_lab.py trace 3 800 13'
"$PY" modexp_lab.py trace 3 800 13
echo ""
_demo_pause

echo "Задача 3. Разный вес Хэмминга при одинаковой длине показателя (32 бита)"
echo ""
echo '$ $PY modexp_lab.py hamming-demo --bits 32'
"$PY" modexp_lab.py hamming-demo --bits 32
echo ""
_demo_pause

echo "Сравнение быстрого и медленного алгоритма (медленный считаем только для маленького x)"
echo ""
echo '$ $PY modexp_lab.py compare 7 200 1000'
"$PY" modexp_lab.py compare 7 200 1000
echo ""
_demo_pause

echo "Запускаем тесты"
echo ""
echo '$ $PY -m pytest test_modexp_lab.py -v --tb=short'
"$PY" -m pytest test_modexp_lab.py -v --tb=short

echo ""
_demo_pause
echo "Готово"

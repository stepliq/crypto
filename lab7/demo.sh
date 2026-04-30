#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

_demo_pause() {
  [[ -z "${LAB_DEMO_PAUSE:-}" ]] || sleep "${LAB_DEMO_PAUSE}"
}

echo ""
echo "=== Лабораторная 7, дискретный логарифм: перебор и метод Шэнкса ==="
echo ""
_demo_pause

echo ""
echo '$ python3 dlog_lab.py -v --help'
python3 dlog_lab.py -v --help
echo ""
_demo_pause

echo "Задача 1. Метод Шэнкса (BSGS) с подробной трассировкой"
echo "Параметры m и k программа выбирает автоматически: m = ceil(sqrt(n)), k подобрано так, что m*k >= n"
echo ""
echo '$ python3 dlog_lab.py bsgs 2 22 29'
python3 dlog_lab.py bsgs 2 22 29
echo ""
_demo_pause

echo "Задача 2. Тот же логарифм полным перебором"
echo ""
echo '$ python3 dlog_lab.py brute 2 22 29'
python3 dlog_lab.py brute 2 22 29
echo ""
_demo_pause

echo "Задача 3. Сравнение числа умножений на маленьком p"
echo ""
echo '$ python3 dlog_lab.py compare 2 22 29'
python3 dlog_lab.py compare 2 22 29
echo ""
_demo_pause

echo "Сравнение на большом p (секретный x = 54321, y = 2^54321 mod 100003)"
echo ""
echo '$ python3 dlog_lab.py compare 2 56246 100003'
python3 dlog_lab.py compare 2 56246 100003
echo ""
_demo_pause

echo "Зависимость числа умножений от величины искомого x (BSGS почти не зависит, перебор зависит)"
echo ""
echo '$ python3 dlog_lab.py demo'
python3 dlog_lab.py demo
echo ""
_demo_pause

echo "Запускаем тесты"
echo ""
echo '$ python3 -m pytest test_dlog_lab.py -v --tb=short'
python3 -m pytest test_dlog_lab.py -v --tb=short

echo ""
_demo_pause
echo "Готово"

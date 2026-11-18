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
echo "=== Лабораторная 1, шифр Цезаря ==="
echo ""
_demo_pause

echo ""
echo '$ $PY caesar.py -v --help'
"$PY" caesar.py -v --help
echo ""
_demo_pause

echo "Шифртекст Khoor в заданиях 2, 3 и 4 это слово Hello с ключом 3"
echo ""
_demo_pause

echo "Задание 1. Шифрование и расшифрование, латинские буквы, ключ от 0 до 25"
echo "Шифруем фразу ключом 7 и расшифровываем полученный шифртекст тем же ключом"
echo ""
echo '$ $PY caesar.py -v encrypt "Attack at dawn" -k 7'
"$PY" caesar.py -v encrypt "Attack at dawn" -k 7
echo '$ $PY caesar.py -v decrypt "Haahjr ha khdu" -k 7'
"$PY" caesar.py -v decrypt "Haahjr ha khdu" -k 7
echo ""
_demo_pause

echo "Задание 2. Атака по известному открытому тексту, на входе пара открытый текст и шифртекст"
echo "На выходе программа печатает одно число это найденный ключ сдвига от 0 до 25"
echo ""
echo '$ $PY caesar.py -v kpa --plain "Hello" --cipher "Khoor"'
"$PY" caesar.py -v kpa --plain "Hello" --cipher "Khoor"
echo "Тройка это тот самый ключ 3 на столько позиций вперёд сдвинута каждая буква при шифровании Hello в Khoor"
echo ""
_demo_pause

echo "Задание 3. Атака только по шифртексту, печатаются все 26 вариантов расшифрования для ключей от 0 до 25"
echo ""
echo '$ $PY caesar.py -v brute "Khoor"'
"$PY" caesar.py -v brute "Khoor"
echo ""
_demo_pause

echo "Задание 4. Снова только шифртекст, ключ подбирается по словарю автоматически"
echo "Выбирается вариант с наибольшим числом слов из словаря"
echo ""
echo '$ $PY caesar.py -v dict-attack "Khoor"'
"$PY" caesar.py -v dict-attack "Khoor"
echo ""
_demo_pause

echo "Запускаем тесты"
echo ""
echo '$ $PY -m pytest test_caesar.py -v --tb=short'
"$PY" -m pytest test_caesar.py -v --tb=short

echo ""
_demo_pause
echo "Готово"

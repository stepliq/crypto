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
echo "=== Лабораторная 2: энтропия и частоты байтов ==="
echo ""
_demo_pause

echo "Шаг 0. Генерируем тестовые файлы"
echo ""
echo '$ $PY entropy_lab.py demo -n 8000'
"$PY" entropy_lab.py demo -n 8000
echo ""
_demo_pause

echo "Шаг 1. Смотрим доступные команды"
echo ""
echo '$ $PY entropy_lab.py --help'
"$PY" entropy_lab.py --help
echo ""
_demo_pause

echo "Шаг 2. Частоты символов"
echo "Пример: текстовый файл"
echo ""
echo '$ $PY entropy_lab.py freq samples/sample_text.txt --top 8'
"$PY" entropy_lab.py freq samples/sample_text.txt --top 8
echo ""
_demo_pause

echo "Шаг 3. Энтропия"
echo "Файл из одного символа → почти нет неопределённости"
echo ""
echo '$ $PY entropy_lab.py entropy samples/sample_const.bin --top 4'
"$PY" entropy_lab.py entropy samples/sample_const.bin --top 4
echo ""
_demo_pause

echo "Шаг 4. Случайные 0/1"
echo "Ожидаем: H ≈ 1 бит"
echo ""
echo '$ $PY entropy_lab.py entropy samples/sample_coin.txt --top 4'
"$PY" entropy_lab.py entropy samples/sample_coin.txt --top 4
echo ""
_demo_pause

echo "Шаг 5. Случайные байты (0..255)"
echo "Ожидаем: H ≈ 8 бит (максимум)"
echo ""
echo '$ $PY entropy_lab.py entropy samples/sample_uniform255.bin --top 8'
"$PY" entropy_lab.py entropy samples/sample_uniform255.bin --top 8
echo ""
_demo_pause

echo "Шаг 6. Два символа 50/50"
echo "Ожидаем: H ≈ 1 бит"
echo ""
echo '$ $PY entropy_lab.py entropy samples/sample_two_equal.bin --top 4'
"$PY" entropy_lab.py entropy samples/sample_two_equal.bin --top 4
echo ""
_demo_pause

echo "Шаг 7. Повторяющийся текст"
echo "Энтропия ниже максимума (неравномерное распределение)"
echo ""
echo '$ $PY entropy_lab.py entropy samples/sample_text.txt --top 8'
"$PY" entropy_lab.py entropy samples/sample_text.txt --top 8
echo ""
_demo_pause

echo "Шаг 8. Проверка тестами"
echo ""
echo '$ $PY -m pytest test_entropy_lab.py -v --tb=short'
"$PY" -m pytest test_entropy_lab.py -v --tb=short

echo ""
echo "=== Готово ==="

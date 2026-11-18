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
echo "=== Лабораторная 4, XTEA и CBC ==="
echo ""

echo "Покажем справку CLI"
echo ""
echo '$ $PY block_cipher.py -v --help'
"$PY" block_cipher.py -v --help
echo ""
_demo_pause

echo "Подготовим samples"
echo ""
echo '$ $PY block_cipher.py prepare-samples --dir samples'
"$PY" block_cipher.py prepare-samples --dir samples
echo ""
_demo_pause

echo "Задача 1. Итеративный блочный шифр XTEA"
echo "Покажем встроенную демонстрацию шифрования одного блока и CBC-файла"
echo ""
echo '$ $PY block_cipher.py demo --dir samples'
"$PY" block_cipher.py demo --dir samples
echo ""
_demo_pause

echo "Задача 2. Шифрование и расшифрование файла XTEA в режиме CBC"
echo ""
echo '$ $PY block_cipher.py encrypt samples/plain.txt samples/cipher.bin --key-file samples/key.bin'
"$PY" block_cipher.py encrypt samples/plain.txt samples/cipher.bin --key-file samples/key.bin
echo '$ $PY block_cipher.py decrypt samples/cipher.bin samples/restored.txt --key-file samples/key.bin'
"$PY" block_cipher.py decrypt samples/cipher.bin samples/restored.txt --key-file samples/key.bin
echo '$ cmp -s samples/plain.txt samples/restored.txt && echo "Совпадает: true"'
cmp -s samples/plain.txt samples/restored.txt && echo "Совпадает: true"
echo ""
_demo_pause

echo "Запускаем тесты"
echo ""
echo '$ $PY -m pytest test_block_cipher.py -v --tb=short'
"$PY" -m pytest test_block_cipher.py -v --tb=short

echo ""
_demo_pause
echo "Готово"

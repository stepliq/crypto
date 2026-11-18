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
echo "=== Лабораторная 3, потоковые шифры ==="
echo ""
_demo_pause

echo "Покажем справку CLI"
echo ""
echo '$ $PY stream_ciphers.py -v --help'
"$PY" stream_ciphers.py -v --help
echo ""
_demo_pause

echo "Подготовим samples через основной Python-код"
echo ""
echo '$ $PY stream_ciphers.py prepare-samples --dir samples --method secrets'
"$PY" stream_ciphers.py prepare-samples --dir samples --method secrets
echo ""
_demo_pause

echo "Задача 1. Генерация файла ключа из случайных символов (ГПСЧ)"
echo "Ключ уже сгенерирован на предыдущем шаге в samples/key.bin"
echo ""
echo '$ ls -lh samples/plain.txt samples/key.bin'
ls -lh samples/plain.txt samples/key.bin
echo ""
_demo_pause

echo "Задача 2. Шифр Вернама (XOR): шифрование и расшифрование файла"
echo ""
echo '$ $PY stream_ciphers.py vernam-encrypt samples/plain.txt samples/key.bin samples/vernam.bin'
"$PY" stream_ciphers.py vernam-encrypt samples/plain.txt samples/key.bin samples/vernam.bin
echo '$ $PY stream_ciphers.py vernam-decrypt samples/vernam.bin samples/key.bin samples/recovered.txt'
"$PY" stream_ciphers.py vernam-decrypt samples/vernam.bin samples/key.bin samples/recovered.txt
echo '$ cmp -s samples/plain.txt samples/recovered.txt && echo "Совпадает: true"'
cmp -s samples/plain.txt samples/recovered.txt && echo "Совпадает: true"
echo ""
_demo_pause

echo "Задача 3. Применение готового поточного шифра ChaCha20"
echo ""
echo '$ $PY stream_ciphers.py chacha-encrypt samples/plain.txt samples/key.bin samples/chacha.bin'
"$PY" stream_ciphers.py chacha-encrypt samples/plain.txt samples/key.bin samples/chacha.bin
echo '$ $PY stream_ciphers.py chacha-decrypt samples/chacha.bin samples/key.bin samples/chacha_plain.txt'
"$PY" stream_ciphers.py chacha-decrypt samples/chacha.bin samples/key.bin samples/chacha_plain.txt
echo '$ cmp -s samples/plain.txt samples/chacha_plain.txt && echo "Round-trip: true"'
cmp -s samples/plain.txt samples/chacha_plain.txt && echo "Round-trip: true"
echo ""
_demo_pause

echo "Запускаем тесты"
echo ""
echo '$ $PY -m pytest test_stream_ciphers.py -v --tb=short'
"$PY" -m pytest test_stream_ciphers.py -v --tb=short

echo ""
_demo_pause
echo "Готово"

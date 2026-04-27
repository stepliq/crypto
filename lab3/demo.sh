#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

_demo_pause() {
  [[ -z "${LAB_DEMO_PAUSE:-}" ]] || sleep "${LAB_DEMO_PAUSE}"
}

echo ""
echo "=== Лабораторная 3, потоковые шифры ==="
echo ""
_demo_pause

echo "Покажем справку CLI"
echo ""
echo '$ python3 stream_ciphers.py -v --help'
python3 stream_ciphers.py -v --help
echo ""
_demo_pause

echo "Подготовим samples через основной Python-код"
echo ""
echo '$ python3 stream_ciphers.py prepare-samples --dir samples --method secrets'
python3 stream_ciphers.py prepare-samples --dir samples --method secrets
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
echo '$ python3 stream_ciphers.py vernam-encrypt samples/plain.txt samples/key.bin samples/vernam.bin'
python3 stream_ciphers.py vernam-encrypt samples/plain.txt samples/key.bin samples/vernam.bin
echo '$ python3 stream_ciphers.py vernam-decrypt samples/vernam.bin samples/key.bin samples/recovered.txt'
python3 stream_ciphers.py vernam-decrypt samples/vernam.bin samples/key.bin samples/recovered.txt
echo '$ cmp -s samples/plain.txt samples/recovered.txt && echo "Совпадает: true"'
cmp -s samples/plain.txt samples/recovered.txt && echo "Совпадает: true"
echo ""
_demo_pause

echo "Задача 3. Применение готового поточного шифра ChaCha20"
echo ""
echo '$ python3 stream_ciphers.py chacha-encrypt samples/plain.txt samples/key.bin samples/chacha.bin'
python3 stream_ciphers.py chacha-encrypt samples/plain.txt samples/key.bin samples/chacha.bin
echo '$ python3 stream_ciphers.py chacha-decrypt samples/chacha.bin samples/key.bin samples/chacha_plain.txt'
python3 stream_ciphers.py chacha-decrypt samples/chacha.bin samples/key.bin samples/chacha_plain.txt
echo '$ cmp -s samples/plain.txt samples/chacha_plain.txt && echo "Round-trip: true"'
cmp -s samples/plain.txt samples/chacha_plain.txt && echo "Round-trip: true"
echo ""
_demo_pause

echo "Запускаем тесты"
echo ""
echo '$ python3 -m pytest test_stream_ciphers.py -v --tb=short'
python3 -m pytest test_stream_ciphers.py -v --tb=short

echo ""
_demo_pause
echo "Готово"

# crypto labs

## 1sem
Labs `lab1`…`lab7`.

## 2sem
Practical assignments from topics 2.1–2.4:

| lab | topic | practical task | libs |
|---|---|---|---|
| `2sem/lab1` | PKI | hierarchical + network trust chains | `networkx` |
| `2sem/lab2` | Elliptic curves | residue tables, EC ops, scalar mul | `sympy` |
| `2sem/lab3` | MAC | HMAC-SHA256 + file integrity | stdlib |
| `2sem/lab4` | Key distribution | Diffie–Hellman for N users | `sympy` |

Lecture/source PDFs: `2sem/materials/`.

Each lab: modular Python package (`*_lab.py` entry + helpers), `test_*.py`, `demo.sh`, `requirements.txt`.

### Setup

System Python is PEP 668 managed. Prefer the repo venv:

```bash
python3 -m venv .venv
.venv/bin/pip install -U pip
.venv/bin/pip install -r 2sem/lab1/requirements.txt \
  -r 2sem/lab2/requirements.txt \
  -r 2sem/lab3/requirements.txt \
  -r 2sem/lab4/requirements.txt \
  pytest
```

If you insist on system Python (Arch/PEP 668):

```bash
python3 -m pip install --user --break-system-packages \
  -r 2sem/lab1/requirements.txt \
  -r 2sem/lab2/requirements.txt \
  -r 2sem/lab3/requirements.txt \
  -r 2sem/lab4/requirements.txt
```

### Run

```bash
# all 2sem labs (uses .venv)
./test_2sem.sh

# one lab
cd 2sem/lab1
../../.venv/bin/python -m pytest -v
bash demo.sh   # auto-picks repo .venv if present
# optional GIF:
# ../../record_demo_gif.sh .
```

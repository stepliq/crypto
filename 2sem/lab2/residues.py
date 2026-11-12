from __future__ import annotations

from util import is_prime, multiplicative_order


def elements(p: int) -> list[int]:
    if not is_prime(p):
        raise ValueError(f"P must be prime, got {p}")
    return list(range(1, p))


def mult_table(p: int) -> list[list[int]]:
    elems = elements(p)
    return [[(a * b) % p for b in elems] for a in elems]


def element_order(a: int, p: int) -> int:
    if a % p == 0:
        raise ValueError("0 is not in (Z/pZ)*")
    return multiplicative_order(a, p)


def orders_table(p: int) -> list[tuple[int, list[int], int, bool]]:
    rows: list[tuple[int, list[int], int, bool]] = []
    for a in elements(p):
        order = element_order(a, p)
        powers = [pow(a, k, p) for k in range(1, order + 1)]
        rows.append((a, powers, order, order == p - 1))
    return rows


def format_mult_table(p: int) -> str:
    elems = elements(p)
    table = mult_table(p)
    width = max(2, len(str(p - 1)))
    header = "*".rjust(width) + " |" + "".join(str(b).rjust(width + 1) for b in elems)
    lines = [header, "-" * len(header)]
    for a, row in zip(elems, table):
        lines.append(str(a).rjust(width) + " |" + "".join(str(x).rjust(width + 1) for x in row))
    return "\n".join(lines)


def format_orders(p: int) -> str:
    rows = orders_table(p)
    max_ord = p - 1
    width = max(2, len(str(p - 1)))
    head = "".join(f"a^{i}".rjust(width + 1) for i in range(1, max_ord + 1))
    lines = [f"a |{head} | ord | gen?", "-" * (len(head) + 14)]
    for a, powers, order, is_gen in rows:
        padded: list[int | str] = list(powers) + [""] * (max_ord - len(powers))
        pows = "".join(str(x).rjust(width + 1) for x in padded)
        gen = "GEN" if is_gen else ""
        lines.append(f"{a} |{pows} | {order:>3} | {gen}")
    gens = [a for a, _, _, g in rows if g]
    lines.append(f"generators (order = p-1 = {p - 1}): {gens}")
    return "\n".join(lines)

from __future__ import annotations

from sympy import isprime, mod_inverse
from sympy.ntheory import n_order


def is_prime(n: int) -> bool:
    return bool(isprime(n))


def inv_mod(a: int, p: int) -> int:
    return int(mod_inverse(a % p, p))


def multiplicative_order(a: int, p: int) -> int:
    return int(n_order(a % p, p))

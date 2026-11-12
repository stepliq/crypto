from __future__ import annotations

import random
import secrets
from dataclasses import dataclass

from sympy import isprime


@dataclass(frozen=True)
class DHParams:
    p: int
    g: int


@dataclass(frozen=True)
class User:
    name: str
    private: int
    public: int


def is_prime(n: int) -> bool:
    return bool(isprime(n))


def generate_users(n: int, params: DHParams, seed: int | None = None) -> list[User]:
    if n < 2:
        raise ValueError("need at least 2 users")
    rng = secrets.SystemRandom() if seed is None else random.Random(seed)
    users: list[User] = []
    for i in range(n):
        private = rng.randrange(2, params.p - 1)
        public = pow(params.g, private, params.p)
        users.append(User(name=f"U{i + 1}", private=private, public=public))
    return users


def find_user(users: list[User], name: str) -> User:
    for user in users:
        if user.name.lower() == name.lower():
            return user
    raise KeyError(f"unknown user {name!r}")


def shared_secret(params: DHParams, me: User, peer: User) -> tuple[int, list[str]]:
    k1 = pow(peer.public, me.private, params.p)
    k2 = pow(me.public, peer.private, params.p)
    if k1 != k2:
        raise RuntimeError("shared secrets do not match")

    steps = [
        f"params: p={params.p}, g={params.g}",
        f"{me.name}: x={me.private}, y=g^x mod p = {me.public}",
        f"{peer.name}: x={peer.private}, y=g^x mod p = {peer.public}",
        f"{me.name}: K = y_{peer.name}^x_{me.name} = {peer.public}^{me.private} mod {params.p} = {k1}",
        f"{peer.name}: K = y_{me.name}^x_{peer.name} = {me.public}^{peer.private} mod {params.p} = {k2}",
        f"shared secret {me.name}-{peer.name}: {k1}",
    ]
    return k1, steps

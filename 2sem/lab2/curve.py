from __future__ import annotations

from dataclasses import dataclass

from sympy.ntheory.elliptic_curve import EllipticCurve as SymCurve

from util import is_prime


@dataclass(frozen=True)
class Point:
    x: int | None
    y: int | None
    infinity: bool = False

    @staticmethod
    def O() -> Point:
        return Point(None, None, True)

    def __str__(self) -> str:
        return "O" if self.infinity else f"({self.x},{self.y})"

    def label(self) -> str:
        return "(0,0)" if self.infinity else str(self)


class EllipticCurve:
    """y^2 = x^3 + a x + b (mod p), backed by sympy for group law."""

    def __init__(self, p: int, a: int, b: int) -> None:
        if not is_prime(p):
            raise ValueError(f"p must be prime: {p}")
        self.p = p
        self.a = a % p
        self.b = b % p
        self._curve = SymCurve(self.a, self.b, modulus=p)
        if self._curve.is_singular:
            raise ValueError("singular curve")

    def _to_sym(self, pt: Point):
        if pt.infinity:
            return self._curve(0, 1, 0)
        assert pt.x is not None and pt.y is not None
        return self._curve(pt.x, pt.y)

    def _from_sym(self, pt) -> Point:
        if str(pt) == "O" or int(pt.z) == 0:
            return Point.O()
        return Point(int(pt.x) % self.p, int(pt.y) % self.p)

    def on_curve(self, pt: Point) -> bool:
        if pt.infinity:
            return True
        assert pt.x is not None and pt.y is not None
        return (pt.x, pt.y) in self._curve

    def points(self) -> list[Point]:
        affine = [
            Point(int(x) % self.p, int(y) % self.p)
            for x, y in self._curve.points()
        ]
        return [Point.O()] + sorted(affine, key=lambda pt: (pt.x, pt.y))

    def add(self, p: Point, q: Point) -> Point:
        return self._from_sym(self._to_sym(p) + self._to_sym(q))

    def negate(self, p: Point) -> Point:
        if p.infinity:
            return p
        assert p.x is not None and p.y is not None
        return Point(p.x, (-p.y) % self.p)

    def mul(self, m: int, p: Point) -> Point:
        if m < 0:
            return self.mul(-m, self.negate(p))
        return self._from_sym(m * self._to_sym(p))

    def mul_trace(self, m: int, p: Point) -> tuple[Point, list[tuple[int, int, int, Point, Point]]]:
        if m < 0:
            raise ValueError("m must be >= 0 for trace")
        rows: list[tuple[int, int, int, Point, Point]] = []
        result = Point.O()
        addend = p
        if m == 0:
            return result, []

        i = 0
        mm = m
        while mm > 0:
            bit = mm & 1
            if bit:
                result = self.add(result, addend)
            rows.append((i, 1 << i, bit, addend, result))
            addend = self.add(addend, addend)
            mm >>= 1
            i += 1
        return result, rows


def point_order(curve: EllipticCurve, p: Point, group_size: int | None = None) -> int:
    # sympy's EllipticCurvePoint.order() is unreliable on small prime fields,
    # so compute the order from the group law directly.
    if p.infinity:
        return 1
    limit = group_size if group_size is not None else len(curve.points())
    acc = p
    for k in range(1, limit + 1):
        if acc.infinity:
            return k
        acc = curve.add(acc, p)
    raise RuntimeError(f"order of {p} not found")


def format_add_table(curve: EllipticCurve) -> str:
    group = curve.points()
    labels = [pt.label() for pt in group]
    w = max(len(s) for s in labels + ["+"])
    header = "+".rjust(w) + " |" + "".join(s.rjust(w + 1) for s in labels)
    lines = [header, "-" * len(header)]
    for i, p in enumerate(group):
        vals = [curve.add(p, q).label() for q in group]
        lines.append(labels[i].rjust(w) + " |" + "".join(s.rjust(w + 1) for s in vals))
    return "\n".join(lines)


def format_orders(curve: EllipticCurve) -> str:
    group = curve.points()
    n = len(group)
    lines = [f"|E| = {n} (O shown as (0,0))", "P | multiples | order | gen?"]
    gens: list[str] = []

    for p in group:
        if p.infinity:
            lines.append("(0,0) | (0,0) | 1 | ")
            continue
        order = point_order(curve, p)
        multiples = [curve.mul(k, p).label() for k in range(1, order + 1)]
        is_gen = order == n
        if is_gen:
            gens.append(str(p))
        lines.append(f"{p} | {' '.join(multiples)} | {order} | {'GEN' if is_gen else ''}")

    lines.append(f"generators (order = |E| = {n}): {gens}")
    return "\n".join(lines)

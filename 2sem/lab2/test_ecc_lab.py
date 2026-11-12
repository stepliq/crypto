from __future__ import annotations

import unittest

from click.testing import CliRunner

from curve import EllipticCurve, Point, point_order
from ecc_cli import cli
from residues import element_order, mult_table, orders_table


class TestResidues(unittest.TestCase):
    def test_mult_table_mod7(self) -> None:
        table = mult_table(7)
        self.assertEqual(table[0], [1, 2, 3, 4, 5, 6])
        self.assertEqual(table[1], [2, 4, 6, 1, 3, 5])

    def test_generators_mod7(self) -> None:
        gens = [a for a, _, _, g in orders_table(7) if g]
        self.assertEqual(gens, [3, 5])
        self.assertEqual(element_order(2, 7), 3)
        self.assertEqual(element_order(6, 7), 2)


class TestEllipticCurve(unittest.TestCase):
    def setUp(self) -> None:
        self.curve = EllipticCurve(p=7, a=1, b=3)

    def test_points_count(self) -> None:
        pts = self.curve.points()
        self.assertEqual(len(pts), 6)
        affine = {str(p) for p in pts if not p.infinity}
        self.assertEqual(affine, {"(4,1)", "(4,6)", "(5,0)", "(6,1)", "(6,6)"})

    def test_add_inverse_is_infinity(self) -> None:
        self.assertTrue(self.curve.add(Point(4, 1), Point(4, 6)).infinity)

    def test_generators(self) -> None:
        n = len(self.curve.points())
        self.assertEqual(point_order(self.curve, Point(4, 1), n), 6)
        self.assertEqual(point_order(self.curve, Point(4, 6), n), 6)
        self.assertEqual(point_order(self.curve, Point(5, 0), n), 2)

    def test_presentation_scalar(self) -> None:
        curve = EllipticCurve(p=53, a=45, b=27)
        p = Point(6, 47)
        self.assertTrue(curve.on_curve(p))
        self.assertEqual(curve.mul(120, p), Point(12, 49))


class TestCLI(unittest.TestCase):
    def test_demo(self) -> None:
        result = CliRunner().invoke(cli, ["demo"])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("[m]P = (12,49)", result.output)
        self.assertIn("GEN", result.output)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from click.testing import CliRunner

from demo_data import sample_hierarchical, sample_network
from pki_cli import cli


class TestHierarchicalPKI(unittest.TestCase):
    def setUp(self) -> None:
        self.pki = sample_hierarchical()

    def test_chain_to_root(self) -> None:
        subjects = [c.subject for c in self.pki.trust_chain("Alice")]
        self.assertEqual(subjects, ["Alice", "DeptCA", "IntermediateCA", "RootCA"])

    def test_root_self_signed(self) -> None:
        chain = self.pki.trust_chain("RootCA")
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0].subject, chain[0].issuer)

    def test_missing_leaf(self) -> None:
        with self.assertRaises(KeyError):
            self.pki.trust_chain("Eve")


class TestNetworkPKI(unittest.TestCase):
    def setUp(self) -> None:
        self.pki = sample_network()

    def test_shortest_path(self) -> None:
        self.assertEqual(self.pki.trust_chain("CA1", "Bob"), ["CA1", "CA2", "CA3", "Bob"])

    def test_same_node(self) -> None:
        self.assertEqual(self.pki.trust_chain("Alice", "Alice"), ["Alice"])

    def test_no_path(self) -> None:
        self.assertIsNone(self.pki.trust_chain("Bob", "Alice"))

    def test_adjacency_matrix(self) -> None:
        nodes, matrix = self.pki.adjacency_matrix()
        i, j = nodes.index("CA1"), nodes.index("CA2")
        self.assertEqual(matrix[i][j], 1)


class TestCLI(unittest.TestCase):
    def test_demo(self) -> None:
        result = CliRunner().invoke(cli, ["demo"])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("hierarchical", result.output.lower())
        self.assertIn("network", result.output.lower())


if __name__ == "__main__":
    unittest.main()

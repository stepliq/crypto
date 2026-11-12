from __future__ import annotations

import unittest

from click.testing import CliRunner

from dh import DHParams, generate_users, shared_secret
from keydist_cli import cli


class TestDH(unittest.TestCase):
    def test_shared_secret_symmetric(self) -> None:
        params = DHParams(p=23, g=5)
        users = generate_users(3, params, seed=1)
        k12, _ = shared_secret(params, users[0], users[1])
        k21, _ = shared_secret(params, users[1], users[0])
        self.assertEqual(k12, k21)
        self.assertEqual(k12, pow(users[1].public, users[0].private, params.p))

    def test_public_matches_pow(self) -> None:
        params = DHParams(p=23, g=5)
        users = generate_users(2, params, seed=7)
        for user in users:
            self.assertEqual(user.public, pow(params.g, user.private, params.p))


class TestCLI(unittest.TestCase):
    def test_demo(self) -> None:
        result = CliRunner().invoke(cli, ["demo"])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("shared secret", result.output)

    def test_pair(self) -> None:
        result = CliRunner().invoke(cli, ["pair", "U1", "U2", "-n", "4", "--seed", "42"])
        self.assertEqual(result.exit_code, 0, result.output)


if __name__ == "__main__":
    unittest.main()

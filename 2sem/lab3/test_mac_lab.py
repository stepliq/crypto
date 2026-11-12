from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from click.testing import CliRunner

from hmac_mac import tag_hex, verify
from integrity import check, protect
from mac_cli import cli


class TestHMAC(unittest.TestCase):
    def test_roundtrip(self) -> None:
        key = b"key"
        msg = b"The quick brown fox jumps over the lazy dog"
        mac = tag_hex(key, msg)
        self.assertEqual(len(mac), 64)
        self.assertTrue(verify(key, msg, mac))
        self.assertFalse(verify(key, msg + b"x", mac))


class TestFileIntegrity(unittest.TestCase):
    def test_detect_tamper(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sample = Path(tmp) / "file.txt"
            sample.write_text("hello\n", encoding="utf-8")
            key = b"secret"
            catalog = protect(key, [sample])
            self.assertTrue(check(key, catalog)[0].ok)
            sample.write_text("bye\n", encoding="utf-8")
            self.assertFalse(check(key, catalog)[0].ok)


class TestCLI(unittest.TestCase):
    def test_demo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            old = os.getcwd()
            try:
                os.chdir(tmp)
                result = CliRunner().invoke(cli, ["demo"])
            finally:
                os.chdir(old)
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("HMAC-SHA256", result.output)
        self.assertIn("FAIL", result.output)


if __name__ == "__main__":
    unittest.main()

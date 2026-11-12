from __future__ import annotations

import hashlib
import hmac


def tag(key: bytes, msg: bytes) -> bytes:
    return hmac.new(key, msg, hashlib.sha256).digest()


def tag_hex(key: bytes, msg: bytes) -> str:
    return tag(key, msg).hex()


def verify(key: bytes, msg: bytes, tag_hex_value: str) -> bool:
    try:
        expected = bytes.fromhex(tag_hex_value)
    except ValueError:
        return False
    return hmac.compare_digest(tag(key, msg), expected)

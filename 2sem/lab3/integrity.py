from __future__ import annotations

import hmac
import os
import json
from dataclasses import dataclass
from pathlib import Path

from hmac_mac import tag_hex

Catalog = dict[str, str]


def catalog_key(path: Path) -> str:
    """Stable relative key so ./samples/f and samples/f match."""
    path = Path(path)
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return Path(os.path.normpath(str(path))).as_posix()


@dataclass(frozen=True)
class CheckResult:
    path: str
    ok: bool
    detail: str


def protect(key: bytes, files: list[Path]) -> Catalog:
    return {catalog_key(path): tag_hex(key, path.read_bytes()) for path in files}


def check(key: bytes, catalog: Catalog) -> list[CheckResult]:
    results: list[CheckResult] = []
    for path_str, expected in catalog.items():
        path = Path(path_str)
        if not path.exists():
            results.append(CheckResult(path_str, False, "missing"))
            continue
        actual = tag_hex(key, path.read_bytes())
        ok = hmac.compare_digest(actual, expected)
        detail = "ok" if ok else f"expected {expected}, got {actual}"
        results.append(CheckResult(path_str, ok, detail))
    return results


def save_catalog(catalog: Catalog, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_catalog(path: Path) -> Catalog:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("catalog must be a JSON object")
    return {str(k): str(v) for k, v in data.items()}

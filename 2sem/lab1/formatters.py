from __future__ import annotations

from hierarchical import Certificate


def format_hierarchical_chain(chain: list[Certificate]) -> str:
    lines = ["Trust chain (hierarchical PKI):"]
    for i, cert in enumerate(chain, 1):
        mark = " <- ROOT" if cert.subject == cert.issuer else ""
        lines.append(f"  {i}. {cert}{mark}")
    lines.append("Path: " + " -> ".join(c.subject for c in chain))
    return "\n".join(lines)


def format_network_chain(path: list[str] | None, trust_anchor: str, target: str) -> str:
    if path is None:
        return f"No trust chain: {trust_anchor} -/-> {target}"

    lines = [
        "Trust chain (network PKI):",
        "  nodes: " + " -> ".join(path),
    ]
    for i, (a, b) in enumerate(zip(path, path[1:]), 1):
        lines.append(f"  {i}. Cert({b} <- {a})")
    return "\n".join(lines)

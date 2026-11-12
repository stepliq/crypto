from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Certificate:
    subject: str
    issuer: str

    def __str__(self) -> str:
        return f"Cert({self.subject} <- {self.issuer})"


class HierarchicalPKI:
    def __init__(self, owner_to_ca: dict[str, str], root: str) -> None:
        if root not in owner_to_ca:
            raise ValueError(f"root {root!r} missing from mapping")
        if owner_to_ca[root] != root:
            raise ValueError(f"root {root!r} must be self-signed")
        self.owner_to_ca = dict(owner_to_ca)
        self.root = root

    def certificate_of(self, owner: str) -> Certificate:
        if owner not in self.owner_to_ca:
            raise KeyError(f"no certificate for {owner!r}")
        return Certificate(subject=owner, issuer=self.owner_to_ca[owner])

    def trust_chain(self, leaf: str) -> list[Certificate]:
        if leaf not in self.owner_to_ca:
            raise KeyError(f"unknown node {leaf!r}")

        chain: list[Certificate] = []
        seen: set[str] = set()
        current = leaf

        while True:
            if current in seen:
                raise ValueError(f"cycle near {current!r}")
            seen.add(current)

            cert = self.certificate_of(current)
            chain.append(cert)

            if current == self.root:
                return chain

            current = cert.issuer
            if current not in self.owner_to_ca:
                raise ValueError(f"broken chain: missing CA {current!r}")

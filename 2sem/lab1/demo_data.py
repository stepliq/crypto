from __future__ import annotations

from hierarchical import HierarchicalPKI
from network import NetworkPKI


def sample_hierarchical() -> HierarchicalPKI:
    return HierarchicalPKI(
        {
            "RootCA": "RootCA",
            "IntermediateCA": "RootCA",
            "DeptCA": "IntermediateCA",
            "Alice": "DeptCA",
            "Bob": "DeptCA",
        },
        root="RootCA",
    )


def sample_network() -> NetworkPKI:
    return NetworkPKI(
        {
            "CA1": ["CA2", "Alice"],
            "CA2": ["CA3", "CA1"],
            "CA3": ["Bob"],
            "Alice": [],
            "Bob": [],
        }
    )

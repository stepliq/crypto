from __future__ import annotations

from dh import DHParams, User


def format_users_table(params: DHParams, users: list[User]) -> str:
    lines = [
        f"DH params: p={params.p}, g={params.g}",
        f"{'user':<6} {'private x':>10} {'public y':>12}",
        "-" * 32,
    ]
    for user in users:
        lines.append(f"{user.name:<6} {user.private:>10} {user.public:>12}")
    return "\n".join(lines)

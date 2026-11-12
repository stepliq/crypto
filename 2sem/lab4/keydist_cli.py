from __future__ import annotations

import logging
import time

import click

from dh import DHParams, find_user, generate_users, is_prime, shared_secret
from dh_formatters import format_users_table

DEFAULT_P = 23
DEFAULT_G = 5
DEFAULT_N = 4
DEFAULT_SEED = 42


def time_seed() -> int:
    return int(time.time())


def configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
        force=True,
    )


def make_params(p: int, g: int) -> DHParams:
    if not is_prime(p):
        raise click.ClickException(f"p must be prime: {p}")
    if not (2 <= g <= p - 2):
        raise click.ClickException(f"g must satisfy 2 <= g <= p-2, got {g}")
    return DHParams(p=p, g=g)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-v", "--verbose", is_flag=True)
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Lab 2.4 — Diffie-Hellman key distribution."""
    configure_logging(verbose)
    ctx.ensure_object(dict)


@cli.command("setup")
@click.option("-n", "--users", "n_users", type=int, default=DEFAULT_N, show_default=True)
@click.option("--p", type=int, default=DEFAULT_P, show_default=True)
@click.option("--g", type=int, default=DEFAULT_G, show_default=True)
@click.option("--seed", type=int, default=DEFAULT_SEED, show_default=True)
def cmd_setup(n_users: int, p: int, g: int, seed: int) -> None:
    params = make_params(p, g)
    users = generate_users(n_users, params, seed=seed)
    click.echo(format_users_table(params, users))


@cli.command("pair")
@click.argument("a")
@click.argument("b")
@click.option("-n", "--users", "n_users", type=int, default=DEFAULT_N, show_default=True)
@click.option("--p", type=int, default=DEFAULT_P, show_default=True)
@click.option("--g", type=int, default=DEFAULT_G, show_default=True)
@click.option("--seed", type=int, default=DEFAULT_SEED, show_default=True)
def cmd_pair(a: str, b: str, n_users: int, p: int, g: int, seed: int) -> None:
    params = make_params(p, g)
    users = generate_users(n_users, params, seed=seed)
    click.echo(format_users_table(params, users))
    click.echo("")
    _, steps = shared_secret(params, find_user(users, a), find_user(users, b))
    for line in steps:
        click.echo(line)


@cli.command("demo")
@click.option("--seed", type=int, default=DEFAULT_SEED, show_default=True)
def cmd_demo(seed: int) -> None:
    params = DHParams(p=DEFAULT_P, g=DEFAULT_G)
    users = generate_users(DEFAULT_N, params, seed=seed)
    click.echo(format_users_table(params, users))
    click.echo("")
    for a, b in (("U1", "U2"), ("U1", "U4"), ("U2", "U3")):
        click.echo(f"--- pair {a} {b} ---")
        _, steps = shared_secret(params, find_user(users, a), find_user(users, b))
        for line in steps:
            click.echo(line)
        click.echo("")


@cli.command("interactive")
@click.option("-n", "--users", "n_users", type=int, prompt="number of users")
@click.option("--p", type=int, default=DEFAULT_P, show_default=True)
@click.option("--g", type=int, default=DEFAULT_G, show_default=True)
@click.option("--seed", type=int, default=None)
def cmd_interactive(n_users: int, p: int, g: int, seed: int | None) -> None:
    params = make_params(p, g)
    users = generate_users(n_users, params, seed=seed)
    click.echo(format_users_table(params, users))
    names = ", ".join(user.name for user in users)

    while True:
        click.echo("")
        choice = click.prompt(
            f"two users (from {names}) or exit",
            default="exit",
            show_default=True,
        )
        if choice.strip().lower() in {"exit", "q", "quit", "выход"}:
            click.echo("bye")
            break

        parts = choice.split()
        if len(parts) != 2:
            click.echo("expected two names, e.g. U1 U3")
            continue

        try:
            left = find_user(users, parts[0])
            right = find_user(users, parts[1])
        except KeyError as exc:
            click.echo(str(exc))
            continue

        _, steps = shared_secret(params, left, right)
        for line in steps:
            click.echo(line)

from __future__ import annotations

import logging

import click

from demo_data import sample_hierarchical, sample_network
from formatters import format_hierarchical_chain, format_network_chain


def configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
        force=True,
    )


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-v", "--verbose", is_flag=True)
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Lab 2.1 — hierarchical and network PKI trust chains."""
    configure_logging(verbose)
    ctx.ensure_object(dict)


@cli.command("hierarchical")
@click.option("--leaf", default="Alice", show_default=True)
def cmd_hierarchical(leaf: str) -> None:
    pki = sample_hierarchical()
    click.echo("owner -> CA")
    for owner, ca in sorted(pki.owner_to_ca.items()):
        click.echo(f"  {owner:>16} -> {ca}")
    click.echo(f"root: {pki.root}\n")
    click.echo(format_hierarchical_chain(pki.trust_chain(leaf)))


@cli.command("network")
@click.option("--anchor", default="CA1", show_default=True)
@click.option("--target", default="Bob", show_default=True)
def cmd_network(anchor: str, target: str) -> None:
    pki = sample_network()
    nodes, matrix = pki.adjacency_matrix()

    click.echo("adjacency lists (A -> B = A signed B)")
    for src in nodes:
        dsts = pki.adjacency[src]
        click.echo(f"  {src}: {', '.join(dsts) if dsts else '(none)'}")

    click.echo("\nadjacency matrix: " + ", ".join(nodes))
    click.echo("     " + " ".join(f"{n:>5}" for n in nodes))
    for i, row in enumerate(matrix):
        click.echo(f"{nodes[i]:>5} " + " ".join(f"{x:>5}" for x in row))

    click.echo("")
    click.echo(format_network_chain(pki.trust_chain(anchor, target), anchor, target))


@cli.command("demo")
def cmd_demo() -> None:
    ctx = click.get_current_context()
    click.echo("=== hierarchical PKI ===\n")
    ctx.invoke(cmd_hierarchical, leaf="Alice")
    click.echo("\n=== network PKI ===\n")
    ctx.invoke(cmd_network, anchor="CA1", target="Bob")

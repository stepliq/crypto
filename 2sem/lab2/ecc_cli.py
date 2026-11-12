from __future__ import annotations

import logging

import click

from curve import EllipticCurve, Point, format_add_table, format_orders as format_ec_orders
from residues import format_mult_table, format_orders as format_mod_orders


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
    """Lab 2.2 — residue groups and elliptic curves."""
    configure_logging(verbose)
    ctx.ensure_object(dict)


@cli.command("mult-table")
@click.argument("p", type=int)
def cmd_mult_table(p: int) -> None:
    click.echo(format_mult_table(p))


@cli.command("orders-mod")
@click.argument("p", type=int)
def cmd_orders_mod(p: int) -> None:
    click.echo(format_mod_orders(p))


@cli.command("scalar")
@click.option("--p", "prime", type=int, default=53, show_default=True)
@click.option("--a", type=int, default=45, show_default=True)
@click.option("--b", type=int, default=27, show_default=True)
@click.option("--x", type=int, default=6, show_default=True)
@click.option("--y", type=int, default=47, show_default=True)
@click.option("--m", type=int, default=120, show_default=True)
def cmd_scalar(prime: int, a: int, b: int, x: int, y: int, m: int) -> None:
    curve = EllipticCurve(p=prime, a=a, b=b)
    pt = Point(x, y)
    if not curve.on_curve(pt):
        raise click.ClickException(f"{pt} is not on the curve")
    result, rows = curve.mul_trace(m, pt)
    click.echo(f"y^2 = x^3 + {a}x + {b} (mod {prime})")
    click.echo(f"P = {pt}, m = {m} = {bin(m)}")
    click.echo("i  2^i  bit  T=2^i*P     sum")
    for i, pow2, bit, addend, acc in rows:
        click.echo(f"{i:<3}{pow2:<5}{bit:<5}{str(addend):<12}{acc}")
    click.echo(f"[m]P = {result}")


@cli.command("ec-table")
@click.option("--p", "prime", type=int, default=7, show_default=True)
@click.option("--a", type=int, default=1, show_default=True)
@click.option("--b", type=int, default=3, show_default=True)
def cmd_ec_table(prime: int, a: int, b: int) -> None:
    curve = EllipticCurve(p=prime, a=a, b=b)
    click.echo(f"y^2 = x^3 + {a}x + {b} over F{prime}")
    click.echo("O shown as (0,0)")
    click.echo(format_add_table(curve))


@cli.command("ec-orders")
@click.option("--p", "prime", type=int, default=7, show_default=True)
@click.option("--a", type=int, default=1, show_default=True)
@click.option("--b", type=int, default=3, show_default=True)
def cmd_ec_orders(prime: int, a: int, b: int) -> None:
    click.echo(format_ec_orders(EllipticCurve(p=prime, a=a, b=b)))


@cli.command("demo")
def cmd_demo() -> None:
    ctx = click.get_current_context()
    click.echo("=== 1. mult table mod 7 ===")
    click.echo(format_mult_table(7))
    click.echo("\n=== 2. orders in (Z/7Z)* ===")
    click.echo(format_mod_orders(7))
    click.echo("\n=== 3. scalar mul (lecture example) ===")
    ctx.invoke(cmd_scalar, prime=53, a=45, b=27, x=6, y=47, m=120)
    click.echo("\n=== 4. EC group law ===")
    ctx.invoke(cmd_ec_table, prime=7, a=1, b=3)
    click.echo("\n=== 5. EC point orders ===")
    ctx.invoke(cmd_ec_orders, prime=7, a=1, b=3)

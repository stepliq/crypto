from __future__ import annotations

import logging
from pathlib import Path

import click

from hmac_mac import tag_hex, verify
from integrity import check, load_catalog, protect, save_catalog

DEFAULT_KEY = "demo-secret-key"
DEFAULT_CATALOG = Path("samples/mac_catalog.json")


def configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
        force=True,
    )


def parse_key(key_text: str | None, key_hex: str | None) -> bytes:
    if key_hex is not None:
        return bytes.fromhex(key_hex)
    if key_text is not None:
        return key_text.encode("utf-8")
    raise click.ClickException("need --key or --key-hex")


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-v", "--verbose", is_flag=True)
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Lab 2.3 — HMAC-SHA256 and file integrity."""
    configure_logging(verbose)
    ctx.ensure_object(dict)


@cli.command("tag")
@click.argument("message")
@click.option("--key", default=None)
@click.option("--key-hex", default=None)
def cmd_tag(message: str, key: str | None, key_hex: str | None) -> None:
    k = parse_key(key, key_hex)
    click.echo(tag_hex(k, message.encode("utf-8")))


@cli.command("verify")
@click.argument("message")
@click.argument("tag_hex_value")
@click.option("--key", default=None)
@click.option("--key-hex", default=None)
def cmd_verify(message: str, tag_hex_value: str, key: str | None, key_hex: str | None) -> None:
    k = parse_key(key, key_hex)
    ok = verify(k, message.encode("utf-8"), tag_hex_value)
    click.echo("OK" if ok else "FAIL")
    if not ok:
        raise SystemExit(1)


@cli.command("protect")
@click.argument("files", nargs=-1, type=click.Path(path_type=Path, exists=True, dir_okay=False))
@click.option("--key", default=DEFAULT_KEY, show_default=True)
@click.option("--out", type=click.Path(path_type=Path, dir_okay=False), default=DEFAULT_CATALOG, show_default=True)
def cmd_protect(files: tuple[Path, ...], key: str, out: Path) -> None:
    if not files:
        raise click.ClickException("provide at least one file")
    catalog = protect(key.encode("utf-8"), list(files))
    save_catalog(catalog, out)
    click.echo(f"catalog saved to {out}")
    for path, mac in catalog.items():
        click.echo(f"  {path}: {mac}")


@cli.command("check")
@click.option("--catalog", type=click.Path(path_type=Path, exists=True, dir_okay=False), default=DEFAULT_CATALOG, show_default=True)
@click.option("--key", default=DEFAULT_KEY, show_default=True)
def cmd_check(catalog: Path, key: str) -> None:
    results = check(key.encode("utf-8"), load_catalog(catalog))
    failed = 0
    for item in results:
        status = "OK" if item.ok else "FAIL"
        click.echo(f"[{status}] {item.path}: {item.detail}")
        if not item.ok:
            failed += 1
    if failed:
        raise SystemExit(1)
    click.echo(f"all files intact: {len(results)}")


@cli.command("demo")
def cmd_demo() -> None:
    key = DEFAULT_KEY.encode("utf-8")
    msg = b"transfer 100 to Bob"
    mac = tag_hex(key, msg)

    click.echo("=== HMAC-SHA256 ===")
    click.echo(f"msg = {msg!r}")
    click.echo(f"tag = {mac}")
    click.echo(f"verify = {verify(key, msg, mac)}\n")

    sample_dir = Path("samples")
    sample_dir.mkdir(exist_ok=True)
    files = []
    for i in range(1, 6):
        path = sample_dir / f"file{i}.txt"
        path.write_text(f"demo content {i}\n", encoding="utf-8")
        files.append(path)

    catalog = protect(key, files)
    save_catalog(catalog, sample_dir / "mac_catalog.json")

    click.echo("=== file integrity ===")
    for path, mac_value in catalog.items():
        click.echo(f"  {path}: {mac_value}")

    click.echo("check before tamper:")
    for item in check(key, catalog):
        click.echo(f"  [{'OK' if item.ok else 'FAIL'}] {item.path}")

    files[0].write_text("TAMPERED\n", encoding="utf-8")
    click.echo("check after tamper file1.txt:")
    for item in check(key, catalog):
        click.echo(f"  [{'OK' if item.ok else 'FAIL'}] {item.path}: {item.detail}")

    # leave samples consistent for the next demo/check run
    files[0].write_text("demo content 1\n", encoding="utf-8")
    catalog = protect(key, files)
    save_catalog(catalog, sample_dir / "mac_catalog.json")

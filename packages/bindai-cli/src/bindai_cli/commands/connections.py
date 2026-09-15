from __future__ import annotations

from pathlib import Path

import typer
from bindai_config import get_provider_connection
from bindai_connections import (
    ConnectionManifest,
    KeyringProviderCredentialStore,
)
from rich.console import Console

app = typer.Typer(
    help="Manage provider connections.",
    no_args_is_help=True,
)

console = Console()


@app.command(name="add")
def add_connection(
    provider: str = typer.Argument(
        ...,
        help="Provider to connect.",
    ),
    name: str | None = typer.Option(
        None,
        "--name",
        help="Connection name. Defaults to the provider name.",
    ),
) -> None:
    """
    Store a provider credential and register its non-secret metadata.
    """
    provider_name = provider.strip().lower()

    try:
        get_provider_connection(provider_name)
    except KeyError as exc:
        raise typer.BadParameter(
            str(exc).strip("'"),
        ) from exc

    connection_name = (
        name.strip().lower()
        if name is not None
        else provider_name
    )

    if not connection_name:
        raise typer.BadParameter(
            "Connection name cannot be empty.",
        )

    credential = typer.prompt(
        "Credential",
        hide_input=True,
    )

    store = KeyringProviderCredentialStore()
    manifest = ConnectionManifest(
        Path.cwd() / ".bindai" / "connections.toml",
    )

    store.set(
        provider_name,
        credential,
    )

    manifest.add(
        connection_name,
        provider_name,
    )

    console.print(
        f'Connection "{connection_name}" added for provider '
        f'"{provider_name}".',
    )
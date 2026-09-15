from __future__ import annotations

from pathlib import Path

import typer
from bindai_config import get_provider_connection
from bindai_connections import (
    ConnectionManifest,
    KeyringProviderCredentialStore,
)
from rich.console import Console
from rich.table import Table

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


@app.command(name="list")
def list_connections() -> None:
    """
    List configured provider connections and credential status.
    """
    manifest = ConnectionManifest(
        Path.cwd() / ".bindai" / "connections.toml",
    )
    store = KeyringProviderCredentialStore()

    connections = manifest.list()

    table = Table(title="BindAI Connections")

    table.add_column("Name", style="cyan")
    table.add_column("Provider")
    table.add_column("Credential")

    for connection in connections:
        credential_status = (
            "Configured"
            if store.exists(connection.provider)
            else "Missing"
        )

        table.add_row(
            connection.name,
            connection.provider,
            credential_status,
        )

    console.print(table)


@app.command(name="remove")
def remove_connection(
    name: str = typer.Argument(
        ...,
        help="Connection name to remove.",
    ),
) -> None:
    """
    Remove a provider connection and its stored credential.
    """
    manifest = ConnectionManifest(
        Path.cwd() / ".bindai" / "connections.toml",
    )
    store = KeyringProviderCredentialStore()

    connection = manifest.get(name)

    if connection is None:
        raise typer.BadParameter(
            f'Connection "{name}" not found.',
        )

    provider_connections = [
        existing
        for existing in manifest.list()
        if existing.provider == connection.provider
        and existing.name != connection.name
    ]

    if provider_connections:
        names = ", ".join(
            existing.name
            for existing in provider_connections
        )

        raise typer.BadParameter(
            f'Cannot remove "{connection.name}" because provider '
            f'"{connection.provider}" is also used by: {names}.',
        )

    store.delete(connection.provider)
    manifest.remove(connection.name)

    console.print(
        f'Connection "{connection.name}" removed.',
    )
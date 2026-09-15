from __future__ import annotations

from pathlib import Path

import typer
from bindai_config import ProjectRuntime
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    help="Inspect BindAI project configuration.",
    no_args_is_help=True,
)

console = Console()


@app.command(
    name="list",
)
def list_config() -> None:
    """
    List effective project configuration and its source.
    """
    runtime = ProjectRuntime(Path.cwd())
    values = runtime.resolver.all()

    table = Table(
        title="Configuration",
    )

    table.add_column("Name", style="cyan")
    table.add_column("Value")
    table.add_column("Source")

    for name, config_value in values.items():
        table.add_row(
            name,
            str(config_value.value),
            config_value.source,
        )

    console.print(table)


@app.command(
    name="get",
)
def get_config(
    name: str = typer.Argument(
        ...,
        help="Configuration field to inspect.",
    ),
) -> None:
    """
    Show one effective configuration value and its source.
    """
    runtime = ProjectRuntime(Path.cwd())

    try:
        config_value = runtime.resolver.resolve(name)
    except KeyError as exc:
        raise typer.BadParameter(
            f'Unknown configuration field "{name}".',
        ) from exc

    console.print(
        f"{name} = {config_value.value}",
    )
    console.print(
        f"source = {config_value.source}",
    )
from __future__ import annotations

from dataclasses import fields
from pathlib import Path
from typing import Any, get_type_hints

import typer
from bindai_config import ProjectConfig, ProjectRuntime, TomlWriter
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    help="Inspect and modify BindAI project configuration.",
    no_args_is_help=True,
)

console = Console()


@app.command(name="list")
def list_config() -> None:
    """
    List effective project configuration and its source.
    """
    runtime = ProjectRuntime(Path.cwd())
    values = runtime.resolver.all()

    table = Table(title="Configuration")
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


@app.command(name="get")
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

    console.print(f"{name} = {config_value.value}")
    console.print(f"source = {config_value.source}")


@app.command(name="set")
def set_config(
    name: str = typer.Argument(
        ...,
        help="Configuration field to update.",
    ),
    value: str = typer.Argument(
        ...,
        help="Value to persist in bindai.toml.",
    ),
) -> None:
    """
    Set one project configuration value in bindai.toml.
    """
    config_path = Path.cwd() / "bindai.toml"

    if not config_path.exists():
        raise typer.BadParameter(
            f'No bindai.toml found in "{Path.cwd()}".',
        )

    try:
        expected_type = _field_type(name)
        converted_value = _convert_value(
            name,
            value,
            expected_type,
        )
    except KeyError as exc:
        raise typer.BadParameter(str(exc).strip("'")) from exc
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    try:
        TomlWriter().set(
            config_path,
            name,
            converted_value,
        )
    except (TypeError, ValueError) as exc:
        raise typer.BadParameter(str(exc)) from exc

    console.print(
        f'Set {name} = {converted_value!r} in {config_path.name}.',
    )


@app.command(name="path")
def config_path() -> None:
    """
    Show the path to the active bindai.toml file.
    """
    config_path = Path.cwd() / "bindai.toml"

    if not config_path.exists():
        raise typer.BadParameter(
            f'No bindai.toml found in "{Path.cwd()}".',
        )

    console.print(config_path.resolve())


def _field_type(name: str) -> type[Any]:
    config_fields = {
        field.name: field
        for field in fields(ProjectConfig)
    }

    if name not in config_fields:
        raise KeyError(
            f'Unknown configuration field "{name}".'
        )

    return get_type_hints(ProjectConfig)[name]


def _convert_value(
    name: str,
    value: str,
    expected_type: type[Any],
) -> Any:
    if expected_type is str:
        return value

    if expected_type is int:
        try:
            return int(value)
        except ValueError as exc:
            raise ValueError(
                f'Invalid value for "{name}": '
                f'expected an integer, got "{value}".',
            ) from exc

    if expected_type is float:
        try:
            return float(value)
        except ValueError as exc:
            raise ValueError(
                f'Invalid value for "{name}": '
                f'expected a number, got "{value}".',
            ) from exc

    if expected_type is bool:
        normalized = value.strip().lower()

        if normalized in {"1", "true", "yes", "on"}:
            return True

        if normalized in {"0", "false", "no", "off"}:
            return False

        raise ValueError(
            f'Invalid value for "{name}": '
            f'expected a boolean, got "{value}".',
        )

    raise ValueError(
        f'Unsupported configuration type for "{name}".',
    )
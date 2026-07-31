from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from bindai_cli.inspectors.project import ProjectInspector

app = typer.Typer(
    invoke_without_command=True,
)

console = Console()


@app.callback()
def inspect():

    inspector = ProjectInspector(
        Path.cwd(),
    )

    data = inspector.inspect()

    table = Table(
        title="Project Inspection",
    )

    table.add_column("Component")
    table.add_column("Count")
    table.add_column("Items")

    for key, values in data.items():
        table.add_row(
            key.capitalize(),
            str(len(values)),
            ", ".join(values) if values else "-",
        )

    console.print(table)

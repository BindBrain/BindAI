from pathlib import Path

import typer
from rich import print

from bindai_cli.utils.scaffold import copy_scaffold

app = typer.Typer(
    invoke_without_command=True,
)


@app.callback()
def new(
    name: str,
):
    """
    Create a new BindAI project.
    """

    root = Path(name)

    if root.exists():
        print(f"[red]Project '{name}' already exists.[/red]")
        raise typer.Exit(1)

    scaffold = (
        Path(__file__)
        .parent.parent
        / "scaffolds"
        / "basic"
    )

    copy_scaffold(
        scaffold,
        root,
    )

    print(f"[green]✓ Project '{name}' created successfully.[/green]")
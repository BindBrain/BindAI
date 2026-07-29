from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import typer
from rich import print

app = typer.Typer(
    invoke_without_command=True,
)


@app.callback()
def run():
    """
    Run the current BindAI project.
    """

    project = Path.cwd()

    config = project / "bindai.toml"

    if not config.exists():
        print("[red]bindai.toml not found.[/red]")
        raise typer.Exit(1)

    main = project / "main.py"

    if not main.exists():
        print("[red]main.py not found.[/red]")
        raise typer.Exit(1)

    subprocess.run(
        [
            sys.executable,
            str(main),
        ],
        check=True,
    )
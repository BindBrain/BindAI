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

    main = project / "main.py"

    workflow = project / "workflow.py"

    # Full BindAI project
    if config.exists():
        if not main.exists():
            print("[red]main.py not found.[/red]")

            raise typer.Exit(1)

        target = main

    # Template / example / demo
    elif main.exists():
        target = main

    # Future workflow entrypoint
    elif workflow.exists():
        target = workflow

    else:
        print("[red]Nothing to run.[/red]")

        print()

        print("Expected one of:")

        print("  • bindai.toml")

        print("  • main.py")

        print("  • workflow.py")

        raise typer.Exit(1)

    subprocess.run(
        [
            sys.executable,
            str(target),
        ],
        check=True,
    )

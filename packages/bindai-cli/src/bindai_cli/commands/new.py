import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console

from bindai_cli.utils.scaffold import copy_scaffold

console = Console()

app = typer.Typer(
    invoke_without_command=True,
)


@app.callback()
def new(
    name: str,
    install: bool = typer.Option(
        False,
        "--install",
        help="Install dependencies.",
    ),
):
    """
    Create a new BindAI project.
    """

    root = Path(name)

    if root.exists():
        console.print(
            f"[red]Project '{name}' already exists.[/red]"
        )
        raise typer.Exit(1)

    scaffold = Path(__file__).parent.parent / "scaffolds" / "basic"

    copy_scaffold(
        scaffold,
        root,
    )

    console.print("[cyan]Creating virtual environment...[/cyan]")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "venv",
            str(root / ".venv"),
        ],
        check=False,
    )

    print()

    console.print(
        f"[green]✓ Project '{name}' created successfully.[/green]"
    )

    console.print()

    console.print("[bold]Next steps:[/bold]")

    console.print(f"  cd {name}")
    console.print("  .venv\\Scripts\\activate")
    console.print("  pip install -r requirements.txt")
    console.print("  bindai doctor")
    console.print("  python main.py")

    if install:
        subprocess.run(
            [
                str(root / ".venv" / "Scripts" / "python"),
                "-m",
                "pip",
                "install",
                "-r",
                str(root / "requirements.txt"),
            ],
            check=False,
        )

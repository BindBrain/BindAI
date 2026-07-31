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
        print(f"[red]Project '{name}' already exists.[/red]")
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

    print(f"[green]✓ Project '{name}' created successfully.[/green]")

    print()

    print("[bold]Next steps:[/bold]")

    print(f"  cd {name}")

    print("  .venv\\Scripts\\activate")

    print("  pip install -r requirements.txt")

    print("  bindai doctor")

    print("  python main.py")

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

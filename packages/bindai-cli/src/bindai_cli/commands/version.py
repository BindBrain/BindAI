import typer

from bindai_cli import __version__

app = typer.Typer(
    invoke_without_command=True,
)


@app.callback()
def version():
    """
    Show installed BindAI version.
    """
    typer.echo(f"BindAI CLI {__version__}")
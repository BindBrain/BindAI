import typer

app = typer.Typer(
    invoke_without_command=True,
)


@app.callback()
def version():
    """
    Show installed BindAI version.
    """
    typer.echo("BindAI CLI 0.1.0")

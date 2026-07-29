import typer

from bindai_cli.commands.version import app as version_app
from bindai_cli.commands.doctor import app as doctor_app
from bindai_cli.commands.new import app as new_app
from bindai_cli.commands.run import app as run_app
from bindai_cli.commands.template import app as template_app

app = typer.Typer(
    help="BindAI Command Line Interface",
    no_args_is_help=True,
)

app.add_typer(
    version_app,
    name="version",
)

app.add_typer(
    doctor_app,
    name="doctor",
)

app.add_typer(
    new_app,
    name="new",
)

app.add_typer(
    run_app,
    name="run",
)

app.add_typer(
    template_app,
    name="template",
)
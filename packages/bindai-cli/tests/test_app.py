from bindai_cli.app import app
from typer.testing import CliRunner

runner = CliRunner()


def test_help_lists_commands():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "doctor" in result.stdout
    assert "new" in result.stdout
    assert "run" in result.stdout
    assert "template" in result.stdout
    assert "workflow" in result.stdout
    assert "inspect" in result.stdout
    assert "version" in result.stdout


def test_version_command():
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "BindAI CLI 0.2.1"
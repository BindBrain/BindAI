from pathlib import Path

from bindai_cli.app import app
from typer.testing import CliRunner

runner = CliRunner()


def test_workflow_run_requires_workflow_path(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr(
        "bindai_cli.commands.workflow.subprocess.run",
        fake_run,
    )

    result = runner.invoke(
        app,
        ["workflow", "run"],
    )

    assert result.exit_code != 0
    assert "Missing argument" in result.output
    assert calls == []
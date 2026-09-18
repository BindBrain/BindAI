import os
import sys
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


def test_workflow_validate_uses_visible_check_mark(
    tmp_path: Path,
):
    workflow_file = tmp_path / "workflow.py"
    workflow_file.write_text(
        "from bindai import WorkflowBuilder\n\n"
        "workflow = (\n"
        '    WorkflowBuilder("test")\n'
        "    .start_node()\n"
        "    .end_node()\n"
        "    .build()\n"
        ")\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["workflow", "validate", str(workflow_file)],
    )

    assert result.exit_code == 0
    assert "✓ Workflow is valid." in result.output


def test_workflow_run_forwards_arguments_and_project_root(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    workflow_file = tmp_path / "workflow.py"
    workflow_file.write_text(
        "",
        encoding="utf-8",
    )

    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr(
        "bindai_cli.commands.workflow.subprocess.run",
        fake_run,
    )

    result = runner.invoke(
        app,
        [
            "workflow",
            "run",
            str(workflow_file),
            "hello",
            "world",
        ],
    )

    assert result.exit_code == 0
    assert calls[0][0] == (
        [
            sys.executable,
            str(workflow_file),
            "hello",
            "world",
        ],
    )
    assert calls[0][1]["check"] is True

    pythonpath = calls[0][1]["env"]["PYTHONPATH"]
    assert pythonpath.split(os.pathsep)[0] == str(tmp_path)

def test_workflow_name_resolves_to_workflow_file(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    workflows_dir = tmp_path / "workflows"
    workflows_dir.mkdir()

    workflow_file = workflows_dir / "research.py"
    workflow_file.write_text(
        "",
        encoding="utf-8",
    )

    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr(
        "bindai_cli.commands.workflow.subprocess.run",
        fake_run,
    )

    result = runner.invoke(
        app,
        [
            "workflow",
            "research",
            "hello",
        ],
    )

    assert result.exit_code == 0
    assert calls[0][0] == (
        [
            sys.executable,
            str(workflow_file),
            "hello",
        ],
    )
    assert calls[0][1]["check"] is True

    pythonpath = calls[0][1]["env"]["PYTHONPATH"]
    assert pythonpath.split(os.pathsep)[0] == str(tmp_path)
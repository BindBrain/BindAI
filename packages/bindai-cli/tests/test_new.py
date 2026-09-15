import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from bindai_cli.app import app
from bindai_cli.commands.new import _activation_command, _venv_python
from typer.testing import CliRunner

runner = CliRunner()


def test_venv_python_windows(monkeypatch, tmp_path):
    monkeypatch.setattr("bindai_cli.commands.new.os.name", "nt")

    assert _venv_python(tmp_path) == tmp_path / ".venv" / "Scripts" / "python"


def test_venv_python_posix(monkeypatch, tmp_path):
    monkeypatch.setattr("bindai_cli.commands.new.os.name", "posix")

    assert _venv_python(tmp_path) == tmp_path / ".venv" / "bin" / "python"


def test_activation_command_windows(monkeypatch):
    monkeypatch.setattr("bindai_cli.commands.new.os.name", "nt")

    assert _activation_command() == ".venv\\Scripts\\activate"


def test_activation_command_posix(monkeypatch):
    monkeypatch.setattr("bindai_cli.commands.new.os.name", "posix")

    assert _activation_command() == "source .venv/bin/activate"


def test_new_creates_project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["new", "demo"])

    assert result.exit_code == 0
    assert "Project 'demo' created successfully." in result.output

    project = tmp_path / "demo"
    assert project.is_dir()
    assert (project / "main.py").is_file()
    assert (project / "requirements.txt").is_file()


def test_new_rejects_existing_project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    project = tmp_path / "demo"
    project.mkdir()

    result = runner.invoke(app, ["new", "demo"])

    assert result.exit_code != 0
    assert "already exists" in result.output.lower()


def test_new_accepts_install_after_name(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def fake_run(command, check):
        assert check is True

    with patch(
        "bindai_cli.commands.new.subprocess.run",
        side_effect=fake_run,
    ):
        result = runner.invoke(app, ["new", "demo", "--install"])

    assert result.exit_code == 0
    assert "Project 'demo' created successfully." in result.output


def test_new_accepts_install_before_name(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def fake_run(command, check):
        assert check is True

    with patch(
        "bindai_cli.commands.new.subprocess.run",
        side_effect=fake_run,
    ):
        result = runner.invoke(app, ["new", "--install", "demo"])

    assert result.exit_code == 0
    assert "Project 'demo' created successfully." in result.output


def test_new_reports_venv_creation_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def fail_run(command, check):
        raise subprocess.CalledProcessError(1, command)

    with patch(
        "bindai_cli.commands.new.subprocess.run",
        side_effect=fail_run,
    ):
        result = runner.invoke(app, ["new", "demo"])

    assert result.exit_code == 1
    assert "Failed to create the virtual environment." in result.output

    project = tmp_path / "demo"
    assert project.is_dir()


def test_new_reports_dependency_install_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    calls = []

    def fail_install(command, check):
        calls.append(command)

        if len(calls) == 2:
            raise subprocess.CalledProcessError(1, command)

    with patch(
        "bindai_cli.commands.new.subprocess.run",
        side_effect=fail_install,
    ):
        result = runner.invoke(app, ["new", "demo", "--install"])

    assert result.exit_code == 1
    assert "Failed to install project dependencies." in result.output
    assert len(calls) == 2

    project = tmp_path / "demo"
    assert project.is_dir()

def test_new_install_uses_project_python(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    commands = []

    def fake_run(command, check):
        commands.append(command)
        assert check is True

    with patch(
        "bindai_cli.commands.new.subprocess.run",
        side_effect=fake_run,
    ):
        result = runner.invoke(app, ["new", "demo", "--install"])

    assert result.exit_code == 0
    assert len(commands) == 2

    assert commands[0] == [
        sys.executable,
        "-m",
        "venv",
        str(Path("demo") / ".venv"),
    ]

    assert commands[1] == [
        str(Path("demo") / ".venv" / "Scripts" / "python"),
        "-m",
        "pip",
        "install",
        "-r",
        str(Path("demo") / "requirements.txt"),
    ]

def test_new_generates_expected_requirements(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["new", "demo"])

    assert result.exit_code == 0

    requirements = (
        tmp_path / "demo" / "requirements.txt"
    ).read_text(encoding="utf-8")

    assert "bindai>=0.1.3" in requirements


def test_new_does_not_install_without_flag(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with patch("bindai_cli.commands.new.subprocess.run") as run:
        result = runner.invoke(app, ["new", "demo"])

    assert result.exit_code == 0
    run.assert_called_once()


def test_new_preserves_generated_project_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["new", "demo"])

    assert result.exit_code == 0

    project = Path(tmp_path / "demo")

    assert (project / "main.py").exists()
    assert (project / "requirements.txt").exists()

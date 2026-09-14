import os
import subprocess

from typer.testing import CliRunner

from bindai_cli.commands.new import app, _activation_command, _venv_python

runner = CliRunner()


def test_new_creates_project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def fake_run(*args, **kwargs):
        assert kwargs["check"] is True
        return None

    monkeypatch.setattr(
        "bindai_cli.commands.new.subprocess.run",
        fake_run,
    )

    result = runner.invoke(app, ["demo"])

    assert result.exit_code == 0
    assert "created successfully" in result.stdout

    project = tmp_path / "demo"

    assert project.exists()
    assert (project / "main.py").exists()
    assert (project / "README.md").exists()
    assert (project / "bindai.toml").exists()
    assert (project / ".env").exists()


def test_new_rejects_existing_project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    project = tmp_path / "existing"
    project.mkdir()

    result = runner.invoke(app, ["existing"])

    assert result.exit_code == 1
    assert "already exists" in result.stdout


def test_new_replaces_project_name_placeholder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "bindai_cli.commands.new.subprocess.run",
        lambda *args, **kwargs: None,
    )

    result = runner.invoke(app, ["my-agent"])

    assert result.exit_code == 0

    project = tmp_path / "my-agent"

    bindai_toml = (project / "bindai.toml").read_text(
        encoding="utf-8",
    )

    assert "my-agent" in bindai_toml
    assert "{{ project_name }}" not in bindai_toml
    assert "{{PROJECT_NAME}}" not in bindai_toml


def test_new_reports_virtual_environment_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def fail_run(*args, **kwargs):
        assert kwargs["check"] is True
        raise subprocess.CalledProcessError(
            returncode=1,
            cmd=args[0],
        )

    monkeypatch.setattr(
        "bindai_cli.commands.new.subprocess.run",
        fail_run,
    )

    result = runner.invoke(app, ["demo"])

    assert result.exit_code == 1
    assert "Failed to create the virtual environment" in result.stdout
    assert "setup is incomplete" in result.stdout
    assert "created successfully" not in result.stdout
    assert (tmp_path / "demo").exists()


def test_new_reports_dependency_install_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    calls = []

    def fail_install(args, **kwargs):
        assert kwargs["check"] is True
        calls.append(args)

        if len(calls) == 1:
            return None

        raise subprocess.CalledProcessError(
            returncode=1,
            cmd=args,
        )

    monkeypatch.setattr(
        "bindai_cli.commands.new.subprocess.run",
        fail_install,
    )

    result = runner.invoke(app, ["--install", "demo"])

    assert result.exit_code == 1
    assert "Failed to install project dependencies" in result.stdout
    assert "setup is incomplete" in result.stdout
    assert "created successfully" not in result.stdout
    assert len(calls) == 2
    assert (tmp_path / "demo").exists()


def test_venv_python_uses_windows_layout(tmp_path, monkeypatch):
    monkeypatch.setattr("bindai_cli.commands.new.os.name", "nt")

    assert _venv_python(tmp_path) == (
        tmp_path / ".venv" / "Scripts" / "python"
    )


def test_venv_python_uses_posix_layout(tmp_path, monkeypatch):
    monkeypatch.setattr("bindai_cli.commands.new.os.name", "posix")

    assert _venv_python(tmp_path) == (
        tmp_path / ".venv" / "bin" / "python"
    )


def test_activation_command_uses_windows_layout(monkeypatch):
    monkeypatch.setattr("bindai_cli.commands.new.os.name", "nt")

    assert _activation_command() == ".venv\\Scripts\\activate"


def test_activation_command_uses_posix_layout(monkeypatch):
    monkeypatch.setattr("bindai_cli.commands.new.os.name", "posix")

    assert _activation_command() == "source .venv/bin/activate"
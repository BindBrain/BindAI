from pathlib import Path

from typer.testing import CliRunner

from bindai_cli.commands.new import app


runner = CliRunner()


def test_new_creates_project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def fake_run(*args, **kwargs):
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

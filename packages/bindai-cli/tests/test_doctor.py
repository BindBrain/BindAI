from pathlib import Path

from bindai_cli.commands.doctor import app
from bindai_connections import (
    ConnectionManifest,
    KeyringProviderCredentialStore,
)
from typer.testing import CliRunner

runner = CliRunner()


def test_doctor_without_project_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OLLAMA_HOST", raising=False)

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "BindAI Doctor" in result.stdout
    assert "Python" in result.stdout
    assert "Virtual Environment" in result.stdout
    assert "Templates" in result.stdout
    assert "Providers" in result.stdout
    assert "OPENAI_API_KEY" in result.stdout
    assert "ANTHROPIC_API_KEY" in result.stdout
    assert "OLLAMA_HOST" in result.stdout


def test_doctor_reports_environment_variables(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("OLLAMA_HOST", "http://localhost:11434")

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "OPENAI_API_KEY" in result.stdout
    assert "ANTHROPIC_API_KEY" in result.stdout
    assert "OLLAMA_HOST" in result.stdout
    assert "http://localhost:11434" in result.stdout


def test_doctor_reports_project_configuration(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "bindai.toml").write_text(
        """
name = "test-project"
provider = "openai"
connection = "work"
model = "gpt-4o-mini"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "test-project" in result.stdout
    assert "openai" in result.stdout
    assert "gpt-4o-mini" in result.stdout
    assert "Connection" in result.stdout
    assert "work" in result.stdout
    assert "Connection not configured" in result.stdout


def test_doctor_reports_configured_connection(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "bindai.toml").write_text(
        """
name = "test-project"
provider = "openai"
connection = "work"
model = "gpt-4.1-mini"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    manifest = ConnectionManifest(
        tmp_path / ".bindai" / "connections.toml",
    )
    manifest.add("work", "openai")

    monkeypatch.setattr(
        KeyringProviderCredentialStore,
        "exists",
        lambda self, name: True,
    )

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "Connection" in result.stdout
    assert "work" in result.stdout
    assert "Connection Credential" in result.stdout
    assert "Configured" in result.stdout


def test_doctor_reports_unknown_connection(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "bindai.toml").write_text(
        """
name = "test-project"
provider = "openai"
connection = "doesnotexist"
model = "gpt-4.1-mini"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "Connection" in result.stdout
    assert "doesnotexist" in result.stdout
    assert "Connection not configured" in result.stdout


def test_doctor_reports_missing_connection_credential(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "bindai.toml").write_text(
        """
name = "test-project"
provider = "openai"
connection = "work"
model = "gpt-4.1-mini"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    manifest = ConnectionManifest(
        tmp_path / ".bindai" / "connections.toml",
    )
    manifest.add("work", "openai")

    monkeypatch.setattr(
        KeyringProviderCredentialStore,
        "exists",
        lambda self, name: False,
    )

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "Connection" in result.stdout
    assert "work" in result.stdout
    assert "Connection Credential" in result.stdout
    assert "Missing" in result.stdout

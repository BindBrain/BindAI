from bindai_cli.commands.run import app
from typer.testing import CliRunner

runner = CliRunner()


def test_run_uses_main_py_for_bindai_project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "bindai.toml").write_text(
        'name = "test-project"\n',
        encoding="utf-8",
    )
    (tmp_path / "main.py").write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr(
        "bindai_cli.commands.run.subprocess.run",
        fake_run,
    )

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert len(calls) == 1

    command = calls[0][0][0]

    assert command[0]
    assert command[1] == str(tmp_path / "main.py")
    assert calls[0][1]["check"] is True


def test_run_uses_main_py_when_no_config_exists(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "main.py").write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr(
        "bindai_cli.commands.run.subprocess.run",
        fake_run,
    )

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert len(calls) == 1
    assert calls[0][0][0][1] == str(tmp_path / "main.py")


def test_run_uses_workflow_py_as_fallback(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "workflow.py").write_text(
        "print('workflow')\n",
        encoding="utf-8",
    )

    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr(
        "bindai_cli.commands.run.subprocess.run",
        fake_run,
    )

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert len(calls) == 1
    assert calls[0][0][0][1] == str(tmp_path / "workflow.py")


def test_run_fails_when_bindai_project_has_no_main(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "bindai.toml").write_text(
        'name = "test-project"\n',
        encoding="utf-8",
    )

    result = runner.invoke(app)

    assert result.exit_code == 1
    assert "main.py not found" in result.stdout


def test_run_fails_when_nothing_can_be_run(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app)

    assert result.exit_code == 1
    assert "Nothing to run" in result.stdout
    assert "bindai.toml" in result.stdout
    assert "main.py" in result.stdout
    assert "workflow.py" in result.stdout

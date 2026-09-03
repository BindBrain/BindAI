import json

from bindai_cli.templates.validator import TemplateValidator


def test_validator_accepts_valid_template(tmp_path):
    (tmp_path / "README.md").write_text("# Test\n", encoding="utf-8")
    (tmp_path / "main.py").write_text("print('hello')\n", encoding="utf-8")

    metadata = {
        "name": "test-template",
        "version": "0.1.0",
        "category": "agent",
        "description": "A test template.",
    }

    (tmp_path / "template.json").write_text(
        json.dumps(metadata),
        encoding="utf-8",
    )

    errors = TemplateValidator.validate(tmp_path)

    assert errors == []


def test_validator_reports_missing_required_files(tmp_path):
    errors = TemplateValidator.validate(tmp_path)

    assert "Missing required file: README.md" in errors
    assert "Missing required file: main.py" in errors


def test_validator_reports_missing_metadata_fields(tmp_path):
    (tmp_path / "README.md").write_text("# Test\n", encoding="utf-8")
    (tmp_path / "main.py").write_text("print('hello')\n", encoding="utf-8")

    metadata = {
        "name": "test-template",
    }

    (tmp_path / "template.json").write_text(
        json.dumps(metadata),
        encoding="utf-8",
    )

    errors = TemplateValidator.validate(tmp_path)

    assert "template.json missing 'version'." in errors
    assert "template.json missing 'category'." in errors
    assert "template.json missing 'description'." in errors


def test_validator_reports_invalid_metadata(tmp_path):
    (tmp_path / "README.md").write_text("# Test\n", encoding="utf-8")
    (tmp_path / "main.py").write_text("print('hello')\n", encoding="utf-8")
    (tmp_path / "template.json").write_text(
        "{ invalid json",
        encoding="utf-8",
    )

    errors = TemplateValidator.validate(tmp_path)

    assert errors == ["Invalid template.json"]

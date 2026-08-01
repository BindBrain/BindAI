import tomllib
from pathlib import Path

ROOT = Path("packages")

required = [
    "name",
    "version",
    "requires-python",
]

optional = [
    "description",
    "readme",
    "license",
    "authors",
]

print()

for pyproject in ROOT.rglob("pyproject.toml"):
    print("=" * 70)
    print(pyproject)

    with open(pyproject, "rb") as f:
        data = tomllib.load(f)

    project = data.get("project", {})

    for field in required:
        if field not in project:
            print(f"❌ missing: {field}")

    for field in optional:
        if field not in project:
            print(f"⚠ optional missing: {field}")

print()
print("Done.")

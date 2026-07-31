from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
PACKAGES = ROOT / "packages"


def find_packages():
    return sorted(PACKAGES.rglob("pyproject.toml"))


def build_package(pyproject):
    package_dir = pyproject.parent

    print("=" * 70)
    print(f"Building: {package_dir}")

    result = subprocess.run(
        [
            "uv",
            "build",
            str(package_dir),
        ],
        cwd=ROOT,
    )

    return result.returncode == 0


def main():
    failures = []

    for pyproject in find_packages():
        if not build_package(pyproject):
            failures.append(pyproject.parent)

    print()
    print("=" * 70)

    if failures:
        print("FAILED PACKAGES:")
        for package in failures:
            print(f" - {package}")

        sys.exit(1)

    print("All packages built successfully.")


if __name__ == "__main__":
    main()
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


COMMANDS = {
    "audit": "audit_packages.py",
    "build": "build_packages.py",
    "clean": "clean.py",
    "playground": "run_playground_tests.py",
}


def run(script: str) -> int:
    return subprocess.call(
        [sys.executable, str(Path(__file__).parent / script)],
        cwd=ROOT,
    )


def main() -> None:
    if len(sys.argv) < 2:
        print("Available commands:")
        for command in sorted(COMMANDS):
            print(f"  {command}")
        sys.exit(1)

    command = sys.argv[1]

    if command not in COMMANDS:
        print(f"Unknown command: {command}")
        sys.exit(1)

    raise SystemExit(run(COMMANDS[command]))


if __name__ == "__main__":
    main()

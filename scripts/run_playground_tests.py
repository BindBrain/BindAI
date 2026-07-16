from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAYGROUND = ROOT / "playground"


def main():

    tests = sorted(
        PLAYGROUND.glob("*_test.py")
    )

    passed = []
    failed = []

    print("=" * 70)
    print("Running BindAI playground tests")
    print("=" * 70)

    for test in tests:

        print(f"\nRunning {test.name}...")

        result = subprocess.run(
            [sys.executable, str(test)],
            cwd=ROOT,
        )

        if result.returncode == 0:
            print("PASS")
            passed.append(test.name)
        else:
            print("FAIL")
            failed.append(test.name)

    print("\n" + "=" * 70)

    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")

    if failed:

        print("\nFailed tests:")

        for name in failed:
            print(f" - {name}")

        sys.exit(1)

    print("\nAll playground tests passed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
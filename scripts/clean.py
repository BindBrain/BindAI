from pathlib import Path
import shutil

root = Path(".")

for path in root.rglob("__pycache__"):
    shutil.rmtree(path)

for path in root.rglob("*.pyc"):
    path.unlink()

print("Cache removed.")
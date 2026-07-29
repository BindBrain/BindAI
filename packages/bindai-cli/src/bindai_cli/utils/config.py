from __future__ import annotations

from pathlib import Path
import tomllib


def load_config() -> dict:
    path = Path("bindai.toml")

    if not path.exists():
        return {}

    with path.open("rb") as f:
        return tomllib.load(f)
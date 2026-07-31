from __future__ import annotations

from pathlib import Path

from bindai_config import ProjectRuntime


def load_config():

    runtime = ProjectRuntime(
        Path.cwd(),
    )

    return runtime.config

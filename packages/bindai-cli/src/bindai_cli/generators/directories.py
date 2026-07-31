from pathlib import Path

DIRECTORIES = [
    "agents",
    "knowledge",
    "memory",
    "templates",
    "tools",
    "workflows",
    "tests",
]


def generate_directories(root: Path):
    for directory in DIRECTORIES:
        path = root / directory

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        (path / ".gitkeep").touch()
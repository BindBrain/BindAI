from dataclasses import dataclass


@dataclass(slots=True)
class ToolMetadata:

    name: str

    description: str

    version: str = "1.0"

    tags: list[str] | None = None
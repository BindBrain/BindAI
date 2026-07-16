from dataclasses import dataclass


@dataclass(slots=True)
class ToolParameter:

    name: str

    type: str

    description: str = ""

    required: bool = True
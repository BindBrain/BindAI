from dataclasses import dataclass


@dataclass(slots=True)
class GraphEdge:
    source: str

    target: str

    condition: str | None = None

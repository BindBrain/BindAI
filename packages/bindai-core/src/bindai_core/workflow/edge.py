from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class WorkflowEdge:
    """
    Connection between two workflow nodes.
    """

    source: str

    target: str
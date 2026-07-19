from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CompensationAction:
    """
    Action executed when
    rolling back a workflow.
    """

    node_id: str

    action: callable
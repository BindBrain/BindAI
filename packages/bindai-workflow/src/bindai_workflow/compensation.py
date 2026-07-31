from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class CompensationAction:
    """
    Action executed when
    rolling back a workflow.
    """

    node_id: str

    action: Callable[..., Any]

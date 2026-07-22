from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TimeoutPolicy:
    """
    Maximum execution time.
    """

    seconds: int

    fail_workflow: bool = True

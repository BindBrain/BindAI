from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RetryPolicy:
    """
    Retry configuration.
    """

    max_attempts: int = 3

    delay_seconds: int = 5

    exponential_backoff: bool = True
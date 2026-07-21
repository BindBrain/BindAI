from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class LLMResult:
    """
    Result returned by an LLM provider.
    """

    success: bool

    value: str | None = None

    error: str | None = None

    usage: dict | None = None
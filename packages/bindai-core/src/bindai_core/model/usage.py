from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TokenUsage:
    """
    Token accounting.
    """

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

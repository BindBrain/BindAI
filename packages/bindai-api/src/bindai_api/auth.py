from __future__ import annotations

import hmac
import os

from fastapi import Header, HTTPException, status


def require_api_key(
    authorization: str | None = Header(default=None),
) -> None:
    configured_key = os.getenv("BINDAI_API_KEY")

    if not configured_key:
        raise RuntimeError("BINDAI_API_KEY is not configured.")

    expected = f"Bearer {configured_key}"

    if not hmac.compare_digest(authorization or "", expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
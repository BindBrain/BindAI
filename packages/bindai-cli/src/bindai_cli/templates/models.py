from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Template:
    name: str

    title: str

    description: str

    version: str

    author: str

    category: str

    status: str

    tags: list[str]

    path: str

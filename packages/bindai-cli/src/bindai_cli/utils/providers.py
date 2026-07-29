from __future__ import annotations

from importlib.metadata import distributions


def installed_providers() -> list[str]:
    """
    Return installed BindAI provider packages.
    """

    providers: set[str] = set()

    for dist in distributions():
        name = dist.metadata.get("Name")

        if not name:
            continue

        if name.startswith("bindai-provider-"):
            providers.add(name)

    return sorted(providers)
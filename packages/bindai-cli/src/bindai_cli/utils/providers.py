from __future__ import annotations

from bindai_providers import ProviderRegistry


def installed_providers():

    return ProviderRegistry.list()

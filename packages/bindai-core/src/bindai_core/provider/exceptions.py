from __future__ import annotations


class ProviderException(Exception):
    """
    Base provider exception.
    """


class ProviderNotFound(
    ProviderException,
):

    def __init__(
        self,
        name: str,
    ):
        super().__init__(
            f"Provider '{name}' is not registered."
        )


class ProviderAlreadyRegistered(
    ProviderException,
):

    def __init__(
        self,
        name: str,
    ):
        super().__init__(
            f"Provider '{name}' is already registered."
        )


class DefaultProviderNotConfigured(
    ProviderException,
):

    def __init__(self):
        super().__init__(
            "No default provider configured."
        )
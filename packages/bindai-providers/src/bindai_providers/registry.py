from __future__ import annotations


class ProviderRegistry:
    """
    Registry for model providers.
    """

    _providers: dict[str, object] = {}

    @classmethod
    def register(
        cls,
        name: str,
        builder,
    ):

        cls._providers[name] = builder

    @classmethod
    def create(
        cls,
        name: str,
        **kwargs,
    ):

        try:
            builder = cls._providers[name]

        except KeyError as exc:
            raise ValueError(
                f"Unknown provider '{name}'."
            ) from exc

        return builder(**kwargs)

    @classmethod
    def names(
        cls,
    ) -> list[str]:

        return sorted(cls._providers.keys())
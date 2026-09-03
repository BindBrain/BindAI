from __future__ import annotations


def bootstrap() -> None:
    providers = [
        "bindai_provider_openai",
        "bindai_provider_anthropic",
        "bindai_provider_google",
    ]

    for module_name in providers:
        try:
            module = __import__(
                module_name,
                fromlist=["register"],
            )
        except ModuleNotFoundError as exc:
            if exc.name == module_name:
                continue

            raise

        register = getattr(module, "register", None)

        if register is None:
            continue

        register()
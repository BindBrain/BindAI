from __future__ import annotations


def bootstrap():

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

            module.register()

        except ImportError:
            pass

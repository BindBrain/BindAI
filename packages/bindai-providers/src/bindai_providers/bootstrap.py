def bootstrap():

    try:
        from bindai_provider_openai import register
        register()
    except ImportError:
        pass

    try:
        from bindai_provider_anthropic import register
        register()
    except ImportError:
        pass

    try:
        from bindai_provider_google import register
        register()
    except ImportError:
        pass
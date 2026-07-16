def tool(name: str | None = None):
    """
    Placeholder decorator.

    In future milestones this will expose metadata,
    schemas, and automatic registration.
    """

    def wrapper(obj):

        obj.__tool_name__ = name or obj.__name__

        return obj

    return wrapper
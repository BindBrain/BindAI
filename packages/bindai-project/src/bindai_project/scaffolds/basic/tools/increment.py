from bindai_tool import tool


@tool
def increment(
    value: int,
) -> int:
    return value + 1

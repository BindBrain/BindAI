from bindai_tool import tool


@tool
def echo(
    text: str,
) -> str:
    return text

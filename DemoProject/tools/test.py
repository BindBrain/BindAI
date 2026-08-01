from bindai_tool import tool


@tool
def hello() -> str:
    return "Hello from auto-loaded tool!"

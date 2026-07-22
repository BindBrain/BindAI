from bindai_core.tool import tool


@tool()
def add(
    a: int,
    b: int,
):
    """Add two numbers."""

    return a + b


print(add)
print(add.name)
print(add.description)
print(add.parameters)
print(add.execute(a=2, b=3))

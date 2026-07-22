from bindai_core.tool import tool


@tool(description="Say hello")
def hello(name: str):

    return f"Hello {name}"


print(hello("BindAI"))

print(hello.__metadata__)

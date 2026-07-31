from bindai_tool import tool


@tool
def weather(city: str):
    return f"Weather for {city}"

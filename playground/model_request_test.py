from bindai_core import ModelRequest

request = ModelRequest(
    temperature=0.2,
    max_tokens=500,
    top_p=0.95,
    stream=True,
)

print(request)
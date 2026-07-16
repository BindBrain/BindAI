from bindai_core import (
    Message,
    MessageRole,
    ModelRequest,
)

request = ModelRequest(
    messages=[
        Message(
            role=MessageRole.USER,
            content="Hello BindAI"
        )
    ]
)

print(request.messages[0].role.value)
print(request.messages[0].content)
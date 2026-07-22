from bindai_core import PromptTemplate


template = PromptTemplate(
    """
You are {{role}}.

User:
{{input}}

Language:
{{language}}
"""
)

print(template.variables())

print()

print(
    template.render(
        role="Assistant",
        input="Hello!",
        language="English",
    )
)

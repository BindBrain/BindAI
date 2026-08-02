from dataclasses import dataclass

from bindai import AgentBuilder


@dataclass
class Person:
    name: str
    age: int
    occupation: str


agent = (
    AgentBuilder()
    .name("Structured Assistant")
    .instructions("Return structured data matching the requested schema.")
    .openai(
        model="gpt-5",
    )
    .build()
)

print("=" * 60)
print("Structured Output")
print("=" * 60)

result = agent.chat(
    "Extract: John is a 32 year old software engineer.",
    output=Person,
)

print("Success:")
print(result.success)

print()

print("Output:")
print(result.output)

from bindai_prompts import Prompt
from bindai_prompts import PromptTemplate


def test_template():

    template = PromptTemplate(
        Prompt(
            system="You are ${role}.",
            user="Hello ${name}",
        )
    )

    prompt = template.render(
        role="assistant",
        name="John",
    )

    assert prompt.system == "You are assistant."
    assert prompt.user == "Hello John"
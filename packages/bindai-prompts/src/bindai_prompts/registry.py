from .prompt import Prompt


class PromptRegistry:
    _prompts: dict[str, Prompt] = {}

    @classmethod
    def register(
        cls,
        name,
        prompt,
    ):
        cls._prompts[name] = prompt

    @classmethod
    def get(
        cls,
        name,
    ):
        return cls._prompts[name]

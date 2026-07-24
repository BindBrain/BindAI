class PromptRegistry:

    _prompts = {}

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
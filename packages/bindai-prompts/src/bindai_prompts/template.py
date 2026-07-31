from string import Template

from .prompt import Prompt


class PromptTemplate:
    def __init__(
        self,
        prompt: Prompt,
    ):
        self.prompt = prompt

    def render(
        self,
        **kwargs,
    ) -> Prompt:

        return Prompt(
            system=Template(
                self.prompt.system or "",
            ).safe_substitute(**kwargs),
            user=Template(
                self.prompt.user,
            ).safe_substitute(**kwargs),
            assistant=Template(
                self.prompt.assistant or "",
            ).safe_substitute(**kwargs),
        )

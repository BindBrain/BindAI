from __future__ import annotations

import re


class PromptTemplate:
    """
    Represents a prompt template.
    """

    def __init__(
        self,
        template: str,
    ):
        self.template = template

    def variables(
        self,
    ) -> list[str]:
        """
        Returns every variable used by the template.

        Example:

        Hello {{name}}

        -> ["name"]
        """

        matches = re.findall(
            r"\{\{(.*?)\}\}",
            self.template,
        )

        return [variable.strip() for variable in matches]

    def render(
        self,
        **variables,
    ) -> str:

        result = self.template

        for key, value in variables.items():
            result = result.replace(
                "{{" + key + "}}",
                str(value),
            )

        return result

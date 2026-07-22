from bindai_core.model import ModelRequest

class PromptBuilder:
    def build(
        self,
        agent,
        context,
    ) -> ModelRequest: ...

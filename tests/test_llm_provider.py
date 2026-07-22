from bindai import LLMProvider
from bindai import LLMResult


class DummyProvider(LLMProvider):
    def generate(
        self,
        prompt: str,
    ) -> LLMResult:

        return LLMResult(
            success=True,
            value=f"Echo: {prompt}",
        )


def test_provider():

    provider = DummyProvider()

    result = provider.generate("Hello")

    assert result.success

    assert result.value == "Echo: Hello"

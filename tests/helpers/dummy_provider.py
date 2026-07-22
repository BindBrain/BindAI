from bindai_core.model import (
    ModelRequest,
    ModelResponse,
)


class DummyProvider:
    """
    Simple provider used by unit tests.
    """

    def __init__(
        self,
        response: str,
    ):
        self.response = response

    def generate(
        self,
        request: ModelRequest,
    ) -> ModelResponse:

        return ModelResponse(
            content=self.response,
            tool_calls=[],
        )

    def stream(
        self,
        request: ModelRequest,
    ):

        yield type(
            "Chunk",
            (),
            {
                "delta": self.response,
            },
        )()

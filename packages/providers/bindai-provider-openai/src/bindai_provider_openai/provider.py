from openai import OpenAI

from bindai_core.model import (
    ModelProvider,
    ProviderCapabilities,
    ModelRequest,
    ModelResponse,
)

from .mapper import OpenAIMapper
from .settings import OpenAISettings


class OpenAIProvider(ModelProvider):

    def __init__(
        self,
        settings: OpenAISettings,
    ):

        self._settings = settings

        self._client = OpenAI(
            api_key=settings.api_key,
            base_url=settings.base_url,
        )

    @property
    def name(self):

        return "openai"

    @property
    def capabilities(self):

        return ProviderCapabilities(

            chat=True,

            streaming=True,

            embeddings=True,

            tool_calling=True,

            structured_output=True,

        )

    def generate(
        self,
        request: ModelRequest,
    ):

        response = self._client.chat.completions.create(

            model=self._settings.model,

            messages=OpenAIMapper.messages(request),

        )

        return ModelResponse(

            content=response.choices[0].message.content,

            model=response.model,

        )
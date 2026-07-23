from __future__ import annotations

from .application import Application

from dotenv import load_dotenv


class ApplicationBuilder:
    def __init__(self):

        self._application = Application()

    def provider(
        self,
        provider,
    ):

        self._application.add_provider(
            provider,
        )

        return self

    def agent(
        self,
        agent,
    ):

        self._application.add_agent(
            agent,
        )

        return self

    def build(
        self,
    ) -> Application:

        load_dotenv()

        return self._application

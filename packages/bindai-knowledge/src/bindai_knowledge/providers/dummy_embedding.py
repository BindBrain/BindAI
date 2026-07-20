class DummyEmbeddingProvider:
    """
    Simple deterministic embedding provider used only for tests.
    """

    def embed(
        self,
        text: str,
    ) -> list[float]:

        return [
            float(len(text)),
        ]
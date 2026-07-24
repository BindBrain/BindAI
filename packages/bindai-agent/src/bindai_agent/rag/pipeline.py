from __future__ import annotations


class RAGPipeline:

    def __init__(
        self,
        retriever,
        context_builder,
    ):
        self.retriever = retriever
        self.context_builder = context_builder

    def build_prompt(
        self,
        question: str,
    ):

        result = self.retriever.retrieve(question)

        context = self.context_builder.build(
            result.documents or [],
        )

        return f"""
    Context:

    {context}

    Question:

    {question}
    """
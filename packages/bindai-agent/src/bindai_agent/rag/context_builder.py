from __future__ import annotations


class ContextBuilder:

    def build(self, documents):

        return "\n\n".join(
            doc.value
            for doc in documents
        )
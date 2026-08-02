"""
21. Document QA

Question answering over documents
using BindAI knowledge and retrieval.
"""

from bindai import AgentBuilder

documents = [
    {
        "title": "BindAI Overview",
        "content": """
        BindAI is a framework for building
        AI applications with agents,
        workflows, tools, memory,
        and knowledge systems.
        """,
    },
    {
        "title": "BindAI Workflows",
        "content": """
        Workflows allow developers to
        create multi-step AI pipelines
        with conditions, retries,
        parallel execution and tasks.
        
        A workflow coordinates different
        execution steps and allows reliable
        automation of complex AI processes.
        """,
    },
]


def tokenize(text):

    return text.lower().replace("?", "").replace(".", "").replace(",", "").split()


def retrieve_context(
    question: str,
    top_k=2,
):

    question_words = set(tokenize(question))

    scored = []

    for doc in documents:
        words = set(tokenize(doc["content"]))

        score = len(question_words.intersection(words))

        scored.append((score, doc["content"]))

    scored.sort(reverse=True, key=lambda x: x[0])

    return "\n".join(item[1] for item in scored[:top_k] if item[0] > 0)


agent = (
    AgentBuilder()
    .instructions(
        """
        You are a document QA assistant.

        Answer only from the provided context.

        If the answer is missing,
        say that the context does not contain
        the information.
        """
    )
    .build()
)


def ask(question):

    context = retrieve_context(question)

    prompt = f"""
Context:

{context}


Question:

{question}
"""

    result = agent.chat(prompt)

    return result.output


if __name__ == "__main__":
    question = "What are BindAI workflows?"

    answer = ask(question)

    print("=" * 60)
    print("Question:")
    print(question)

    print()

    print("Answer:")

    print(answer)

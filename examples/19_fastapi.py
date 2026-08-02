"""
19. FastAPI Integration

Demonstrates exposing a BindAI agent
through a REST API.
"""

from bindai import AgentBuilder
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="BindAI Assistant API")


agent = (
    AgentBuilder()
    .openai("gpt-4.1-mini")
    .instructions(
        """
        You are a helpful AI assistant.
        Answer clearly and concisely.
        """
    )
    .build()
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def health():
    return {"status": "BindAI API running"}


@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):

    result = agent.chat(request.message)

    return ChatResponse(response=result.output)

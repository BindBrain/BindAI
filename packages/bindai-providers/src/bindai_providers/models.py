from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Tool Calls
# ---------------------------------------------------------


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------
# Messages
# ---------------------------------------------------------


class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]

    content: str | None = None

    name: str | None = None

    tool_calls: list[ToolCall] = Field(default_factory=list)

    tool_call_id: str | None = None


# ---------------------------------------------------------
# Tool Definitions
# ---------------------------------------------------------


class ToolDefinition(BaseModel):
    name: str

    description: str

    parameters: dict[str, Any] = Field(default_factory=dict)


class ToolChoice(BaseModel):
    name: str | None = None

    required: bool = False


# ---------------------------------------------------------
# Usage
# ---------------------------------------------------------


class Usage(BaseModel):
    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0


# ---------------------------------------------------------
# Request
# ---------------------------------------------------------


class ChatCompletionRequest(BaseModel):
    model: str

    messages: list[Message]

    temperature: float = 0.7

    max_tokens: int | None = None

    tools: list[ToolDefinition] = Field(default_factory=list)

    tool_choice: ToolChoice | None = None

    stream: bool = False

    metadata: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------
# Response
# ---------------------------------------------------------


class ChatCompletionResponse(BaseModel):
    message: Message

    usage: Usage = Field(default_factory=Usage)

    finish_reason: str | None = None

    raw: dict[str, Any] | None = None
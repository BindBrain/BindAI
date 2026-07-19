from __future__ import annotations

from typing import TYPE_CHECKING

from bindai_core.context import ExecutionContext
from bindai_core.model import (
	ModelRequest,
	ModelResponse,
)

from .result import AgentResult
from bindai_core.schema import SchemaSerializer

if TYPE_CHECKING:
	from .agent import Agent


class AgentExecutor:
	"""
	Executes an agent by driving the full execution loop.
	"""

	def execute(
		self,
		agent: Agent,
		context: ExecutionContext,
	) -> AgentResult:

		self._initialize(
			agent,
			context,
		)

		while True:

			request = self._build_request(
				agent,
				context,
			)

			response = self._generate(
				agent,
				request,
			)

			if not response.tool_calls:

				return self._finish(
					agent,
					response,
				)

			self._execute_tool_calls(
				agent,
				response,
			)

	def stream(
		self,
		agent: Agent,
		context: ExecutionContext,
	):

		self._initialize(
			agent,
			context,
		)

		request = self._build_request(
			agent,
			context,
		)

		content = ""

		for chunk in agent.provider.stream(
			request,
		):

			content += chunk.delta

			yield chunk

		agent.conversation.add_assistant(
			content,
		)

	def _initialize(
		self,
		agent: Agent,
		context: ExecutionContext,
	) -> None:

		user_input = context.variables.get(
			"input",
			"",
		)

		if len(agent.conversation) == 0:

			agent.conversation.add_system(
				agent.instructions,
			)

		agent.conversation.add_user(
			user_input,
		)

	def _build_request(
		self,
		agent: Agent,
		context: ExecutionContext,
	) -> ModelRequest:

		request = agent.conversation.to_request()

		request.tools = agent.tools.definitions()

		output_type = context.variables.get(
			"output_type",
		)

		if output_type is not None:

			request.response_schema = (
				SchemaSerializer.serialize(
					output_type,
				)
			)

		return request

	def _generate(
		self,
		agent: Agent,
		request: ModelRequest,
	) -> ModelResponse:

		return agent.provider.generate(
			request,
		)

	def _execute_tool_calls(
		self,
		agent: Agent,
		response: ModelResponse,
	) -> None:

		agent.conversation.add_assistant_tool_call(
			response.tool_calls,
		)

		for tool_call in response.tool_calls:

			result = agent.execute_tool(
				tool_call.name,
				**tool_call.arguments,
			)

			agent.conversation.add_tool(
				tool_call_id=tool_call.id,
				content=(
					str(result.output)
					if result.success
					else f"ERROR: {result.error}"
				),
			)

	def _finish(
		self,
		agent: Agent,
		response: ModelResponse,
	) -> AgentResult:

		agent.conversation.add_assistant(
			response.content,
		)

		return AgentResult(
			success=True,
			output=response.content,
		)
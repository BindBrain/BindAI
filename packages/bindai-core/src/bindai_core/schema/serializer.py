from __future__ import annotations

from typing import Any

from .schema import ResponseSchema


class SchemaSerializer:
	"""
	Converts Python models into provider-independent schemas.
	"""

	@staticmethod
	def serialize(
		model: type[Any],
	) -> ResponseSchema:

		#
		# Pydantic v2
		#

		if hasattr(
			model,
			"model_json_schema",
		):

			return ResponseSchema(
				model=model,
				json_schema=model.model_json_schema(),
			)

		raise TypeError(
			f"Unsupported schema type: {model}"
		)
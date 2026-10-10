from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


DiagnosticSeverity = Literal["error", "warning"]


@dataclass(frozen=True, slots=True)
class DefinitionDiagnostic:
    severity: DiagnosticSeverity
    code: str
    message: str
    node_id: str | None = None
    node_type: str | None = None
    suggestion: str | None = None

    @property
    def is_error(self) -> bool:
        return self.severity == "error"

    @property
    def is_warning(self) -> bool:
        return self.severity == "warning"

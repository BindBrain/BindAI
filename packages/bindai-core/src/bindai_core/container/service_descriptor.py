from dataclasses import dataclass
from typing import Any

from .lifetime import ServiceLifetime


@dataclass(slots=True)
class ServiceDescriptor:
    service_type: type
    implementation: Any
    lifetime: ServiceLifetime

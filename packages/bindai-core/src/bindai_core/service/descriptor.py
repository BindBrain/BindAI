from dataclasses import dataclass

from .lifetime import ServiceLifetime


@dataclass(slots=True)
class ServiceDescriptor:

    service_type: type

    implementation: object

    lifetime: ServiceLifetime
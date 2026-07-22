from __future__ import annotations

from .descriptor import ServiceDescriptor
from .lifetime import ServiceLifetime


class ServiceContainer:
    def __init__(self):

        self._services: dict[type, ServiceDescriptor] = {}

    def add_singleton(
        self,
        service_type: type,
        implementation,
    ):

        self._services[service_type] = ServiceDescriptor(
            service_type=service_type,
            implementation=implementation,
            lifetime=ServiceLifetime.SINGLETON,
        )

    def resolve(
        self,
        service_type: type,
    ):

        descriptor = self._services.get(service_type)

        if descriptor is None:
            raise KeyError(service_type)

        return descriptor.implementation

    def contains(
        self,
        service_type: type,
    ):

        return service_type in self._services

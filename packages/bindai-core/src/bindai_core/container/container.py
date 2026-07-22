from __future__ import annotations

from typing import Any

from .lifetime import ServiceLifetime
from .service_descriptor import ServiceDescriptor


class BindContainer:
    """
    Lightweight dependency injection container.

    This is the heart of the BindAI runtime.
    """

    def __init__(self) -> None:
        self._services: dict[type, ServiceDescriptor] = {}

    def register(
        self,
        service_type: type,
        implementation: Any,
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
    ) -> None:
        """
        Register a service.
        """

        self._services[service_type] = ServiceDescriptor(
            service_type=service_type,
            implementation=implementation,
            lifetime=lifetime,
        )

    def resolve(self, service_type: type) -> Any:
        """
        Resolve a registered service.
        """

        descriptor = self._services.get(service_type)

        if descriptor is None:
            raise KeyError(f"Service '{service_type.__name__}' is not registered.")

        return descriptor.implementation

    def is_registered(self, service_type: type) -> bool:
        return service_type in self._services

    def clear(self) -> None:
        self._services.clear()

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import Callable


class ServiceLifetime(
    Enum,
):
    """
    Service lifetime.
    """

    SINGLETON = "singleton"

    TRANSIENT = "transient"


@dataclass(slots=True)
class ServiceDescriptor:

    service_type: type

    implementation: Any

    lifetime: ServiceLifetime


class Container:
    """
    Lightweight dependency injection container.
    """

    def __init__(
        self,
    ):

        self._services: dict[
            type,
            ServiceDescriptor,
        ] = {}

    #
    # Registration
    #

    def register(
        self,
        service_type: type,
        implementation: Any,
        *,
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
    ):

        self._services[
            service_type
        ] = ServiceDescriptor(
            service_type=service_type,
            implementation=implementation,
            lifetime=lifetime,
        )

    def register_singleton(
        self,
        service_type: type,
        instance: Any,
    ):

        self.register(
            service_type,
            instance,
            lifetime=ServiceLifetime.SINGLETON,
        )

    def register_transient(
        self,
        service_type: type,
        factory: Callable[[], Any],
    ):

        self.register(
            service_type,
            factory,
            lifetime=ServiceLifetime.TRANSIENT,
        )

    #
    # Resolution
    #

    def resolve(
        self,
        service_type: type,
    ) -> Any:

        if service_type not in self._services:

            raise KeyError(
                f"Service '{service_type.__name__}' is not registered."
            )

        descriptor = self._services[
            service_type
        ]

        if (
            descriptor.lifetime
            == ServiceLifetime.SINGLETON
        ):

            return descriptor.implementation

        return descriptor.implementation()

    #
    # Helpers
    #

    def contains(
        self,
        service_type: type,
    ) -> bool:

        return (
            service_type
            in self._services
        )

    def clear(
        self,
    ):

        self._services.clear()
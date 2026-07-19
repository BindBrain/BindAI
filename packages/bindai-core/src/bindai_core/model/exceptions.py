from __future__ import annotations


class ModelException(Exception):
    """
    Base model exception.
    """


class ProviderException(ModelException):
    """
    Provider communication failed.
    """


class AuthenticationException(
    ProviderException,
):
    """
    Invalid credentials.
    """


class RateLimitException(
    ProviderException,
):
    """
    Provider rate limit exceeded.
    """


class InvalidRequestException(
    ProviderException,
):
    """
    Invalid request.
    """
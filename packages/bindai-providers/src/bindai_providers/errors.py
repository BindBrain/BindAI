class ProviderError(Exception):
    pass


class AuthenticationError(ProviderError):
    pass


class RateLimitError(ProviderError):
    pass


class InvalidRequestError(ProviderError):
    pass


class ProviderUnavailableError(ProviderError):
    pass


class ConfigurationError(ProviderError):
    pass

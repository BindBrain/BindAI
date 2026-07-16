from bindai_core.provider import ProviderConfiguration

config = ProviderConfiguration(
    api_key="123456",
    endpoint="https://api.bindai.dev",
    model="gpt-5",
)

print(config.api_key)
print(config.endpoint)
print(config.model)
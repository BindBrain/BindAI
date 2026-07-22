import os

from bindai import YamlLoader


loader = YamlLoader()

group = loader.load(
    "examples/marketing.yaml",
)

#
# Temporary provider initialization.
#
# Until we add Application configuration,
# assign the API key after loading.
#

for agent in group.agents:
    if hasattr(agent.provider.configuration, "api_key"):
        agent.provider.configuration.api_key = os.getenv(
            "OPENAI_API_KEY",
        )

result = group.run()

print(result.output)

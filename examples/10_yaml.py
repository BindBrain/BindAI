from bindai_config.yaml_loader import YamlLoader

print("=" * 60)
print("YAML Configuration")
print("=" * 60)
print()

loader = YamlLoader()

group = loader.load(
    "examples/assets/research_group.yaml",
)

result = group.run()

print("Success:")
print(result.success)

print()

print("Output:")
print(result.output)

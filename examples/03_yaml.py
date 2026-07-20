from bindai import YamlLoader


group = (
    YamlLoader()
    .load(
        "examples/marketing.yaml",
    )
)

result = group.run()

print(
    result.output,
)
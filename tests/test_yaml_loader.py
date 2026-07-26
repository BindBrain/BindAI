from bindai import YamlLoader


def test_yaml_loader():

    group = YamlLoader().load(
        "examples/assets/marketing.yaml",
    )

    assert group is not None

    assert len(group.agents) == 2

    assert len(group.tasks) == 2

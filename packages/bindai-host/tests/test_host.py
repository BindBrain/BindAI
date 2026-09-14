from bindai_host import BindHost, BindHostBuilder, HostConfiguration


class FakeProject:
    def __init__(self, name: str):
        self.name = name
        self.run_calls: list[dict[str, str]] = []
        self.stream_calls: list[dict[str, str]] = []

    def run(self, *, application: str, agent: str, message: str):
        self.run_calls.append(
            {
                "application": application,
                "agent": agent,
                "message": message,
            }
        )
        return f"run:{message}"

    def stream(self, *, application: str, agent: str, message: str):
        self.stream_calls.append(
            {
                "application": application,
                "agent": agent,
                "message": message,
            }
        )
        return f"stream:{message}"


def make_host(
    name: str = "BindAI",
    version: str = "1.0.0",
) -> BindHost:
    return BindHost(
        HostConfiguration(
            name=name,
            version=version,
        )
    )


def test_configuration_defaults():
    configuration = HostConfiguration()

    assert configuration.name == "BindAI"
    assert configuration.version == "1.0.0"


def test_host_initializes_with_empty_projects():
    host = make_host(
        name="test-host",
        version="2.0.0",
    )

    assert host.name == "test-host"
    assert host.configuration.version == "2.0.0"
    assert host.projects == {}


def test_add_project_registers_and_returns_host():
    host = make_host()
    project = FakeProject("demo")

    result = host.add_project(project)

    assert result is host
    assert host.project("demo") is project
    assert host.projects == {"demo": project}


def test_add_project_replaces_project_with_same_name():
    host = make_host()
    first = FakeProject("demo")
    second = FakeProject("demo")

    host.add_project(first)
    host.add_project(second)

    assert host.project("demo") is second
    assert len(host.projects) == 1


def test_project_raises_key_error_for_unknown_project():
    host = make_host()

    try:
        host.project("missing")
    except KeyError as error:
        assert error.args == ("missing",)
    else:
        raise AssertionError("Expected KeyError")


def test_run_delegates_to_project():
    host = make_host()
    project = FakeProject("demo")
    host.add_project(project)

    result = host.run(
        project="demo",
        application="assistant-app",
        agent="assistant",
        message="Hello",
    )

    assert result == "run:Hello"
    assert project.run_calls == [
        {
            "application": "assistant-app",
            "agent": "assistant",
            "message": "Hello",
        }
    ]


def test_stream_delegates_to_project():
    host = make_host()
    project = FakeProject("demo")
    host.add_project(project)

    result = host.stream(
        project="demo",
        application="assistant-app",
        agent="assistant",
        message="Hello",
    )

    assert result == "stream:Hello"
    assert project.stream_calls == [
        {
            "application": "assistant-app",
            "agent": "assistant",
            "message": "Hello",
        }
    ]


def test_builder_project_registers_project_and_returns_builder():
    builder = BindHostBuilder()
    project = FakeProject("demo")

    result = builder.project(project)

    assert result is builder
    assert builder.host.project("demo") is project


def test_builder_build_returns_host():
    builder = BindHostBuilder()
    project = FakeProject("demo")

    result = builder.project(project).build()

    assert isinstance(result, BindHost)
    assert result is builder.host
    assert result.name == "BindAI"
    assert result.project("demo") is project
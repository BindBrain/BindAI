from __future__ import annotations

from pathlib import Path

from bindai_api.app import app
from bindai_api.routes.studio import (
    clear_studio_projects,
    configure_studio_project,
    configure_studio_workspace,
)
from fastapi.testclient import TestClient

TEST_API_KEY = "test-api-key"

AUTH_HEADERS = {
    "Authorization": f"Bearer {TEST_API_KEY}",
}


def create_project(root: Path, name: str = "Studio Test") -> Path:
    root.mkdir()

    (root / "bindai.toml").write_text(
        f'name = "{name}"\nworkflows = "workflows"\n',
        encoding="utf-8",
    )

    (root / "workflows").mkdir()

    return root


def create_workflow(root: Path) -> Path:
    workflow = root / "workflows" / "hello.yaml"

    workflow.write_text(
        """version: 1
workflow:
  id: hello
  name: Hello Workflow
  nodes:
    - id: start
      type: start
    - id: end
      type: end
  edges:
    - from: start
      to: end
""",
        encoding="utf-8",
    )

    return workflow


def setup_function() -> None:
    clear_studio_projects()


def teardown_function() -> None:
    clear_studio_projects()


def test_studio_requires_api_key(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.get(
        "/api/v1/studio/projects",
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid or missing API key.",
    }


def test_list_studio_projects(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.get(
        "/api/v1/studio/projects",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Studio Test",
            "path": str(root.resolve()),
            "workflow_count": 0,
            "agent_count": 0,
            "form_count": 0,
        }
    ]


def test_get_studio_project(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.get(
        "/api/v1/studio/projects/test-project",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Studio Test"


def test_studio_project_not_found(
    monkeypatch,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    client = TestClient(app)

    response = client.get(
        "/api/v1/studio/projects/missing",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Studio project 'missing' was not found.",
    }


def test_list_studio_workflows(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")
    create_workflow(root)

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.get(
        "/api/v1/studio/projects/test-project/workflows",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "hello",
            "name": "Hello Workflow",
            "path": str(
                (root / "workflows" / "hello.yaml").resolve()
            ),
        }
    ]


def test_get_studio_workflow(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")
    create_workflow(root)

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.get(
        "/api/v1/studio/projects/test-project/workflows/hello",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["version"] == 1
    assert body["workflow"]["id"] == "hello"
    assert body["workflow"]["name"] == "Hello Workflow"
    assert len(body["workflow"]["nodes"]) == 2
    assert len(body["workflow"]["edges"]) == 1


def test_validate_studio_workflow(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")
    create_workflow(root)

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.post(
        "/api/v1/studio/projects/test-project/workflows/hello/validate",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json() == []
def test_save_studio_workflow(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")
    create_workflow(root)

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.put(
        "/api/v1/studio/projects/test-project/workflows/hello",
        headers=AUTH_HEADERS,
        json={
            "version": 1,
            "workflow": {
                "id": "hello",
                "name": "Updated Workflow",
                "nodes": [
                    {
                        "id": "start",
                        "type": "start",
                    },
                    {
                        "id": "end",
                        "type": "end",
                        "name": "Finished",
                    },
                ],
                "edges": [
                    {
                        "from": "start",
                        "to": "end",
                    },
                ],
            },
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["workflow"]["workflow"]["name"] == "Updated Workflow"
    assert body["diagnostics"] == []

    saved = (root / "workflows" / "hello.yaml").read_text(
        encoding="utf-8",
    )

    assert "Updated Workflow" in saved
    assert "Finished" in saved

def test_create_studio_workflow(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )
    root = create_project(tmp_path / "project")
    configure_studio_project(
        "test-project",
        root,
    )
    client = TestClient(app)

    response = client.put(
        "/api/v1/studio/projects/test-project/workflows/new-workflow",
        headers=AUTH_HEADERS,
        json={
            "version": 1,
            "workflow": {
                "id": "new-workflow",
                "name": "New Workflow",
                "nodes": [
{
    "id": "start",
    "type": "start",
    "position": {
        "x": 147.5,
        "y": 211.25,
    },
},
                    {
                        "id": "end",
                        "type": "end",
                    },
                ],
                "edges": [
                    {
                        "from": "start",
                        "to": "end",
                    },
                ],
            },
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["workflow"]["workflow"]["id"] == "new-workflow"
    assert body["workflow"]["workflow"]["name"] == "New Workflow"
    assert body["diagnostics"] == []

    saved = root / "workflows" / "new-workflow.yaml"
    assert saved.is_file()

    loaded = client.get(
        "/api/v1/studio/projects/test-project/workflows/new-workflow",
        headers=AUTH_HEADERS,
    )

    assert loaded.status_code == 200
    assert loaded.json()["workflow"]["id"] == "new-workflow"

    loaded_workflow = loaded.json()["workflow"]

    assert loaded_workflow["nodes"][0]["position"] == {
        "x": 147.5,
        "y": 211.25,
    }

    assert loaded_workflow["edges"] == [
        {
            "from": "start",
            "to": "end",
        },
    ]

def test_save_allows_invalid_workflow_with_diagnostics(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")
    create_workflow(root)

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.put(
        "/api/v1/studio/projects/test-project/workflows/hello",
        headers=AUTH_HEADERS,
        json={
            "version": 1,
            "workflow": {
                "id": "hello",
                "name": "Incomplete Workflow",
                "nodes": [
                    {
                        "id": "start",
                        "type": "start",
                    },
                    {
                        "id": "end",
                        "type": "end",
                    },
                ],
                "edges": [
                    {
                        "from": "start",
                        "to": "missing-node",
                    },
                ],
            },
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["workflow"]["workflow"]["name"] == "Incomplete Workflow"
    assert any(
        diagnostic["code"] == "workflow.invalid_node_reference"
        for diagnostic in body["diagnostics"]
    )

    loaded = client.get(
        "/api/v1/studio/projects/test-project/workflows/hello",
        headers=AUTH_HEADERS,
    )

    assert loaded.status_code == 200
    assert (
        loaded.json()["workflow"]["name"]
        == "Incomplete Workflow"
    )

def test_save_studio_workflow_preserves_canonical_node_configuration(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")
    create_workflow(root)

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.put(
        "/api/v1/studio/projects/test-project/workflows/hello",
        headers=AUTH_HEADERS,
        json={
            "version": 1,
            "workflow": {
                "id": "hello",
                "name": "Decision Workflow",
                "nodes": [
                    {
                        "id": "start",
                        "type": "start",
                    },
                    {
                        "id": "decision",
                        "type": "decision",
                        "name": "Check score",
                        "expression": "score > 0.8",
                    },
                    {
                        "id": "end",
                        "type": "end",
                    },
                ],
                "edges": [
                    {
                        "from": "start",
                        "to": "decision",
                    },
                    {
                        "from": "decision",
                        "to": "end",
                        "port": "true",
                    },
                ],
            },
        },
    )

    assert response.status_code == 200

    body = response.json()

    decision = next(
        node
        for node in body["workflow"]["workflow"]["nodes"]
        if node["id"] == "decision"
    )

    assert decision["type"] == "decision"
    assert decision["name"] == "Check score"
    assert decision["expression"] == "score > 0.8"

    assert "configuration" not in decision

    loaded = client.get(
        "/api/v1/studio/projects/test-project/workflows/hello",
        headers=AUTH_HEADERS,
    )

    assert loaded.status_code == 200

    loaded_decision = next(
        node
        for node in loaded.json()["workflow"]["nodes"]
        if node["id"] == "decision"
    )

    assert loaded_decision["expression"] == "score > 0.8"

def test_save_reload_execute_agent_condition_workflow(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")

    (root / "agents").mkdir()

    (root / "bindai.toml").write_text(
        'name = "Studio Test"\n'
        'workflows = "workflows"\n'
        'agents = "agents"\n',
        encoding="utf-8",
    )

    (root / "agents" / "classify.yaml").write_text(
        """id: classify
name: Classify
""",
        encoding="utf-8",
    )

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    save = client.put(
        "/api/v1/studio/projects/test-project/workflows/classification",
        headers=AUTH_HEADERS,
        json={
            "version": 1,
            "workflow": {
                "id": "classification",
                "name": "Classification Workflow",
                "nodes": [
                    {"id": "start", "type": "start"},
                    {
                        "id": "agent",
                        "type": "agent",
                        "agent": "classify",
                        "input_variable": "input",
                        "output_variable": "classification",
                    },
                    {
                        "id": "condition",
                        "type": "condition",
                        "expression": 'classification == "true"',
                    },
                    {"id": "true-end", "type": "end"},
                    {"id": "false-end", "type": "end"},
                ],
                "edges": [
                    {"from": "start", "to": "agent"},
                    {"from": "agent", "to": "condition"},
                    {
                        "from": "condition",
                        "to": "true-end",
                        "port": "true",
                    },
                    {
                        "from": "condition",
                        "to": "false-end",
                        "port": "false",
                    },
                ],
            },
        },
    )

    assert save.status_code == 200
    assert save.json()["diagnostics"] == []

    loaded = client.get(
        "/api/v1/studio/projects/test-project/workflows/classification",
        headers=AUTH_HEADERS,
    )

    assert loaded.status_code == 200

    nodes = loaded.json()["workflow"]["nodes"]

    agent = next(node for node in nodes if node["id"] == "agent")
    condition = next(node for node in nodes if node["id"] == "condition")

    assert agent["output_variable"] == "classification"
    assert condition["expression"] == 'classification == "true"'

    class FakeAgent:
        name = "Classify"

        def execute(self, context):
            from bindai_agent import AgentResult

            return AgentResult(
                success=True,
                output="true",
            )

    def fake_build_agent(
        definition,
        *,
        project_root,
        memory=None,
        retriever=None,
        knowledge=None,
    ):
        from bindai_agent import AgentRegistry

        agent = FakeAgent()
        AgentRegistry.register(agent)
        AgentRegistry.register_alias(
            definition.id,
            agent,
        )

        return agent

    monkeypatch.setattr(
        "bindai_project.studio.build_agent",
        fake_build_agent,
    )

    run = client.post(
        "/api/v1/studio/projects/test-project/workflows/classification/run",
        headers=AUTH_HEADERS,
        json={
            "variables": {
                "input": "urgent request",
            },
        },
    )

    assert run.status_code == 200

    body = run.json()

    assert body["workflow"] == "classification"
    assert body["result"]["success"] is True
    assert body["result"]["output"]["classification"] == "true"


def test_workspace_can_open_project_by_directory_name(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "demo")
    configure_studio_workspace(tmp_path)

    client = TestClient(app)

    response = client.get(
        "/api/v1/studio/projects/demo",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Studio Test"
    assert response.json()["path"] == str(root.resolve())


def test_workspace_project_not_found(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    create_project(tmp_path / "demo")
    configure_studio_workspace(tmp_path)

    client = TestClient(app)

    response = client.get(
        "/api/v1/studio/projects/missing",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Studio project 'missing' was not found.",
    }
def test_create_studio_project(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("BINDAI_API_KEY", TEST_API_KEY)
    configure_studio_workspace(tmp_path)

    client = TestClient(app)

    response = client.post(
        "/api/v1/studio/projects",
        headers=AUTH_HEADERS,
        json={"name": "created-project"},
    )

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == "created-project"
    assert body["workflow_count"] == 0

    project_root = Path(body["path"])

    assert project_root == (tmp_path / "created-project").resolve()
    assert project_root.is_dir()
    assert (project_root / "bindai.toml").is_file()
    assert (project_root / ".env").is_file()
    assert (project_root / "workflows").is_dir()

    config_text = (project_root / "bindai.toml").read_text(
        encoding="utf-8"
    )

    assert 'name = "created-project"' in config_text


def test_create_studio_project_conflict(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("BINDAI_API_KEY", TEST_API_KEY)
    configure_studio_workspace(tmp_path)

    client = TestClient(app)

    first = client.post(
        "/api/v1/studio/projects",
        headers=AUTH_HEADERS,
        json={"name": "duplicate-project"},
    )

    assert first.status_code == 201

    second = client.post(
        "/api/v1/studio/projects",
        headers=AUTH_HEADERS,
        json={"name": "duplicate-project"},
    )

    assert second.status_code == 409
    assert "already exists" in second.json()["detail"]

def test_list_studio_capabilities(monkeypatch) -> None:
    monkeypatch.setenv("BINDAI_API_KEY", TEST_API_KEY)
    client = TestClient(app)

    response = client.get(
        "/api/v1/studio/capabilities",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200

    capabilities = response.json()
    assert isinstance(capabilities, list)

    by_type = {item["type"]: item for item in capabilities}

    expected_types = {
        "StartNode",
        "EndNode",
        "AgentNode",
        "ToolNode",
        "ConditionNode",
        "DecisionNode",
        "ParallelNode",
        "JoinNode",
        "LoopNode",
    }

    assert expected_types <= by_type.keys()
    assert by_type["DecisionNode"]["connection_mode"] == "true_false"
    assert by_type["DecisionNode"]["configuration"] == [
        {
            "name": "expression",
            "type": "expression",
            "required": True,
            "default": None,
        }
    ]

def test_studio_shell():
    client = TestClient(app)

    response = client.get("/studio/")

    assert response.status_code == 200
    assert "BindAI Studio" in response.text
    assert '<div id="root"></div>' in response.text
    assert "/assets/" in response.text

def test_list_studio_agents(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")
    (root / "agents").mkdir()

    (root / "bindai.toml").write_text(
        'name = "Studio Test"\n'
        'workflows = "workflows"\n'
        'agents = "agents"\n',
        encoding="utf-8",
    )

    (root / "agents" / "researcher.yaml").write_text(
        """id: researcher
name: Researcher
provider: openai
model: gpt-4.1-mini
instructions: Research the requested topic.
temperature: 0.4
""",
        encoding="utf-8",
    )

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.get(
        "/api/v1/studio/projects/test-project/agents",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "researcher",
            "name": "Researcher",
            "path": str(
                (root / "agents" / "researcher.yaml").resolve()
            ),
        }
    ]


def test_get_studio_agent(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")
    (root / "agents").mkdir()

    (root / "bindai.toml").write_text(
        'name = "Studio Test"\n'
        'workflows = "workflows"\n'
        'agents = "agents"\n',
        encoding="utf-8",
    )

    (root / "agents" / "researcher.yaml").write_text(
        """id: researcher
name: Researcher
provider: openai
model: gpt-4.1-mini
connection: default
instructions: Research the requested topic.
temperature: 0.4
max_tokens: 1000
max_tool_iterations: 5
stream: true
verbose: false
tools:
  - web_search
memory: project_memory
retriever: project_retriever
knowledge: project_knowledge
middleware:
  - logging
hooks:
  - audit
""",
        encoding="utf-8",
    )

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.get(
        "/api/v1/studio/projects/test-project/agents/researcher",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["agent"] == {
        "id": "researcher",
        "name": "Researcher",
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "connection": "default",
        "instructions": "Research the requested topic.",
        "temperature": 0.4,
        "max_tokens": 1000,
        "max_tool_iterations": 5,
        "stream": True,
        "verbose": False,
        "tools": ["web_search"],
        "memory": "project_memory",
        "retriever": "project_retriever",
        "knowledge": "project_knowledge",
        "middleware": ["logging"],
        "hooks": ["audit"],
    }


def test_save_studio_agent(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")
    (root / "agents").mkdir()

    (root / "bindai.toml").write_text(
        'name = "Studio Test"\n'
        'workflows = "workflows"\n'
        'agents = "agents"\n',
        encoding="utf-8",
    )

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.put(
        "/api/v1/studio/projects/test-project/agents/researcher",
        headers=AUTH_HEADERS,
        json={
            "agent": {
                "id": "researcher",
                "name": "Researcher",
                "provider": "openai",
                "model": "gpt-4.1-mini",
                "connection": "default",
                "instructions": "Research the requested topic.",
                "temperature": 0.4,
                "max_tokens": 1200,
                "max_tool_iterations": 8,
                "stream": True,
                "verbose": True,
                "tools": ["web_search"],
                "memory": "project_memory",
                "retriever": "project_retriever",
                "knowledge": "project_knowledge",
                "middleware": ["logging"],
                "hooks": ["audit"],
            }
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["agent"]["id"] == "researcher"
    assert body["agent"]["name"] == "Researcher"
    assert body["agent"]["max_tokens"] == 1200
    assert body["agent"]["max_tool_iterations"] == 8
    assert body["agent"]["stream"] is True
    assert body["agent"]["verbose"] is True

    saved = root / "agents" / "researcher.yaml"

    assert saved.is_file()

    loaded = client.get(
        "/api/v1/studio/projects/test-project/agents/researcher",
        headers=AUTH_HEADERS,
    )

    assert loaded.status_code == 200
    assert loaded.json()["agent"]["max_tokens"] == 1200
    assert loaded.json()["agent"]["tools"] == ["web_search"]


def test_save_studio_agent_rejects_id_mismatch(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")
    (root / "agents").mkdir()

    (root / "bindai.toml").write_text(
        'name = "Studio Test"\n'
        'workflows = "workflows"\n'
        'agents = "agents"\n',
        encoding="utf-8",
    )

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.put(
        "/api/v1/studio/projects/test-project/agents/researcher",
        headers=AUTH_HEADERS,
        json={
            "agent": {
                "id": "different-agent",
                "name": "Researcher",
            }
        },
    )

    assert response.status_code == 400
    assert "does not match URL agent id" in response.json()["detail"]

def test_create_studio_workflow_endpoint(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.post(
        "/api/v1/studio/projects/test-project/workflows",
        headers=AUTH_HEADERS,
        json={
            "name": "Customer Intake",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["workflow"]["workflow"]["name"] == "Customer Intake"
    assert body["workflow"]["workflow"]["id"] == "customer-intake"
    assert body["workflow"]["workflow"]["nodes"] == []
    assert body["workflow"]["workflow"]["edges"] == []
    assert body["diagnostics"] == []

    saved = root / "workflows" / "customer-intake.yaml"

    assert saved.is_file()

    loaded = client.get(
        "/api/v1/studio/projects/test-project/workflows/customer-intake",
        headers=AUTH_HEADERS,
    )

    assert loaded.status_code == 200
    assert loaded.json()["workflow"]["id"] == "customer-intake"
    assert loaded.json()["workflow"]["name"] == "Customer Intake"

    invalid = client.post(
        "/api/v1/studio/projects/test-project/workflows",
        headers=AUTH_HEADERS,
        json={
            "name": "!!!",
        },
    )

    assert invalid.status_code == 400
    assert invalid.json()["detail"] == (
        "Workflow name must contain at least one letter or number."
    )

def test_run_studio_workflow_uses_existing_runtime(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    root = create_project(tmp_path / "project")

    (root / "agents").mkdir()

    (root / "bindai.toml").write_text(
        'name = "Studio Test"\n'
        'workflows = "workflows"\n'
        'agents = "agents"\n',
        encoding="utf-8",
    )

    (root / "agents" / "support.yaml").write_text(
        """id: support-agent
name: Support Agent
""",
        encoding="utf-8",
    )

    (root / "workflows" / "support.yaml").write_text(
        """version: 1
workflow:
  id: support
  name: Support Workflow
  nodes:
    - id: start
      type: start
    - id: agent
      type: agent
      agent: support-agent
      input_variable: input
      output_variable: output
    - id: end
      type: end
  edges:
    - from: start
      to: agent
    - from: agent
      to: end
""",
        encoding="utf-8",
    )

    class FakeAgent:
        name = "Support Agent"

    def fake_build_agent(
        definition,
        *,
        project_root,
        memory=None,
        retriever=None,
        knowledge=None,
    ):
        assert definition.id == "support-agent"
        assert definition.name == "Support Agent"
        assert project_root == root.resolve()

        from bindai_agent import AgentRegistry

        agent = FakeAgent()
        AgentRegistry.register(agent)
        AgentRegistry.register_alias(
            definition.id,
            agent,
        )

        return agent

    monkeypatch.setattr(
        "bindai_project.studio.build_agent",
        fake_build_agent,
    )

    configure_studio_project(
        "test-project",
        root,
    )

    client = TestClient(app)

    response = client.post(
        "/api/v1/studio/projects/test-project/workflows/support/run",
        headers=AUTH_HEADERS,
        json={
            "variables": {
                "input": "Hello",
            },
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["workflow"] == "support"
    assert body["result"] is not None

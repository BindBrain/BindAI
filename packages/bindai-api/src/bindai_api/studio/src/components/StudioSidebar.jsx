import { useEffect, useState } from "react";

import NodeIcon from "./NodeIcon";

import {
  getNodeDescription,
} from "./BindAINode";

export default function StudioSidebar({
  apiKey,
  setApiKeyValue,
  handleApiKeySave,
  apiError,
  setApiError,
  isConnected,
  projects,
  selectedProject,
  handleProjectSelect,
  setShowProjectDialog,
  workflows,
  selectedWorkflow,
  handleWorkflowSelect,
  setShowWorkflowDialog,
  setDeleteWorkflowTarget,
  forms,
  selectedForm,
  handleFormSelect,
  setDeleteFormTarget,
  setNewFormName,
  setNewFormId,
  setShowFormDialog,
  agents,
  handleAgentSelect,
  setDeleteAgentTarget,
  knowledge,
  connections = [],
  connectionProviders = [],
  onCreateConnection,
  onSetConnectionCredential,
  onDeleteConnection,
  setNewAgentName,
  setNewAgentId,
  setShowAgentDialog,
  capabilities,
  handleAddNode,
}) {
  return (
    <aside className="sidebar">
      <div className="api-key-section">
        <label>API Key</label>

        <input
          type="password"
          value={apiKey}
          onChange={(event) =>
            setApiKeyValue(event.target.value)
          }
          placeholder="BINDAI_API_KEY"
        />

        <button
          type="button"
          onClick={handleApiKeySave}
        >
          Connect
        </button>
      </div>

      {apiError && (
        <div className="api-error">
          {apiError}
        </div>
      )}

      {!isConnected && (
        <div className="api-error">
          Studio is locked. Enter a valid API key to
          continue.
        </div>
      )}

      <div className="panel-heading sidebar-section-title">
        Projects
      </div>

      <button
        className="sidebar-create-button"
        type="button"
        onClick={() =>
          setShowProjectDialog(true)
        }
        disabled={!isConnected}
      >
        + New Project
      </button>

      {projects.length > 0 && (
        <div className="sidebar-table">
          <div className="sidebar-table-header project-table-header">
            <span>Project</span>
            <span>Workflows</span>
          </div>

          {projects.map((project) => {
            const isSelected =
              selectedProject?.path ===
              project.path;

            return (
              <button
                className={`sidebar-table-row project-table-row ${
                  isSelected ? "active" : ""
                }`}
                key={project.path}
                type="button"
                disabled={!isConnected}
                onClick={() =>
                  handleProjectSelect(project)
                }
              >
                <span
                  className="sidebar-table-primary"
                  title={project.name}
                >
                  {project.name}
                </span>

                <span className="sidebar-table-count">
                  {project.workflow_count}
                </span>
              </button>
            );
          })}
        </div>
      )}

      {projects.length === 0 && !apiError && (
        <div className="empty-inspector">
          Connect to the BindAI API to load projects.
        </div>
      )}

      <div className="panel-heading workflow-heading sidebar-section-title">
        Workflows
      </div>

      {selectedProject && (
        <button
          className="sidebar-create-button"
          type="button"
          onClick={() =>
            setShowWorkflowDialog(true)
          }
          disabled={!isConnected}
        >
          + New Workflow
        </button>
      )}

      {selectedProject &&
        workflows.length > 0 && (
          <div className="sidebar-table workflow-table">
            <div className="sidebar-table-header workflow-table-header">
              <span>Workflow</span>
            </div>

            {workflows.map((workflow) => {
              const isSelected =
                selectedWorkflow?.id ===
                workflow.id;

              return (
                <div
                  className={`sidebar-table-row workflow-table-row ${
                    isSelected ? "active" : ""
                  }`}
                  key={workflow.id}
                >
                  <button
                    className="sidebar-table-primary"
                    type="button"
                    disabled={!isConnected}
                    onClick={() =>
                      handleWorkflowSelect(
                        workflow,
                      )
                    }
                    title={workflow.name}
                  >
                    {workflow.name}
                  </button>

                  <div className="sidebar-row-menu">
                    <button
                      className="sidebar-row-menu-button sidebar-row-delete-button"
                      type="button"
                      disabled={!isConnected}
                      aria-label={`Delete ${workflow.name}`}
                      title="Delete workflow"
                      onClick={(event) => {
                        event.stopPropagation();
                        setDeleteWorkflowTarget(
                          workflow,
                        );
                      }}
                    >
                      <svg
                        viewBox="0 0 24 24"
                        width="15"
                        height="15"
                        aria-hidden="true"
                      >
                        <path
                          d="M9 3h6l1 2h4v2H4V5h4l1-2Zm-3 6h12l-1 12H7L6 9Zm3 2v8h2v-8H9Zm4 0v8h2v-8h-2Z"
                          fill="currentColor"
                        />
                      </svg>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}

      {selectedProject &&
        workflows.length === 0 && (
          <div className="empty-inspector">
            No workflows found.
          </div>
        )}

      {!selectedProject && (
        <div className="empty-inspector">
          Select a project to view workflows.
        </div>
      )}

      <div className="panel-heading sidebar-section-title">
        Forms
      </div>

      {selectedProject && (
        <button
          className="sidebar-create-button"
          type="button"
          disabled={!isConnected}
          onClick={() => {
            setNewFormName("");
            setNewFormId("");
            setApiError("");
            setShowFormDialog(true);
          }}
        >
          + New Form
        </button>
      )}

      {selectedProject &&
        forms.length > 0 && (
          <div className="sidebar-table workflow-table">
            <div className="sidebar-table-header workflow-table-header">
              <span>Form</span>
            </div>

            {forms.map((form) => {
              const isSelected =
                selectedForm === form.id;

              return (
                <div
                  className={`sidebar-table-row workflow-table-row ${
                    isSelected ? "active" : ""
                  }`}
                  key={form.id}
                >
                  <button
                    className="sidebar-table-primary"
                    type="button"
                    disabled={!isConnected}
                    onClick={() =>
                      handleFormSelect(form)
                    }
                    title={form.name}
                  >
                    {form.name}
                  </button>
                </div>
              );
            })}
          </div>
        )}

      {selectedProject &&
        forms.length === 0 && (
          <div className="empty-inspector">
            No forms found.
          </div>
        )}

        <div className="panel-heading sidebar-section-title">
        Knowledge
        </div>

        {selectedProject && (
        <div className="knowledge-upload">
            <label className="knowledge-upload-button">
            <span>Upload Knowledge</span>
            <input
                type="file"
                accept=".txt,.md,.pdf,.html,.htm"
                onChange={(event) => {
                const file = event.target.files?.[0];

                if (!file) {
                    return;
                }

                if (!selectedProject) {
                    return;
                }

                if (typeof window !== "undefined") {
                    window.dispatchEvent(
                    new CustomEvent(
                        "bindai-studio-upload-knowledge",
                        {
                        detail: {
                            file,
                        },
                        },
                    ),
                    );
                }

                event.target.value = "";
                }}
            />
            </label>

            <div className="field-hint">
            Supported: TXT, MD, PDF, HTML
            </div>
        </div>
        )}

        {selectedProject && knowledge.length > 0 && (
        <div className="sidebar-table workflow-table">
            <div className="sidebar-table-header workflow-table-header">
            <span>Knowledge File</span>
            </div>

            {knowledge.map((item) => (
            <div
                className="sidebar-table-row workflow-table-row"
                key={item.id}
                title={item.path}
            >
                <span className="sidebar-table-primary">
                {item.name}
                </span>
            </div>
            ))}
        </div>
        )}

        {selectedProject && knowledge.length === 0 && (
        <div className="empty-inspector">
            No knowledge files found.
        </div>
        )}

      <div className="node-palette">
        <div className="panel-heading sidebar-section-title">
          Connections
        </div>

        {selectedProject && (
          <ConnectionCreateForm
            connectionProviders={connectionProviders}
            onCreateConnection={onCreateConnection}
          />
        )}

        {selectedProject && (
          <>
            <div className="sidebar-table workflow-table">
              <div className="sidebar-table-header workflow-table-header">
                <span>Connection</span>
                <span>Provider</span>
              </div>
              {connections.map((connection) => (
                <ConnectionRow
                  key={connection.name}
                  connection={connection}
                  onSetConnectionCredential={onSetConnectionCredential}
                  onDeleteConnection={onDeleteConnection}
                />
              ))}
</div>

            {connections.length === 0 && (
              <div className="empty-inspector">
                No connections configured.
              </div>
            )}
          </>
        )}
      </div>
      <div className="node-palette">
        <div className="panel-heading sidebar-section-title">
          Agents
        </div>

        {selectedProject && (
          <button
            className="sidebar-create-button"
            type="button"
            disabled={!isConnected}
            onClick={() => {
              setNewAgentName("");
              setNewAgentId("");
              setApiError("");
              setShowAgentDialog(true);
            }}
          >
            + New Agent
          </button>
        )}

        {selectedProject &&
          agents.length > 0 && (
            <div className="sidebar-table workflow-table">
              <div className="sidebar-table-header workflow-table-header">
                <span>Agent</span>
              </div>

              {agents.map((agent) => (
                <div
                  className={`sidebar-table-row workflow-table-row ${
                    !isConnected ? "disabled" : ""
                  }`}
                  key={agent.id}
                >
                  <button
                    className="sidebar-table-primary"
                    type="button"
                    disabled={!isConnected}
                    onClick={() =>
                      handleAgentSelect(agent)
                    }
                    title={agent.name}
                  >
                    {agent.name}
                  </button>

                  <div className="sidebar-row-menu">
                    <button
                      className="sidebar-row-menu-button sidebar-row-delete-button"
                      type="button"
                      disabled={!isConnected}
                      aria-label={`Delete ${agent.name}`}
                      title="Delete agent"
                      onClick={(event) => {
                        event.stopPropagation();
                        setDeleteAgentTarget(
                          agent,
                        );
                      }}
                    >
                      <svg
                        viewBox="0 0 24 24"
                        width="15"
                        height="15"
                        aria-hidden="true"
                      >
                        <path
                          d="M9 3h6l1 2h4v2H4V5h4l1-2Zm-3 6h12l-1 12H7L6 9Zm3 2v8h2v-8H9Zm4 0v8h2v-8h-2Z"
                          fill="currentColor"
                        />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

        {capabilities.length > 0 ? (
          capabilities.map((capability) => {
            const nodeType =
              capability.type
                .replace(/Node$/, "")
                .toLowerCase();

            const description =
              getNodeDescription(
                nodeType,
                capability.label,
              );

            return (
              <button
                className="node-palette-item"
                key={capability.type}
                type="button"
                onClick={() =>
                  handleAddNode(capability)
                }
                disabled={
                  !isConnected ||
                  !selectedWorkflow
                }
              >
                <span className="node-palette-icon">
                  <NodeIcon
                    type={nodeType}
                    size={13}
                  />
                </span>

                <span className="node-palette-label">
                  {capability.label}
                </span>
              </button>
            );
          })
        ) : (
          <div className="empty-inspector">
            Connect to the BindAI API to load node
            types.
          </div>
        )}
      </div>
    </aside>
  );
}


function ConnectionRow({
  connection,
  onSetConnectionCredential,
  onDeleteConnection,
}) {
  const [credential, setCredential] = useState("");
  const [saving, setSaving] = useState(false);

  async function handleSave(event) {
    event.preventDefault();

    if (!credential.trim()) {
      return;
    }

    setSaving(true);

    try {
      await onSetConnectionCredential(
        connection.name,
        credential.trim(),
      );
      setCredential("");
    } catch (error) {
      alert(
        "Connection error: " +
          (error?.message || String(error)),
      );
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="sidebar-table-row workflow-table-row">
      <div style={{ minWidth: 0 }}>
        <div className="sidebar-table-primary">
          {connection.name}
        </div>

        <div className="sidebar-table-secondary">
          {connection.provider}
          {connection.configured ? " · Configured" : " · Not configured"}
        </div>

        {!connection.configured && connection.provider === "webhook" && (
          <form
            onSubmit={handleSave}
            style={{
              display: "flex",
              gap: "6px",
              marginTop: "6px",
            }}
          >
            <input
              type="url"
              value={credential}
              onChange={(event) =>
                setCredential(event.target.value)
              }
              placeholder="Webhook URL"
              aria-label={`Webhook URL for ${connection.name}`}
              disabled={saving}
              style={{
                minWidth: 0,
                flex: 1,
              }}
            />

            <button
              type="submit"
              disabled={saving || !credential.trim()}
            >
              {saving ? "Saving..." : "Configure"}
            </button>
          </form>
        )}
      </div>

      <button
        type="button"
        onClick={() =>
          onDeleteConnection(connection.name)
        }
        title="Delete connection"
        aria-label={`Delete ${connection.name}`}
        style={{
          border: "none",
          background: "transparent",
          padding: "4px",
          marginLeft: "auto",
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          opacity: 0.65,
        }}
      >
        <svg
          width="13"
          height="13"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <path d="M3 6h18" />
          <path d="M8 6V4h8v2" />
          <path d="M19 6l-1 14H6L5 6" />
          <path d="M10 11v5" />
          <path d="M14 11v5" />
        </svg>
      </button>
    </div>
  );
}
function ConnectionCreateForm({
  connectionProviders = [],
  onCreateConnection,
}) {

  const [name, setName] = useState("");
  const [provider, setProvider] = useState(
    connectionProviders[0],
  );

  async function handleSubmit(event) {
    event.preventDefault();


    const trimmedName = name.trim();

    if (!trimmedName || !provider) {
      return;
    }

    try {

      const result = await onCreateConnection({
        name: trimmedName,
        provider,
      });


      setName("");
    } catch (error) {
      alert(
        "Connection error: " +
        (error?.message || String(error))
      );
    }
  }
  return (
    <form
      className="connection-create-form"
      onSubmit={handleSubmit}
    >
      <input
        type="text"
        value={name}
        placeholder="Connection name"
        onChange={(event) => setName(event.target.value)}
      />

      <select
        value={provider}
        onChange={(event) => setProvider(event.target.value)}
      >
        {connectionProviders.map((item) => (
          <option key={item} value={item}>
            {item}
          </option>
        ))}
      </select>

      <button
        type="submit"
        disabled={!name.trim()}
      >
        Add
      </button>
    </form>
  );
}

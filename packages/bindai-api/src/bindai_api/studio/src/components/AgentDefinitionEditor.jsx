export default function AgentDefinitionEditor({
    agentDefinition,
    setAgentDefinition,
    isConnected,
    handleAgentSave,
    knowledge,
    providers,
  }) {
    if (!agentDefinition) {
      return (
        <div className="empty-inspector">
          Loading agent definition...
        </div>
      );
    }

    return (
      <>
        <div className="inspector-section-title">
          Agent Definition
        </div>

        <div className="inspector-field">
          <label>Agent ID</label>

          <input
            value={agentDefinition.id || ""}
            readOnly
          />
        </div>

        <div className="inspector-field">
          <label>Name</label>

          <input
            value={agentDefinition.name || ""}
            disabled={!isConnected}
            onChange={(event) =>
              setAgentDefinition((current) => ({
                ...current,
                name: event.target.value,
              }))
            }
          />
        </div>

        <div className="inspector-section-title">
          Model
        </div>

        <div className="inspector-field">
        <label>Provider</label>

        <select
            value={agentDefinition.provider || ""}
            disabled={!isConnected}
            onChange={(event) =>
            setAgentDefinition((current) => ({
                ...current,
                provider:
                event.target.value || null,
            }))
            }
        >
            <option value="">
            Select a provider
            </option>
            {(providers || []).map((provider) => (
              <option key={provider} value={provider}>
                {provider.charAt(0).toUpperCase() + provider.slice(1)}
              </option>
            ))}
        </select>
        </div>

        <div className="inspector-field">
          <label>Model</label>

          <input
            value={agentDefinition.model || ""}
            disabled={!isConnected}
            placeholder="gpt-4.1-mini"
            onChange={(event) =>
              setAgentDefinition((current) => ({
                ...current,
                model:
                  event.target.value || null,
              }))
            }
          />
        </div>

        <div className="inspector-field">
          <label>Connection</label>

          <input
            value={agentDefinition.connection || ""}
            disabled={!isConnected}
            placeholder="Optional connection ID"
            onChange={(event) =>
              setAgentDefinition((current) => ({
                ...current,
                connection:
                  event.target.value || null,
              }))
            }
          />
        </div>

        <div className="inspector-section-title">
          Instructions
        </div>

        <div className="inspector-field">
          <label>System Instructions</label>

          <textarea
            value={agentDefinition.instructions || ""}
            rows={7}
            disabled={!isConnected}
            placeholder="Describe how this agent should behave."
            onChange={(event) =>
              setAgentDefinition((current) => ({
                ...current,
                instructions: event.target.value,
              }))
            }
          />
        </div>

        <div className="inspector-section-title">
          Execution
        </div>

        <div className="inspector-field">
          <label>Temperature</label>

          <input
            type="number"
            min="0"
            max="2"
            step="0.1"
            disabled={!isConnected}
            value={agentDefinition.temperature ?? ""}
            placeholder="Provider default"
            onChange={(event) => {
              const raw = event.target.value;

              setAgentDefinition((current) => ({
                ...current,
                temperature:
                  raw === ""
                    ? null
                    : Number.parseFloat(raw),
              }));
            }}
          />
        </div>

        <div className="inspector-field">
          <label>Max Tokens</label>

          <input
            type="number"
            min="1"
            step="1"
            disabled={!isConnected}
            value={agentDefinition.max_tokens ?? ""}
            placeholder="Provider default"
            onChange={(event) => {
              const raw = event.target.value;

              setAgentDefinition((current) => ({
                ...current,
                max_tokens:
                  raw === ""
                    ? null
                    : Number.parseInt(raw, 10),
              }));
            }}
          />
        </div>

        <div className="inspector-field">
          <label>Max Tool Iterations</label>

          <input
            type="number"
            min="0"
            step="1"
            disabled={!isConnected}
            value={
              agentDefinition.max_tool_iterations ?? 10
            }
            onChange={(event) =>
              setAgentDefinition((current) => ({
                ...current,
                max_tool_iterations:
                  Number.parseInt(
                    event.target.value || "0",
                    10,
                  ),
              }))
            }
          />
        </div>

        <div className="inspector-section-title">
          Resources
        </div>

        <div className="inspector-field">
          <label>Memory</label>

          <input
            value={agentDefinition.memory || ""}
            disabled={!isConnected}
            placeholder="Memory resource ID"
            onChange={(event) =>
              setAgentDefinition((current) => ({
                ...current,
                memory:
                  event.target.value || null,
              }))
            }
          />
        </div>

        <div className="inspector-field">
        <label>Knowledge</label>

        <select
            value={agentDefinition.knowledge || ""}
            disabled={!isConnected}
            onChange={(event) =>
            setAgentDefinition((current) => ({
                ...current,
                knowledge:
                event.target.value || null,
            }))
            }
        >
            <option value="">
            No knowledge
            </option>

            {(knowledge || []).map((item) => (
            <option
                key={item.id}
                value={item.id}
            >
                {item.name}
            </option>
            ))}
        </select>

        {(knowledge || []).length === 0 && (
            <div className="field-hint">
            Upload a knowledge file in the Knowledge section first.
            </div>
        )}
        </div>

        <div className="inspector-field">
          <label>Retriever</label>

          <input
            value={agentDefinition.retriever || ""}
            disabled={!isConnected}
            placeholder="Retriever resource ID"
            onChange={(event) =>
              setAgentDefinition((current) => ({
                ...current,
                retriever:
                  event.target.value || null,
              }))
            }
          />
        </div>

        <div className="inspector-field">
          <label>Tools</label>

          <textarea
            value={(agentDefinition.tools || []).join("\n")}
            rows={4}
            disabled={!isConnected}
            placeholder="One tool ID per line"
            onChange={(event) =>
              setAgentDefinition((current) => ({
                ...current,
                tools: event.target.value
                  .split("\n")
                  .map((value) => value.trim())
                  .filter(Boolean),
              }))
            }
          />
        </div>

        <div className="inspector-field">
          <label>Middleware</label>

          <textarea
            value={(
              agentDefinition.middleware || []
            ).join("\n")}
            rows={3}
            disabled={!isConnected}
            placeholder="One middleware ID per line"
            onChange={(event) =>
              setAgentDefinition((current) => ({
                ...current,
                middleware: event.target.value
                  .split("\n")
                  .map((value) => value.trim())
                  .filter(Boolean),
              }))
            }
          />
        </div>

        <div className="inspector-field">
          <label>Hooks</label>

          <textarea
            value={(agentDefinition.hooks || []).join("\n")}
            rows={3}
            disabled={!isConnected}
            placeholder="One hook ID per line"
            onChange={(event) =>
              setAgentDefinition((current) => ({
                ...current,
                hooks: event.target.value
                  .split("\n")
                  .map((value) => value.trim())
                  .filter(Boolean),
              }))
            }
          />
        </div>

        <button
          type="button"
          className="inspector-save-button"
          onClick={handleAgentSave}
          disabled={!isConnected}
        >
          Save Agent
        </button>
      </>
    );
  }

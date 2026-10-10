export default function CreateAgentDialog({
  Modal,
  showAgentDialog,
  selectedProject,
  isConnected,
  creatingAgent,
  newAgentName,
  newAgentId,
  setShowAgentDialog,
  setNewAgentName,
  setNewAgentId,
  handleCreateAgent,
}) {
  if (
    !showAgentDialog ||
    !selectedProject ||
    !isConnected
  ) {
    return null;
  }

  return (
    <Modal
      title="Create Agent"
      onClose={() => {
        if (!creatingAgent) {
          setShowAgentDialog(false);
        }
      }}
    >
      <form
        className="studio-modal-form"
        onSubmit={handleCreateAgent}
      >
        <label>Agent name</label>

        <input
          autoFocus
          value={newAgentName}
          onChange={(event) =>
            setNewAgentName(event.target.value)
          }
          placeholder="Customer Support Agent"
          disabled={creatingAgent}
        />

        <label>
          Agent ID
          <span className="field-hint">
            Optional
          </span>
        </label>

        <input
          value={newAgentId}
          onChange={(event) =>
            setNewAgentId(event.target.value)
          }
          placeholder="customer-support"
          disabled={creatingAgent}
        />

        <p>
          Leave the ID empty to let BindAI generate one
          from the agent name.
        </p>

        <div className="studio-modal-actions">
          <button
            type="button"
            onClick={() =>
              setShowAgentDialog(false)
            }
            disabled={creatingAgent}
          >
            Cancel
          </button>

          <button
            type="submit"
            className="run-button"
            disabled={creatingAgent}
          >
            {creatingAgent
              ? "Creating..."
              : "Create Agent"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

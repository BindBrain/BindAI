export default function CreateWorkflowDialog({
  Modal,
  showWorkflowDialog,
  selectedProject,
  isConnected,
  creatingWorkflow,
  newWorkflowName,
  newWorkflowId,
  setShowWorkflowDialog,
  setNewWorkflowName,
  setNewWorkflowId,
  handleCreateWorkflow,
}) {
  if (
    !showWorkflowDialog ||
    !selectedProject ||
    !isConnected
  ) {
    return null;
  }

  return (
    <Modal
      title="Create Workflow"
      onClose={() => {
        if (!creatingWorkflow) {
          setShowWorkflowDialog(false);
        }
      }}
    >
      <form
        className="studio-modal-form"
        onSubmit={handleCreateWorkflow}
      >
        <label>Workflow name</label>

        <input
          autoFocus
          value={newWorkflowName}
          onChange={(event) =>
            setNewWorkflowName(event.target.value)
          }
          placeholder="customer-support"
          disabled={creatingWorkflow}
        />

        <label>
          Workflow ID
          <span className="field-hint">
            Optional
          </span>
        </label>

        <input
          value={newWorkflowId}
          onChange={(event) =>
            setNewWorkflowId(event.target.value)
          }
          placeholder="customer-support"
          disabled={creatingWorkflow}
        />

        <p>
          Leave the ID empty to let BindAI generate one
          from the workflow name.
        </p>

        <div className="studio-modal-actions">
          <button
            type="button"
            onClick={() =>
              setShowWorkflowDialog(false)
            }
            disabled={creatingWorkflow}
          >
            Cancel
          </button>

          <button
            type="submit"
            className="run-button"
            disabled={creatingWorkflow}
          >
            {creatingWorkflow
              ? "Creating..."
              : "Create Workflow"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

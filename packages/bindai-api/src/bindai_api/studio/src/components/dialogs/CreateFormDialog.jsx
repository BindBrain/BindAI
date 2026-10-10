export default function CreateFormDialog({
  Modal,
  showFormDialog,
  selectedProject,
  isConnected,
  creatingForm,
  newFormName,
  newFormId,
  setShowFormDialog,
  setNewFormName,
  setNewFormId,
  handleCreateForm,
}) {
  if (
    !showFormDialog ||
    !selectedProject ||
    !isConnected
  ) {
    return null;
  }

  return (
    <Modal
      title="Create Form"
      onClose={() => {
        if (!creatingForm) {
          setShowFormDialog(false);
        }
      }}
    >
      <form
        className="studio-modal-form"
        onSubmit={handleCreateForm}
      >
        <label>Form name</label>

        <input
          autoFocus
          value={newFormName}
          onChange={(event) =>
            setNewFormName(event.target.value)
          }
          placeholder="Approval Form"
          disabled={creatingForm}
        />

        <label>
          Form ID
          <span className="field-hint">
            Optional
          </span>
        </label>

        <input
          value={newFormId}
          onChange={(event) =>
            setNewFormId(event.target.value)
          }
          placeholder="approval"
          disabled={creatingForm}
        />

        <p>
          Leave the ID empty to generate one from
          the form name.
        </p>

        <div className="studio-modal-actions">
          <button
            type="button"
            onClick={() =>
              setShowFormDialog(false)
            }
            disabled={creatingForm}
          >
            Cancel
          </button>

          <button
            type="submit"
            className="run-button"
            disabled={creatingForm}
          >
            {creatingForm
              ? "Creating..."
              : "Create Form"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

export default function CreateProjectDialog({
  Modal,
  showProjectDialog,
  isConnected,
  creatingProject,
  newProjectName,
  setShowProjectDialog,
  setNewProjectName,
  handleCreateProject,
}) {
  if (!showProjectDialog || !isConnected) {
    return null;
  }

  return (
    <Modal
      title="Create BindAI Project"
      onClose={() => {
        if (!creatingProject) {
          setShowProjectDialog(false);
        }
      }}
    >
      <form
        className="studio-modal-form"
        onSubmit={handleCreateProject}
      >
        <label>Project name</label>

        <input
          autoFocus
          value={newProjectName}
          onChange={(event) =>
            setNewProjectName(event.target.value)
          }
          placeholder="my-assistant"
          disabled={creatingProject}
        />

        <p>
          The project will be created as a portable
          BindAI project in the configured Studio
          workspace.
        </p>

        <div className="studio-modal-actions">
          <button
            type="button"
            onClick={() =>
              setShowProjectDialog(false)
            }
            disabled={creatingProject}
          >
            Cancel
          </button>

          <button
            type="submit"
            className="run-button"
            disabled={creatingProject}
          >
            {creatingProject
              ? "Creating..."
              : "Create Project"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

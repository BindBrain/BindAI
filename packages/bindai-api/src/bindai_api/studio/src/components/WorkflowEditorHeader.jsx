import { saveWorkflow } from "../api";

export default function WorkflowEditorHeader({
  selectedWorkflow,
  editingWorkflowTitle,
  setEditingWorkflowTitle,
  workflowTitleDraft,
  setWorkflowTitleDraft,
  savingWorkflowTitle,
  setSavingWorkflowTitle,
  setApiError,
  selectedProject,
  workflowDefinition,
  setSelectedWorkflow,
  setWorkflowDefinition,
  setWorkflows,
  getProjectId,
  savingBeforeRun,
  runningWorkflow,
  validatingWorkflow,
}) {
  return (
    <div className="editor-header">
      <div className="editor-title-area">
        <strong>Workflow Editor</strong>

        {selectedWorkflow ? (
          <div className="workflow-title-editor">
            {editingWorkflowTitle ? (
              <>
                <input
                  className="workflow-title-input"
                  value={workflowTitleDraft}
                  autoFocus
                  disabled={savingWorkflowTitle}
                  onChange={(event) =>
                    setWorkflowTitleDraft(event.target.value)
                  }
                  onKeyDown={async (event) => {
                    if (event.key === "Escape") {
                      setEditingWorkflowTitle(false);
                      setWorkflowTitleDraft(
                        selectedWorkflow.name,
                      );
                      return;
                    }

                    if (event.key !== "Enter") {
                      return;
                    }

                    event.preventDefault();

                    const name = workflowTitleDraft.trim();

                    if (!name || savingWorkflowTitle) {
                      return;
                    }

                    try {
                      setSavingWorkflowTitle(true);
                      setApiError("");

                      const projectId =
                        getProjectId(selectedProject);

                      await saveWorkflow(
                        projectId,
                        selectedWorkflow.id,
                        {
                          ...(workflowDefinition || {}),
                          name,
                        },
                      );

                      setSelectedWorkflow({
                        ...selectedWorkflow,
                        name,
                      });

                      setWorkflowDefinition({
                        ...(workflowDefinition || {}),
                        name,
                      });

                      setWorkflows((current) =>
                        current.map((workflow) =>
                          workflow.id ===
                          selectedWorkflow.id
                            ? {
                                ...workflow,
                                name,
                              }
                            : workflow,
                        ),
                      );

                      setEditingWorkflowTitle(false);
                    } catch (error) {
                      setApiError(error.message);
                    } finally {
                      setSavingWorkflowTitle(false);
                    }
                  }}
                />

                <button
                  type="button"
                  className="workflow-title-cancel"
                  disabled={savingWorkflowTitle}
                  onClick={() => {
                    setEditingWorkflowTitle(false);
                    setWorkflowTitleDraft(
                      selectedWorkflow.name,
                    );
                  }}
                  aria-label="Cancel title editing"
                  title="Cancel"
                >
                  ×
                </button>
              </>
            ) : (
              <>
                <span className="workflow-title-name">
                  {selectedWorkflow.name}
                </span>

                <button
                  type="button"
                  className="workflow-title-edit"
                  onClick={() => {
                    setWorkflowTitleDraft(
                      selectedWorkflow.name,
                    );
                    setEditingWorkflowTitle(true);
                  }}
                  aria-label="Edit workflow title"
                  title="Edit workflow title"
                >
                  <svg
                    viewBox="0 0 24 24"
                    width="14"
                    height="14"
                    aria-hidden="true"
                  >
                    <path
                      d="M4 16.5V20h3.5L18.8 8.7l-3.5-3.5-3.5 3.5L4 16.5Zm12.7-12.7 3.5 3.5 1.1-1.1a1.5 1.5 0 0 0 0-2.1l-1.4-1.4a1.5 1.5 0 0 0-2.1 0l-1.1 1.1Z"
                      fill="currentColor"
                    />
                  </svg>
                </button>
              </>
            )}
          </div>
        ) : (
          <span>No workflow selected</span>
        )}
      </div>

      <div className="editor-status">
        {savingBeforeRun
          ? "Saving"
          : runningWorkflow
            ? "Running"
            : validatingWorkflow
              ? "Validating"
              : selectedWorkflow
                ? "Ready"
                : "No workflow selected"}
      </div>
    </div>
  );
}

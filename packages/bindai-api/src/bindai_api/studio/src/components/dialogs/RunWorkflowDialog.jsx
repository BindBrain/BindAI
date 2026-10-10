export default function RunWorkflowDialog({
  Modal,
  showRunDialog,
  selectedProject,
  selectedWorkflow,
  isConnected,
  runningWorkflow,
  resolvingHumanTask,
  savingBeforeRun,
  runVariables,
  runError,
  runResult,
  setShowRunDialog,
  setRunVariables,
  handleRunWorkflow,
  handleResolveHumanTask,
}) {
  if (
    !showRunDialog ||
    !selectedProject ||
    !selectedWorkflow ||
    !isConnected
  ) {
    return null;
  }

  const status = runResult?.waiting
    ? "Waiting for approval"
    : runResult?.success === false
      ? "Failed"
      : runResult
        ? "Completed"
        : runningWorkflow
          ? "Running"
          : "Ready";

  const statusClass = runResult?.waiting
    ? "studio-run-status waiting"
    : runResult?.success === false
      ? "studio-run-status error"
      : runResult
        ? "studio-run-status success"
        : "studio-run-status";

  const output =
    runResult?.result?.output ??
    runResult?.output ??
    null;

  return (
    <Modal
      title={`Run Workflow — ${selectedWorkflow.name}`}
      onClose={() => {
        if (!runningWorkflow && !resolvingHumanTask) {
          setShowRunDialog(false);
        }
      }}
    >
      <form
        className="studio-modal-form"
        onSubmit={async (event) => {
          event.preventDefault();
          await handleRunWorkflow();
        }}
      >
        {!runResult && (
          <>
            <label>Input Variables</label>

            <textarea
              autoFocus
              value={runVariables}
              onChange={(event) =>
                setRunVariables(event.target.value)
              }
              rows={9}
              spellCheck={false}
              placeholder={'{\n  "input": "Hello"\n}'}
              disabled={runningWorkflow}
            />

            <p>
              Provide workflow variables as a JSON object.
              Agent nodes can read variables such as{" "}
              <code>input</code>.
            </p>
          </>
        )}

        {runError && (
          <div className="api-error">
            {runError}
          </div>
        )}

        {runResult && (
          <>
            <div className={statusClass}>
              <strong>Status</strong>
              <span>{status}</span>
            </div>

            {runResult.instance_id && (
              <div
                style={{
                  marginBottom: "16px",
                  fontSize: "12px",
                  color: "#667085",
                }}
              >
                <strong>Run ID:</strong>{" "}
                <code>{runResult.instance_id}</code>
              </div>
            )}

            {runResult.waiting &&
              runResult.human_task && (
                <div
                  style={{
                    marginBottom: "16px",
                    padding: "14px",
                    borderRadius: "8px",
                    border: "1px solid #d7dce2",
                    background: "#fafbfc",
                  }}
                >
                  <div
                    className="inspector-section-title"
                    style={{ marginTop: 0 }}
                  >
                    Human Approval Required
                  </div>

                  <div
                    style={{
                      fontSize: "13px",
                      lineHeight: 1.5,
                      marginBottom: "12px",
                    }}
                  >
                    Workflow execution is paused and requires
                    a human decision before it can continue.
                  </div>

                  <div
                    style={{
                      display: "grid",
                      gap: "6px",
                      marginBottom: "14px",
                      fontSize: "12px",
                    }}
                  >
                    <div>
                      <strong>Task:</strong>{" "}
                      {runResult.human_task.id}
                    </div>

                    <div>
                      <strong>Node:</strong>{" "}
                      {runResult.human_task.node_id}
                    </div>

                    {runResult.human_task.assignee && (
                      <div>
                        <strong>Assignee:</strong>{" "}
                        {runResult.human_task.assignee}
                      </div>
                    )}

                    {runResult.human_task.role && (
                      <div>
                        <strong>Role:</strong>{" "}
                        {runResult.human_task.role}
                      </div>
                    )}
                  </div>

                  <div
                    className="studio-modal-actions"
                    style={{
                      justifyContent: "flex-start",
                    }}
                  >
                    <button
                      type="button"
                      className="run-button"
                      disabled={resolvingHumanTask}
                      onClick={() =>
                        handleResolveHumanTask("approved")
                      }
                    >
                      {resolvingHumanTask
                        ? "Processing..."
                        : "Approve"}
                    </button>

                    <button
                      type="button"
                      disabled={resolvingHumanTask}
                      onClick={() =>
                        handleResolveHumanTask("rejected")
                      }
                    >
                      Reject
                    </button>
                  </div>
                </div>
              )}

            {output && (
              <>
                <div className="inspector-section-title">
                  Output
                </div>

                <pre
                  style={{
                    margin: "0 0 16px",
                    padding: "12px",
                    borderRadius: "8px",
                    background: "#f6f7f9",
                    border: "1px solid #e2e5e9",
                    overflow: "auto",
                    maxHeight: "220px",
                    fontSize: "12px",
                    lineHeight: 1.5,
                  }}
                >
                  {JSON.stringify(output, null, 2)}
                </pre>
              </>
            )}

            <details>
              <summary
                style={{
                  cursor: "pointer",
                  fontSize: "13px",
                  fontWeight: 600,
                  marginBottom: "8px",
                }}
              >
                Raw execution result
              </summary>

              <pre
                style={{
                  margin: 0,
                  padding: "12px",
                  borderRadius: "8px",
                  background: "#f6f7f9",
                  border: "1px solid #e2e5e9",
                  overflow: "auto",
                  maxHeight: "280px",
                  fontSize: "12px",
                  lineHeight: 1.5,
                }}
              >
                {JSON.stringify(runResult, null, 2)}
              </pre>
            </details>
          </>
        )}

        <div className="studio-modal-actions">
          <button
            type="button"
            onClick={() => setShowRunDialog(false)}
            disabled={
              runningWorkflow || resolvingHumanTask
            }
          >
            Close
          </button>

          <button
            type="submit"
            className="run-button"
            disabled={
              runningWorkflow ||
              resolvingHumanTask ||
              Boolean(runResult?.waiting)
            }
          >
            {savingBeforeRun
              ? "Saving..."
              : runningWorkflow
                ? "Running..."
                : "Run Workflow"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

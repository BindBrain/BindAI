from bindai_workflow import WorkflowBuilder

workflow = (
    WorkflowBuilder("research")
    .start_node()
    .end_node()
    .build()
)

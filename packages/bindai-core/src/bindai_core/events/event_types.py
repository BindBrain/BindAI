class EventTypes:

    #
    # Application
    #

    APPLICATION_STARTED = "application.started"
    APPLICATION_STOPPED = "application.stopped"

    #
    # Agent
    #

    AGENT_STARTED = "agent.started"
    AGENT_FINISHED = "agent.finished"

    #
    # Workflow
    #

    WORKFLOW_STARTED = "workflow.started"
    WORKFLOW_FINISHED = "workflow.finished"

    NODE_STARTED = "node.started"
    NODE_COMPLETED = "node.completed"

    #
    # Human
    #

    HUMAN_TASK_CREATED = "human.task.created"
    HUMAN_TASK_COMPLETED = "human.task.completed"

    #
    # Model
    #

    MODEL_INVOKED = "model.invoked"

    #
    # Tools
    #

    TOOL_EXECUTED = "tool.executed"

    #
    # Memory
    #

    MEMORY_READ = "memory.read"
    MEMORY_WRITTEN = "memory.written"

    #
    # MCP
    #

    MCP_CONNECTED = "mcp.connected"

    MCP_DISCONNECTED = "mcp.disconnected"
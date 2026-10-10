export function workflowToReactFlow(definition) {
  const workflow = definition.workflow || definition;

  const nodes = Array.isArray(workflow.nodes)
    ? workflow.nodes.map((node, index) => {
        const configuration = {
          ...(node.configuration || {}),

          ...(node.type === "agent"
            ? {
                agent:
                  node.agent ??
                  node.configuration?.agent ??
                  "",
                input_variable:
                  node.input_variable ??
                  node.configuration?.input_variable ??
                  "input",
                output_variable:
                  node.output_variable ??
                  node.configuration?.output_variable ??
                  "agent_output",
                input_mapping:
                  node.input_mapping ??
                  node.configuration?.input_mapping ??
                  "",
              }
            : {}),

          ...(node.type === "tool"
            ? {
                tool:
                  node.tool ??
                  node.configuration?.tool ??
                  "",
                output_variable:
                  node.output_variable ??
                  node.configuration?.output_variable ??
                  "tool_output",
                  parameter_mapping: Object.fromEntries(
                    Object.entries(
                      node.parameter_mapping ??
                        node.configuration?.parameter_mapping ??
                        {},
                    ).map(([parameter, variable]) => [
                      parameter,
                      typeof variable === "string" && variable.includes("→")
                        ? variable.split("→").pop().trim()
                        : variable,
                    ]),
                  ),
              }
            : {}),

          ...(node.type === "decision"
            ? {
                expression:
                  node.expression ??
                  node.configuration?.expression ??
                  "",
              }
            : {}),

          ...(node.type === "condition"
            ? {
                expression:
                  node.expression ??
                  node.configuration?.expression ??
                  "",
              }
            : {}),
            ...(node.type === "loop" || node.type === "loopnode"
                ? {
                    expression:
                      node.expression ??
                      node.configuration?.expression ??
                      "",
                  }
                : {}),
          ...(node.type === "subworkflow" ||
          node.type === "subworkflownode"
            ? {
                workflow_id:
                  node.workflow_id ??
                  node.configuration?.workflow_id ??
                  "",
              }
            : {}),

          ...(
            node.type === "humantask" ||
            node.type === "human_task" ||
            node.type === "humantasknode"
              ? {
                  form:
                    node.form ??
                    node.configuration?.form ??
                    "",
                }
              : {}
          ),

          ...(node.position
            ? {
                position: node.position,
              }
            : {}),
        };

        return {
          id: node.id || `node-${index}`,

          type: "bindai",

          position: node.position || {
            x: 0,
            y: index * 120,
          },

          data: {
            label: node.name || node.id,
            type: node.type,
            configuration,
          },
        };
      })
    : [];

  const edges = Array.isArray(workflow.edges)
    ? workflow.edges.map((edge, index) => ({
        id: `edge-${index}-${edge.from}-${edge.to}`,

        source: edge.from,

        target: edge.to,

        ...(edge.port
          ? {
              sourceHandle: edge.port,
              label: edge.port,
            }
          : {}),
      }))
    : [];

  return {
    nodes,
    edges,
  };
}

export function reactFlowToWorkflow(
    definition,
    nodes,
    edges,
  ) {
    const workflow =
      definition.workflow || definition;

    return {
      version: definition.version || 1,

      workflow: {
        id: workflow.id,
        name: workflow.name,

        nodes: nodes.map((node) => ({
          id: node.id,

          type:
            node.data?.type || "unknown",

          ...(node.data?.label
            ? {
                name: node.data.label,
              }
            : {}),

          ...(node.data?.configuration || {}),

          position: {
            x: node.position.x,
            y: node.position.y,
          },
        })),

        edges: edges.map((edge) => ({
          from: edge.source,
          to: edge.target,

          ...(edge.sourceHandle
            ? {
                port: edge.sourceHandle,
              }
            : {}),
        })),
      },
    };
  }

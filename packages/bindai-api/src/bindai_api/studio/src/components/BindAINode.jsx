import {
	Handle,
	Position,
  } from "@xyflow/react";

  import NodeIcon from "./NodeIcon";

  const NODE_DESCRIPTIONS = {
	start: "Starts the workflow execution.",
	end: "Marks the end of the workflow.",
	agent: "Runs a configured BindAI agent.",
	tool: "Executes a reusable project tool.",
	condition: "Branches execution using a condition.",
	decision: "Branches execution using an expression.",
	parallel: "Runs multiple workflow branches.",
	join: "Waits for parallel branches to complete.",
	loop: "Repeats a workflow branch while a condition is true.",
	humantask: "Pauses execution for human interaction.",
	human: "Pauses execution for human interaction.",
	subworkflow: "Runs another workflow as a reusable component.",
  };

  export function getNodeDescription(type, label) {
	return (
	  NODE_DESCRIPTIONS[type] ||
	  label ||
	  "Workflow node."
	);
  }

  export default function BindAINode({ data }) {
	const type = String(data?.type || "").toLowerCase();

	const isHumanApproval =
	  type === "humantask" ||
	  type === "human_task" ||
	  type === "humantasknode";

	const isCondition =
	  type === "condition" ||
	  type === "conditionnode" ||
	  type === "decision" ||
	  type === "decisionnode";


        const isLoop =
          type === "loop" ||
          type === "loopnode";
	return (
	  <div
		className="bindai-node"
		title={getNodeDescription(type, data?.label)}
	  >
		<Handle
		  type="target"
		  position={Position.Left}
		/>

		<div className="bindai-node-header">
		  <span className="bindai-node-icon">
			<NodeIcon
			  type={type}
			  size={13}
			/>
		  </span>

		  <span className="bindai-node-title">
			{data.label}
		  </span>
		</div>

		{data.type && (
		  <div className="bindai-node-type">
			{data.type}
		  </div>
		)}

		{isCondition ? (
		  <>
			<Handle
			  type="source"
			  id="true"
			  position={Position.Right}
			  style={{ top: "35%" }}
			/>

			<Handle
			  type="source"
			  id="false"
			  position={Position.Right}
			  style={{ top: "65%" }}
			/>
		  </>
		) : isHumanApproval ? (
		  <>
			<Handle
			  type="source"
			  id="approved"
			  position={Position.Right}
			  style={{ top: "35%" }}
			/>

			<Handle
			  type="source"
			  id="rejected"
			  position={Position.Right}
			  style={{ top: "65%" }}
			/>
		  </>
                ) : isLoop ? (
                  <>
                        <Handle
                          type="source"
                          id="body"
                          position={Position.Right}
                          style={{ top: "35%" }}
                        />

                        <Handle
                          type="source"
                          id="exit"
                          position={Position.Right}
                          style={{ top: "65%" }}
                        />
                  </>
                ) : (
                  <Handle
                        type="source"
                        position={Position.Right}
                  />
		)}
	  </div>
	);
  }

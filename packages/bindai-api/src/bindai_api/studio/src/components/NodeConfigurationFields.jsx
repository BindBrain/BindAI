export default function NodeConfigurationFields({
	field,
	nodeType,
	selectedNode,
	tools,
	agents,
        workflows,
	forms,
	isConnected,
	handleNodeConfigurationChange,
  }) {
	const configuration =
	  selectedNode.data?.configuration || {};

	const selectedTool =
	  tools.find(
		(tool) => tool.id === configuration.tool,
	  ) || null;

	const value =
	  configuration[field.name];

	if (field.type === "boolean") {
	  return (
		<label
		  key={field.name}
		  className="inspector-checkbox"
		>
		  <span>
			{field.name}
			{field.required ? " *" : ""}
		  </span>

		  <input
			type="checkbox"
			checked={Boolean(value)}
			disabled={!isConnected}
			onChange={(event) =>
			  handleNodeConfigurationChange(
				field.name,
				event.target.checked,
			  )
			}
		  />
		</label>
	  );
	}

	if (
	  field.type === "integer" ||
	  field.type === "number"
	) {
	  return (
		<div
		  className="inspector-field"
		  key={field.name}
		>
		  <label>
			{field.name}
			{field.required ? " *" : ""}
		  </label>

		  <input
			type="number"
			disabled={!isConnected}
			value={
			  value === undefined ||
			  value === null
				? ""
				: value
			}
			onChange={(event) => {
			  const raw =
				event.target.value;

			  if (raw === "") {
				handleNodeConfigurationChange(
				  field.name,
				  null,
				);
				return;
			  }

			  handleNodeConfigurationChange(
				field.name,
				field.type === "integer"
				  ? Number.parseInt(
					  raw,
					  10,
					)
				  : Number.parseFloat(
					  raw,
					),
			  );
			}}
		  />
		</div>
	  );
	}

	if (field.type === "agent") {
	  return (
		<div
		  className="inspector-field"
		  key={field.name}
		>
		  <label>
			{field.name}
			{field.required ? " *" : ""}
		  </label>

		  {agents.length > 0 ? (
			<select
			  value={value || ""}
			  disabled={!isConnected}
			  onChange={(event) =>
				handleNodeConfigurationChange(
				  field.name,
				  event.target.value,
				)
			  }
			>
			  <option value="">
				Select an agent
			  </option>

			  {agents.map((agent) => (
				<option
				  key={agent.id}
				  value={agent.id}
				>
				  {agent.name}
				</option>
			  ))}
			</select>
		  ) : (
			<input
			  value={value || ""}
			  disabled={!isConnected}
			  placeholder="Agent ID"
			  onChange={(event) =>
				handleNodeConfigurationChange(
				  field.name,
				  event.target.value,
				)
			  }
			/>
		  )}
		</div>
	  );
	}

	/*
	 * HumanTaskNode uses the existing runtime capability field
	 * called "form". The value stored in the workflow is the Form
	 * resource ID.
	 */
        if (field.type === "workflow") {
          return (
                <div
                  className="inspector-field"
                  key={field.name}
                >
                  <label>
                        {field.name}
                        {field.required ? " *" : ""}
                  </label>

                  {workflows.length > 0 ? (
                        <select
                          value={value || ""}
                          disabled={!isConnected}
                          onChange={(event) =>
                                handleNodeConfigurationChange(
                                  field.name,
                                  event.target.value,
                                )
                          }
                        >
                          <option value="">
                                Select a workflow
                          </option>

                          {workflows.map((workflow) => (
                                <option
                                  key={workflow.id}
                                  value={workflow.id}
                                >
                                  {workflow.name || workflow.id}
                                </option>
                          ))}
                        </select>
                  ) : (
                        <input
                          value={value || ""}
                          disabled={!isConnected}
                          placeholder="Workflow ID"
                          onChange={(event) =>
                                handleNodeConfigurationChange(
                                  field.name,
                                  event.target.value,
                                )
                          }
                        />
                  )}

                  {workflows.length === 0 && (
                        <div className="field-hint">
                          Create a workflow in the project first.
                        </div>
                  )}
                </div>
          );
        }

	if (
	  field.name === "form" &&
	  (
		nodeType === "humantask" ||
		nodeType === "human_task" ||
		nodeType === "humantasknode"
	  )
	) {
	  return (
		<div
		  className="inspector-field"
		  key={field.name}
		>
		  <label>
			Approval Form
			{field.required ? " *" : ""}
		  </label>

		  <select
			value={value || ""}
			disabled={!isConnected}
			onChange={(event) =>
			  handleNodeConfigurationChange(
				field.name,
				event.target.value,
			  )
			}
		  >
			<option value="">
			  Select a form
			</option>

			{forms.map((form) => (
			  <option
				key={form.id}
				value={form.id}
			  >
				{form.name}
			  </option>
			))}
		  </select>

		  {forms.length === 0 && (
			<div className="field-hint">
			  Create a Form in the Forms
			  section first.
			</div>
		  )}
		</div>
	  );
	}

	if (field.type === "tool") {
	  return (
		<div
		  className="inspector-field"
		  key={field.name}
		>
		  <label>
			{field.name}
			{field.required ? " *" : ""}
		  </label>

		  <select
			value={value || ""}
			disabled={!isConnected}
			onChange={(event) =>
			  handleNodeConfigurationChange(
				field.name,
				event.target.value,
			  )
			}
		  >
			<option value="">
			  Select a tool
			</option>

			{tools.map((tool) => (
			  <option
				key={tool.id}
				value={tool.id}
			  >
				{tool.name}
			  </option>
			))}
		  </select>

		  {tools.length === 0 && (
			<div className="field-hint">
			  Add a tool to the project first.
			</div>
		  )}

		  {selectedTool &&
			Object.keys(
			  selectedTool.parameters || {},
			).length > 0 && (
			  <div className="field-hint">
				Parameters:{" "}
				{Object.entries(
				  selectedTool.parameters,
				)
				  .map(
					([name, parameter]) =>
					  `${name}${
						parameter.required
						  ? " *"
						  : ""
					  }`,
				  )
				  .join(", ")}
			  </div>
			)}

		  {selectedTool &&
			Object.keys(
			  selectedTool.parameters || {},
			).length > 0 && (
			  <div className="tool-parameter-mapping">
				<div className="field-hint">
				  Parameter mapping
				</div>

				{Object.entries(
				  selectedTool.parameters,
				).map(([name, parameter]) => {
				  const mapping =
					configuration.parameter_mapping ||
					{};

				  return (
					<div
					  className="tool-parameter-row"
					  key={name}
					>
					  <label>
						{name}
						{parameter.required
						  ? " *"
						  : ""}
					  </label>

					  <input
						value={mapping[name] || ""}
						disabled={!isConnected}
						placeholder="Workflow variable"
						onChange={(event) => {
						  handleNodeConfigurationChange(
							"parameter_mapping",
							{
							  ...(selectedNode.data?.configuration
								?.parameter_mapping || {}),
							  [name]:
								event.target.value,
							},
						  );
						}}
					  />
					</div>
				  );
				})}
			  </div>
			)}
		</div>
	  );
	}

	return (
	  <div
		className="inspector-field"
		key={field.name}
	  >
		<label>
		  {field.name}
		  {field.required ? " *" : ""}
		</label>

		{field.type === "expression" ||
		field.type === "callable" ||
                field.name === "input_mapping" ? (
		  <textarea
			value={
			  value === undefined ||
			  value === null
				? ""
				: String(value)
			}
			rows={4}
			disabled={!isConnected}
			placeholder={field.type}
			onChange={(event) =>
			  handleNodeConfigurationChange(
				field.name,
				event.target.value,
			  )
			}
		  />
		) : (
		  <input
			value={
			  value === undefined ||
			  value === null
				? ""
				: String(value)
			}
			disabled={!isConnected}
			placeholder={
			  field.default !== null &&
			  field.default !== undefined
				? String(field.default)
				: ""
			}
			onChange={(event) =>
			  handleNodeConfigurationChange(
				field.name,
				event.target.value,
			  )
			}
		  />
		)}
	  </div>
	);
  }

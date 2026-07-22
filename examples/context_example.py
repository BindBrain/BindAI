from bindai_core import ExecutionContext

ctx = ExecutionContext()

ctx.variables.set("company", "BindAI")

print("Execution ID:", ctx.execution_id)
print("State:", ctx.state.value)
print("Company:", ctx.variables.get("company"))

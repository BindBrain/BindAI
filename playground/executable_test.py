from bindai_core import ExecutionResult

result = ExecutionResult(
    success=True,
    output="BindAI Execution Layer Ready",
)

print(result.success)
print(result.output)

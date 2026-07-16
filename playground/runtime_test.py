from bindai_core import (
    BindRuntime,
    Executable,
    ExecutionContext,
    ExecutionResult,
)


class HelloExecutable(Executable):

    def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionResult:

        print("Hello from Runtime!")

        return ExecutionResult(
            success=True,
            output="Runtime executed successfully",
        )


runtime = BindRuntime()

result = runtime.execute(
    HelloExecutable()
)

print(result.success)
print(result.output)
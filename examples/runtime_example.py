from bindai_runtime import BindRuntime


class HelloWorkflow:

    def execute(self, context):

        print("Hello from BindAI Runtime")

        print(context.execution_id)

        return "Finished"


runtime = BindRuntime()

result = runtime.run(
    HelloWorkflow()
)

print(result.success)

print(result.value)
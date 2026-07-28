# Workflow Human

Demonstrates a workflow that pauses for a human task before continuing.

## Flow

```
Human Task
      │
      ▼
 Agent
      │
      ▼
    End
```

## Run

```bash
python main.py
```

## Expected Output

```
First Execution
----------------------------------------
Workflow paused.

Task
HumanTask(...)

Resuming workflow...
----------------------------------------

Workflow Result
----------------------------------------
Human task completed.
```

The first execution pauses because the workflow reaches a `HumanTaskNode`.

The example then simulates a user approving the task by calling:

```python
workflow.executor.resume(instance)
```

In a real application, the resume call would happen after a user completes the task through a UI or API.
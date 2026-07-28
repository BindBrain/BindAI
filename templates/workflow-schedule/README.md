# Workflow Schedule

Demonstrates the built-in workflow scheduler.

## Flow

```
Scheduler
    │
    ▼
Workflow
```

The scheduler keeps a list of workflow schedules.

This example checks which schedules are due and executes them manually.

## Run

```bash
python main.py
```

## Expected Output

```text
Checking schedules...
----------------------------------------
Running workflow: scheduled-workflow

Scheduled workflow executed.

Workflow Result
----------------------------------------
Workflow executed by scheduler.
```

## Schedule

```python
schedule = WorkflowSchedule(
    workflow_id=workflow.id,
    next_run=datetime.utcnow(),
    interval_seconds=60,
)
```

## Current Behavior

The scheduler currently provides:

- adding schedules
- checking due schedules
- rescheduling recurring workflows

Execution is performed manually by calling:

```python
scheduler.due()
```

This template intentionally avoids background threads or cron services.
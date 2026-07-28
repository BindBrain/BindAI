# Workflow Parallel

Demonstrates a fan-out / fan-in workflow.

```
Start
   │
Parallel
 ├── Agent A
 └── Agent B
      │
     Join
      │
     End
```

Both branches execute independently.

The Join node waits until every branch reaches it before continuing.

## Run

```bash
python main.py
```

Expected output

```text
Workflow Result
----------------------------------------
{
    "prompt_a": "...",
    "prompt_b": "...",
    "result_a": AgentResult(...),
    "result_b": AgentResult(...)
}
```
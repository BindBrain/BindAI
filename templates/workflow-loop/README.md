# Workflow Loop

This example demonstrates repeating a workflow node until a condition becomes false.

```
        ┌──────────────┐
        │              │
        ▼              │
     Loop Node ─────► Agent
        │              │
        │              │
        └──── false ───┘
               │
               ▼
              End
```

The workflow starts with:

```
counter = 0
```

The loop continues while:

```python
counter < 3
```

After each Agent execution:

```
counter += 1
```

The workflow exits after three iterations.

Run:

```bash
python main.py
```

Expected output:

```
Workflow Result
----------------------------------------
Loop executed.
```
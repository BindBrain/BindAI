# Workflow Condition

This example demonstrates conditional workflow execution.

## Flow

```
Start
   │
   ▼
Condition
 ┌──┴─────┐
 │        │
True    False
 │        │
 ▼        ▼
Agent   Agent
 │        │
 └──┬─────┘
    ▼
   End
```

## Setup

Copy the environment file.

```bash
cp .env.example .env
```

Add your API key.

```env
OPENAI_API_KEY=your_api_key
```

## Run

```bash
python main.py
```

## True branch

```python
instance.context.set(
    "approved",
    True,
)
```

Output:

```
Workflow Result
----------------------------------------
Request approved.
```

## False branch

```python
instance.context.set(
    "approved",
    False,
)
```

Output:

```
Workflow Result
----------------------------------------
Request rejected.
```

The workflow variables will also contain the executed branch result.
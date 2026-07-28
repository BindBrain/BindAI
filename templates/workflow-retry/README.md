# Workflow Retry

Demonstrates automatic retry when a node raises an exception.

## Flow

```
Retry Node
     │
     ▼
    End
```

The node intentionally fails twice before succeeding.

The executor retries automatically because a `RetryPolicy` is configured.

## Run

```bash
python main.py
```

## Expected Output

```
Attempt 1
Attempt 2
Attempt 3

Workflow Result
----------------------------------------
Succeeded after retries.
```

## Retry Policy

```python
instance.context.retry_policy = RetryPolicy(
    max_attempts=3,
)
```

The workflow executor retries failed nodes until either:

- the node succeeds
- the maximum number of attempts is reached
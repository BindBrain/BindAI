## Expected Output

```text
Starting long task...

Workflow Result
----------------------------------------
Workflow timeout.
```

The timeout is evaluated by the workflow executor after a node finishes executing.

A running node is **not interrupted**.

This means a long-running node may still update workflow variables before the timeout is detected.
class RuntimeException(Exception):
    """
    Base runtime exception.
    """


class RuntimeExecutionError(
    RuntimeException,
):
    """
    Executable failed.
    """


class RuntimeCancelled(
    RuntimeException,
):
    """
    Runtime cancelled.
    """

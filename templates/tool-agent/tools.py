from bindai import tool


@tool
def current_time() -> str:
    """
    Returns the current local time.
    """

    from datetime import datetime

    return datetime.now().strftime("%H:%M:%S")

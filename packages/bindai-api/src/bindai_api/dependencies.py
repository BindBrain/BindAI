from __future__ import annotations

from bindai.application import Application


def get_application() -> Application:
    from .app import get_configured_application

    application = get_configured_application()

    if not isinstance(application, Application):
        raise RuntimeError("The configured object is not a BindAI Application.")

    return application

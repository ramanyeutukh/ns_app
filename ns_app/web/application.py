from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from tortoise.contrib.fastapi import register_tortoise

from ns_app.db.config import TORTOISE_CONFIG
from ns_app.web.api.router import api_router
from ns_app.web.lifetime import register_shutdown_event, register_startup_event


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="ns_app",
        version=metadata.version("ns_app"),
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    # Configures tortoise orm.
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        add_exception_handlers=True,
    )

    return app

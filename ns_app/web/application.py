from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    return FastAPI(
        title="ns_app",
        version=metadata.version("ns_app"),
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )

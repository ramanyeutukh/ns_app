from collections.abc import Awaitable, Callable

from fastapi import FastAPI

from ns_app.redis.lifetime import init_redis, shutdown_redis


def register_startup_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application startup.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:
        app.middleware_stack = None
        init_redis(app)

        app.middleware_stack = app.build_middleware_stack()

    return _startup


def register_shutdown_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        await shutdown_redis(app)

    return _shutdown

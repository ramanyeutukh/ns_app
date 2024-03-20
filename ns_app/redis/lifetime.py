from fastapi import FastAPI
from redis.asyncio import ConnectionPool

from ns_app.settings import settings


def init_redis(app: FastAPI) -> None:
    """
    Create connection pool for redis.

    :param app: current fastapi application.
    """
    app.state.redis_pool = ConnectionPool.from_url(
        str(settings.redis.url),
    )


async def shutdown_redis(app: FastAPI) -> None:
    """
    Close redis connection pool.

    :param app: current FastAPI app.
    """
    await app.state.redis_pool.disconnect()

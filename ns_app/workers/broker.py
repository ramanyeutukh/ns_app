import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO

from ns_app.db.helpers import DramatiqDbMiddleware
from ns_app.settings import settings


def setup_broker() -> None:
    """Set up broker."""
    redis_broker = RedisBroker(url=str(settings.redis.url))
    redis_broker.add_middleware(AsyncIO())
    redis_broker.add_middleware(DramatiqDbMiddleware(), after=AsyncIO)
    dramatiq.set_broker(redis_broker)

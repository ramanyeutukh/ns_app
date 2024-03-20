from uuid import UUID

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO

from ns_app.db.helpers import DramatiqDbMiddleware
from ns_app.settings import settings
from ns_app.tasks.helpers import db_task_context

redis_broker = RedisBroker(url=str(settings.redis.url))
redis_broker.add_middleware(AsyncIO())
redis_broker.add_middleware(DramatiqDbMiddleware(), after=AsyncIO)
dramatiq.set_broker(redis_broker)


@dramatiq.actor
async def process_task_s3(amount: int, task_id: str) -> None:
    """Task for processing S3 files."""
    async with db_task_context(UUID(task_id)):
        print(f"Task done. Amount: {amount}")  # noqa: T201

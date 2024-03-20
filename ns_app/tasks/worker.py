from uuid import UUID

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO
from tortoise import Tortoise

from ns_app.db.config import TORTOISE_CONFIG
from ns_app.db.dao.task_dao import TaskDAO
from ns_app.db.models.task_model import TaskStatus
from ns_app.settings import settings

redis_broker = RedisBroker(url=str(settings.redis.url), middleware=[AsyncIO()])
dramatiq.set_broker(redis_broker)


@dramatiq.actor
async def process_task_s3(amount: int, task_id: str) -> None:
    """Task for processing S3 files."""
    await Tortoise.init(config=TORTOISE_CONFIG)
    await TaskDAO().update(UUID(task_id), TaskStatus.DONE)
    print(f"Task done. Amount: {amount}")  # noqa: T201

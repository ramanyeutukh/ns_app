import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from uuid import UUID

from ns_app.db.dao.task_dao import TaskDAO
from ns_app.db.models.task_model import TaskStatus

logger = logging.getLogger(__name__)


@asynccontextmanager
async def db_task_context(task_id: UUID) -> AsyncGenerator[None, None]:
    """Task context."""
    dao = TaskDAO()
    try:
        await dao.update(task_id, TaskStatus.IN_PROGRESS)
        yield
    except Exception:
        await dao.update(task_id, TaskStatus.FAILED)
        logger.exception("Task failed. ID: %s", task_id)
        raise
    else:
        await dao.update(task_id, TaskStatus.DONE)

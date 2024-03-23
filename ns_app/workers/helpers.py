import logging
from collections.abc import Callable
from functools import wraps
from typing import Any
from uuid import UUID

from ns_app.db.dao.task_dao import TaskDAO
from ns_app.enum.task import TaskStatus

logger = logging.getLogger(__name__)


async def manage_task_status(func):  # type: ignore[no-untyped-def] # noqa: ANN001, ANN201
    """Manage task status in a database decorator."""

    @wraps(func)
    async def wrapper(task_id: str, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        dao = TaskDAO()
        await dao.update(UUID(task_id), TaskStatus.IN_PROGRESS)
        try:
            # TODO: check if func is async or not
            return func(task_id, *args, **kwargs)
        except Exception:
            await dao.update(UUID(task_id), TaskStatus.FAILED)
            logger.exception("Task failed. ID: %s", task_id)
            raise
        else:
            await dao.update(UUID(task_id), TaskStatus.DONE)

    return wrapper

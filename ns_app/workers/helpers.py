import logging
from collections.abc import Callable
from functools import wraps
from typing import Any
from uuid import UUID

from dramatiq.asyncio import async_to_sync

from ns_app.db.dao.task_dao import TaskDAO
from ns_app.enum.task import TaskStatus

logger = logging.getLogger(__name__)


def manage_task_status(func):  # type: ignore[no-untyped-def] # noqa: ANN001, ANN201
    """Manage task status in a database decorator."""

    @wraps(func)
    def wrapper(task_id: str, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        dao = TaskDAO()
        async_to_sync(dao.update)(UUID(task_id), TaskStatus.IN_PROGRESS)
        try:
            result = func(task_id, *args, **kwargs)
            async_to_sync(dao.update)(UUID(task_id), TaskStatus.DONE)
            return result  # noqa: TRY300
        except Exception:
            async_to_sync(dao.update)(UUID(task_id), TaskStatus.FAILED)
            logger.exception("Task failed. ID: %s", task_id)
            raise

    return wrapper

from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response

from ns_app.db.dao.task_dao import TaskDAO
from ns_app.dto.task import TaskDTO
from ns_app.workers.tasks import process_task_s3

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{task_id}")
async def get_task(task_id: UUID, task_dao: TaskDAO = Depends()) -> TaskDTO | None:
    """
    Get task by uuid.

    :param task_id: task uuid.
    :return: task.
    """
    return await task_dao.get(task_id)


@router.post("/create/s3/", status_code=202)
async def create_task_s3(
    request: Request,
    response: Response,
    limit: int = 100,
    dao: TaskDAO = Depends(),
) -> TaskDTO:
    """
    Create task for S3.

    :return: task.
    """
    task = await dao.create()
    process_task_s3.send(str(task.id), limit)
    response.headers["Location"] = str(request.url_for("get_task", task_id=task.id))

    return task

from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response

from ns_app.db.dao.task_dao import TaskDAO
from ns_app.db.model.task_model import TaskModel
from ns_app.web.api.tasks.schema import TaskDTO

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{task_id}", response_model=TaskDTO | None)
async def get_task(task_id: UUID, task_dao: TaskDAO = Depends()) -> TaskModel | None:
    """
    Get task by uuid.

    :param task_id: task uuid.
    :return: task.
    """
    return await task_dao.get(task_id)


@router.post("/create/s3/", response_model=TaskDTO, status_code=202)
async def create_task_s3(
    request: Request,
    response: Response,
    task_dao: TaskDAO = Depends(),
) -> TaskModel:
    """
    Create task for S3.

    :return: task.
    """
    task = await task_dao.create()
    # TODO: Implement code to add task with amount to queue

    response.headers["Location"] = str(request.url_for("get_task", task_id=task.id))

    return task

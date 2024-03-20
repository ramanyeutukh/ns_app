from uuid import UUID

from ns_app.db.models.task_model import TaskModel, TaskStatus
from ns_app.dto.task_dto import TaskDTO


class TaskDAO:
    """Class for accessing task table."""

    async def create(self) -> TaskDTO:
        """
        Add single task to session.

        :param name: name of a task.
        :return: task DTO.
        """
        task = await TaskModel.create()
        return TaskDTO.model_validate(task)

    async def get(self, task_id: UUID) -> TaskDTO | None:
        """
        Get single task model by id.

        :param task_id: uuid of a task.
        :return: task DTO or None.
        """
        task = await TaskModel.get_or_none(id=task_id)
        if not task:
            return None

        return TaskDTO.model_validate(task)

    async def update(self, task_id: UUID, status: TaskStatus) -> TaskDTO | None:
        """
        Update task status.

        :param task_id: uuid of a task.
        :param status: new status.
        :return: task DTO or None.
        """
        task = await TaskModel.get_or_none(id=task_id)
        if not task:
            return None

        task.status = status
        await task.save()
        return TaskDTO.model_validate(task)

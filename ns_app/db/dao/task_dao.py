from uuid import UUID

from ns_app.db.models.task_model import TaskModel


class TaskDAO:
    """Class for accessing task table."""

    async def create(self) -> TaskModel:
        """
        Add single task to session.

        :param name: name of a task.
        """
        return await TaskModel.create()

    async def get(self, task_id: UUID) -> TaskModel | None:
        """
        Get single task model by id.

        :param task_id: uuid of a task.
        :return: task model or None.
        """
        return await TaskModel.get_or_none(id=task_id)

    async def update(self, task_id: UUID, status: int) -> TaskModel | None:
        """
        Update task status.

        :param task_id: uuid of a task.
        :param status: new status.
        :return: task model or None.
        """
        task = await TaskModel.get_or_none(id=task_id)
        if task:
            task.status = status
            await task.save()
        return task

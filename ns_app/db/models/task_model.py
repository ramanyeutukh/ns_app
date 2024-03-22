from tortoise import fields, models

from ns_app.enum.task import TaskStatus


class TaskModel(models.Model):
    """Task model."""

    id = fields.UUIDField(pk=True)
    status = fields.IntEnumField(TaskStatus, default=TaskStatus.PENDING)

    class Meta:  # noqa: D106
        table = "tasks"

    def __str__(self) -> str:
        return f"Task: {self.id}. Status: {self.status.name}"

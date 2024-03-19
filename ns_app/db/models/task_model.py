from enum import IntEnum

from tortoise import fields, models


class TaskStatus(IntEnum):
    """Enum for task status."""

    PENDING = 1
    IN_PROGRESS = 2
    DONE = 3
    FAILED = 4


class TaskModel(models.Model):
    """Task model."""

    id = fields.UUIDField(pk=True)
    status = fields.IntEnumField(TaskStatus, default=TaskStatus.PENDING)

    class Meta: # noqa: D106
        table="tasks"

    def __str__(self) -> str:
        return f"Task: {self.id}. Status: {self.status.name}"

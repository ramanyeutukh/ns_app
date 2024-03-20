"""DTOs for Task model."""

from uuid import UUID

from pydantic import BaseModel

from ns_app.db.models.task_model import TaskStatus


class TaskDTO(BaseModel):
    """DTO for Task model."""

    id: UUID
    status: TaskStatus

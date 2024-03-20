"""DTOs for Task model."""

from uuid import UUID

from ns_app.db.models.task_model import TaskStatus
from ns_app.dto.base import BaseDTO


class TaskDTO(BaseDTO):
    """DTO for Task model."""

    id: UUID
    status: TaskStatus

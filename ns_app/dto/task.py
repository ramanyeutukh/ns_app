"""DTOs for Task model."""

from uuid import UUID

from ns_app.dto.base import BaseDTO
from ns_app.enum.task import TaskStatus


class TaskDTO(BaseDTO):
    """DTO for Task model."""

    id: UUID
    status: TaskStatus

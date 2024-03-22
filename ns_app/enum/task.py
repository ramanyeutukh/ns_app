"""Enumeration for task."""

from enum import IntEnum


class TaskStatus(IntEnum):
    """Enum for task status."""

    PENDING = 1
    IN_PROGRESS = 2
    DONE = 3
    FAILED = 4

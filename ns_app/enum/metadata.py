"""Enumeration for metadata."""

from enum import StrEnum


class ArchEnum(StrEnum):
    """Architecture enumeration."""

    x32 = "x32"
    x64 = "x64"


class FileType(StrEnum):
    """File type enumeration."""

    exe = "exe"
    dll = "dll"

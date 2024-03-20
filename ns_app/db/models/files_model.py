from enum import StrEnum

from tortoise import fields, models


class ArchEnum(StrEnum):
    """Architecture enumeration."""

    x32 = "x32"
    x64 = "x64"


class MetadataModel(models.Model):
    """File metadata model."""

    id = fields.BigIntField(pk=True)
    path = fields.CharField(max_length=255)
    file_type = fields.CharField(max_length=255)
    arch = fields.CharEnumField(ArchEnum)
    numer_of_imports = fields.IntField()
    number_of_exports = fields.IntField()
    hash = fields.BigIntField(unique=True, index=True)

    class Meta:  # noqa: D106
        table = "metadata"

    def __str__(self) -> str:
        return f"Metadata {self.id}: {self.hash}"

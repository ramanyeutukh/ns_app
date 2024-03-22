from tortoise import fields, models

from ns_app.enum.metadata import ArchEnum, FileType


class MetadataModel(models.Model):
    """File metadata model."""

    id = fields.BigIntField(pk=True)
    path = fields.CharField(max_length=255)
    file_type = fields.CharEnumField(FileType, null=True)
    arch = fields.CharEnumField(ArchEnum, null=True)
    numer_of_imports = fields.IntField(null=True)
    number_of_exports = fields.IntField(null=True)
    hash = fields.BigIntField(unique=True, index=True)

    class Meta:  # noqa: D106
        table = "metadata"

    def __str__(self) -> str:
        return f"Metadata {self.id}: {self.hash}"

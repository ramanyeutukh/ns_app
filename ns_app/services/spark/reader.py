from abc import ABC, abstractmethod
from typing import Any, TextIO

from pyspark.sql import DataFrame, SparkSession


class BaseSparkReader(ABC):
    """Spark reader."""

    def __init__(self, session: SparkSession, limit: int | None = None):
        """Initialize the reader."""
        self.session = session
        self.limit = limit

    @abstractmethod
    def read(self, **options: Any) -> DataFrame:
        """Read data."""


class SparkS3Reader(BaseSparkReader):
    """Spark S3 Reader."""

    def __init__(
        self,
        session: SparkSession,
        files: list[str],
        file_format: str = "binaryFile",
    ):
        """Initialize the Reader."""
        super().__init__(session)
        self.files = [self.add_prefix(file) for file in files]
        self.file_format = file_format

    def add_prefix(self, path: str) -> str:
        """Add the S3a prefix to the path."""
        return f"s3a://{path}"

    def read(self, **options: Any) -> DataFrame:
        """Read data from a path."""
        return (
            self.session.read.format(self.file_format)
            .options(**options)
            .load(self.files)
        )


class SparkFileReader(BaseSparkReader):
    """Spark file Reader."""

    def __init__(
        self,
        session: SparkSession,
        file: TextIO,
        limit: int | None = None,
    ) -> None:
        """Initialize the Reader."""
        super().__init__(session, limit=limit)
        self.file = file

    def read(self, **options: Any) -> DataFrame:
        """Read data from a file."""
        raise NotImplementedError

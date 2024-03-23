import math
from abc import ABC, abstractmethod
from functools import reduce
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
        paths: list[str],
        limit: int | None = None,
        file_format: str = "binaryFile",
    ):
        """Initialize the Reader."""
        super().__init__(session, limit=limit)
        self.paths = [self.add_prefix(path) for path in paths]
        self.file_format = file_format

    def partition(self, df: DataFrame, partition_size: int = 1000) -> DataFrame:
        """Partition the DataFrame."""
        total_items = df.count()
        num_partitions = max(1, math.ceil(total_items / partition_size))
        return df.repartition(num_partitions)

    def add_prefix(self, path: str) -> str:
        """Add the S3a prefix to the path."""
        return f"s3a://{path}"

    def read(self, **options: Any) -> DataFrame:
        """Read data from a S3 folder."""
        files = [self.read_path(path, **options) for path in self.paths]
        df = reduce(lambda df, df2: df.union(df2), files)
        return self.partition(df)

    def read_path(self, path: str, **options: Any) -> DataFrame:
        """Read data from a path."""
        df = self.session.read.format(self.file_format).options(**options).load(path)
        if self.limit:
            df = df.limit(self.limit)

        return df


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

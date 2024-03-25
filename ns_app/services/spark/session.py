from types import TracebackType
from typing import Any

from pyspark import SparkConf
from pyspark.sql import SparkSession as BaseStarkSession

from ns_app.settings import settings


class SparkSession:
    """Spark session."""

    def __init__(self, **options: Any) -> None:
        """Initialize the Spark session."""
        self.config = settings.spark.to_config | options
        self.session: BaseStarkSession | None = None

    @property
    def spark_config(self) -> SparkConf:
        """Get the Spark configuration."""
        return SparkConf().setAll(list(self.config.items()))

    def get_or_create(self) -> BaseStarkSession:
        """Get or create a SparkSession."""
        return BaseStarkSession.builder.config(conf=self.spark_config).getOrCreate()

    def __enter__(self) -> BaseStarkSession:
        """Enter the Spark session."""
        self.session = self.get_or_create()
        return self.session

    def __exit__(
        self,
        typ: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Close the Spark session."""
        if self.session:
            self.session.stop()

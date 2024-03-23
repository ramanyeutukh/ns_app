from typing import Any

from pyspark import SparkConf
from pyspark.sql import SparkSession as BaseStarkSession
from settings import settings


class SparkSession:
    """Spark session."""

    def __init__(self, **options: Any) -> None:
        """Initialize the Spark session."""
        self.config = settings.spark.to_config | options

    @property
    def spark_config(self) -> SparkConf:
        """Get the Spark configuration."""
        return SparkConf().setAll(self.config.items())

    def get_or_create(self) -> BaseStarkSession:
        """Get or create a SparkSession."""
        return BaseStarkSession.builder.config(conf=self.spark_config).getOrCreate()

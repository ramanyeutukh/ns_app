from pyspark.sql import DataFrame
from pyspark.sql.functions import col, xxhash64

from ns_app.services.spark.reader import BaseSparkReader
from ns_app.services.spark.udf import get_file_metadata
from ns_app.services.spark.writer import BaseSparkWriter


class SparkClient:
    """Spark client."""

    def __init__(self, reader: BaseSparkReader, writer: BaseSparkWriter) -> None:
        """Initialize the client."""
        self.reader = reader
        self.writer = writer

    def read(self) -> DataFrame:
        """Read data."""
        return self.reader.read()

    def write(self, df: DataFrame, mode: str = "append") -> DataFrame:
        """Save DataFrame to the database."""
        return self.writer.write(df, mode)

    def update_columns(self, df: DataFrame) -> DataFrame:
        """Add a hash and metadata columns to the DataFrame."""
        df = df.withColumn("hash", xxhash64(col("content")))
        df = df.withColumn("meta", get_file_metadata(col("content")))
        return df.select(*df.columns, "meta.*").drop("meta", "content")

    def drop_duplicates(self, df: DataFrame) -> DataFrame:
        """Drop duplicates by field in the DataFrame."""
        df = df.dropDuplicates(["hash"])
        return self.writer.clean_duplicates(df, "hash")

    def process_task(self) -> None:
        """Process a task."""
        df = self.read()
        df = self.update_columns(df)
        df = self.drop_duplicates(df)
        self.write(df)

from abc import ABC, abstractmethod
from typing import Any

from pyspark.sql import DataFrame, DataFrameReader, DataFrameWriter, SparkSession
from pyspark.sql.functions import col

from ns_app.db.helpers import get_metadata_table_details
from ns_app.settings import settings


class BaseSparkWriter(ABC):
    """Base Spark Writer."""

    def __init__(self, session: SparkSession) -> None:
        """Initialize the writer."""
        self.session = session

    @abstractmethod
    def write(self, df: DataFrame, mode: str = "append") -> DataFrame:
        """Write DataFrame."""

    @abstractmethod
    def clean_duplicates(self, df: DataFrame, by_field: str) -> DataFrame:
        """Clean duplicates by field."""


class SparkDBWriter(BaseSparkWriter):
    """Spark database writer."""

    def __init__(self, session: SparkSession) -> None:
        """Initialize the database."""
        self.session = session
        self.table, self.columns = get_metadata_table_details()

    def get_db(
        self,
        df: DataFrame | DataFrameReader | DataFrameWriter,
        **options: Any,
    ) -> DataFrame:
        """Get the database and table."""
        return df.jdbc(table=self.table, **settings.db.jdbc_config, **options)  # type: ignore [operator, return-value]

    def clean_duplicates(self, df: DataFrame, by_field: str) -> DataFrame:
        """
        Clean duplicates by field.

        This method gets hashes from the current DataFrame.
        Then it tries to get the same hashes from the database.
        If it finds any, it removes them from the current DataFrame.

        :param df: DataFrame.
        :param by_field: field to clean by

        :raises ValueError: if the field is not found in the DataFrame.
        :return: cleaned DataFrame.
        """
        if by_field not in df.columns:
            msg = f"Column {by_field} not found in DataFrame."
            raise ValueError(msg)

        values = df.select(by_field).rdd.map(lambda x: x[0]).collect()
        db_values = self.get_db(self.session.read).filter(col(by_field).isin(values))
        return df.join(other=db_values, on=by_field, how="leftanti")

    def write(
        self,
        df: DataFrame,
        mode: str = "append",
        extra_columns: list[str] | None = None,
    ) -> DataFrame:
        """
        write DataFrame to the database.

        :param df: DataFrame.
        :param mode: write mode. Options: append, overwrite, ignore, error.
        :param extra_columns: extra columns to add.

        :raises ValueError: if columns do not match.
        :return: DataFrame.
        """
        if extra_columns:
            self.columns.extend(extra_columns)

        if set(df.columns).issubset(set(self.columns)):
            msg = f"Columns {df.columns} do not match {self.columns}."
            raise ValueError(msg)

        return self.get_db(df.select(self.columns).write, mode=mode)

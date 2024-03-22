import logging

from dramatiq.asyncio import async_to_sync
from dramatiq.middleware import Middleware
from tortoise import Tortoise, connections

from ns_app.db.config import TORTOISE_CONFIG
from ns_app.db.models import MetadataModel, TaskModel

DB_MAPPER = {
    MetadataModel.Meta.table: MetadataModel,
    TaskModel.Meta.table: TaskModel,
}


class DramatiqDbMiddleware(Middleware):
    """Database middleware."""

    def __init__(self) -> None:
        """Initialize the middleware."""
        self.logger = logging.getLogger(__name__)

    def before_worker_boot(self, broker, worker) -> None:  # type: ignore[no-untyped-def] # noqa: ANN001, ARG002
        """Set up the database."""
        async_to_sync(Tortoise.init)(config=TORTOISE_CONFIG)
        self.logger.info("Database initialized")

    def after_worker_shutdown(self, broker, worker) -> None:  # type: ignore[no-untyped-def] # noqa: ANN001, ARG002
        """Close the database."""
        async_to_sync(connections.close_all)()
        self.logger.info("Database closed")


def get_table_model_columns(table_name: "str") -> list[str]:
    """
    Get db column names from the table.

    :param table_name: name of the table.

    :raises ValueError: if the table is not found.
    :return: list of db column names.
    """
    if table_name not in DB_MAPPER:
        msg = f"Table {table_name} not found."
        raise ValueError(msg)

    return [
        item["db_column"] for item in DB_MAPPER[table_name].describe()["data_fields"]
    ]

import logging

from dramatiq.asyncio import async_to_sync
from dramatiq.middleware import Middleware
from tortoise import Tortoise, connections

from ns_app.db.config import TORTOISE_CONFIG
from ns_app.db.models import MetadataModel


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


def get_metadata_table_details() -> tuple[str, list[str]]:
    """Get metadata table name."""
    columns = [item["db_column"] for item in MetadataModel.describe()["data_fields"]]
    return MetadataModel.Meta.table, columns

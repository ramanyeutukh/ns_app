import logging
import math

import dramatiq

from ns_app.services.spark.client import SparkClient
from ns_app.services.spark.reader import SparkS3Reader
from ns_app.services.spark.session import SparkSession
from ns_app.services.spark.writer import SparkDBWriter
from ns_app.settings import settings
from ns_app.workers.broker import setup_broker
from ns_app.workers.helpers import manage_task_status

setup_broker()
logger = logging.getLogger(__name__)


@dramatiq.actor
@manage_task_status
async def process_task_s3(task_id: str, amount: int) -> None:
    """Task for processing S3 files."""
    logger.info("Processing task %s", task_id)
    limit = math.ceil(amount / len(settings.s3.folders))

    session = SparkSession().get_or_create()
    reader = SparkS3Reader(session, settings.s3.folders, limit=limit)
    writer = SparkDBWriter(session)
    SparkClient(reader, writer).process_task()

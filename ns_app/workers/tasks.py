import logging
import math

import dramatiq

from ns_app.services.s3.paginator import S3Paginator
from ns_app.services.spark.client import SparkClient
from ns_app.services.spark.reader import SparkS3Reader
from ns_app.services.spark.session import SparkSession
from ns_app.services.spark.writer import SparkDBWriter
from ns_app.settings import settings
from ns_app.workers.broker import setup_broker
from ns_app.workers.helpers import manage_task_status

setup_broker()
logger = logging.getLogger(__name__)


@dramatiq.actor(time_limit=60 * 60 * 1000)  # 1 hour
@manage_task_status
def process_task_s3(task_id: str, amount: int) -> None:
    """Task for processing S3 files."""
    logger.info("Processing task %s", task_id)
    limit = math.ceil(amount / len(settings.s3.folders))
    s3 = S3Paginator()
    with SparkSession() as session:
        for folder in settings.s3.folders:
            paginator = s3.paginate(
                settings.s3.bucket,
                folder,
                limit=limit,
            )
            for files in paginator:
                reader = SparkS3Reader(session, files)
                writer = SparkDBWriter(session)
                SparkClient(reader, writer).process_task()

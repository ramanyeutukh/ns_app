from collections.abc import Generator

import boto3
from botocore import UNSIGNED
from botocore.config import Config

from ns_app.settings import settings


class S3Paginator:
    """Reads objects from an S3 bucket."""

    def __init__(self) -> None:
        """Initialize the S3 reader."""
        self.s3_client = boto3.client(
            "s3",
            region_name=settings.s3.region_name,
            config=Config(signature_version=UNSIGNED),
        )

    def paginate(
        self,
        bucket: str,
        folder: str | None,
        limit: int | None = None,
    ) -> Generator[list[str], None, None]:
        """Read pages from the S3 bucket."""
        paginator = self.s3_client.get_paginator("list_objects_v2")

        paginator_config = {
            "Bucket": bucket,
            "PageSize": settings.s3.page_size,
        }

        if limit:
            paginator_config["MaxItems"] = limit
        if folder:
            paginator_config["Prefix"] = folder
        page_iterator = paginator.paginate(
            Bucket=bucket,
            PaginationConfig=paginator_config,
        )
        for page in page_iterator:
            yield [f"{bucket}/{i['Key']}" for i in page.get("Contents", [])]

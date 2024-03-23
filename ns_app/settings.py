import enum
from typing import Any

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class RedisConfig(BaseModel):
    """Redis configuration."""

    host: str = "ns_app-redis"
    port: int = 6379
    user: str | None = None
    password: str | None = None
    base: int | None = None

    @property
    def url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ""
        if self.base is not None:
            path = f"/{self.base}"
        return URL.build(
            scheme="redis",
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            path=path,
        )


class DBConfig(BaseModel):
    """Database configuration."""

    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = ""
    base: str = "ns_app"
    echo: bool = False

    @property
    def url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgres",
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            path=f"/{self.base}",
        )

    @property
    def jdbc_config(self) -> dict[str, Any]:
        """
        Convert to JDBC configuration.

        return: dict with JDBC configuration.
        """
        return {
            "properties": {
                "user": self.user,
                "password": self.password,
                "driver": "org.postgresql.Driver",
            },
            "url": f"jdbc:postgresql://{self.host}:{self.port}/{self.base}",
        }


class SparkConfig(BaseModel):
    """Spark configuration."""

    master: str = Field(default="local[*]", alias="spark.master")
    app_name: str = Field(default="File processor", alias="spark.app.name")
    executor_memory: str = Field(default="12g", alias="spark.executor.memory")
    executor_cores: int = Field(default=2, alias="spark.executor.cores")
    creds_provider: str = Field(
        default="org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider",
        alias="spark.hadoop.fs.s3a.aws.credentials.provider",
    )

    @property
    def to_config(self) -> dict[str, Any]:
        """
        Convert to Spark configuration.

        :return: dict with spark configuration.
        """
        return self.model_dump(by_alias=True)


class S3Config(BaseModel):
    """S3 configuration."""

    region_name: str = "eu-central-1"
    bucket: str = "s3-nord-challenge-data"

    @property
    def endpoint_url(self) -> str:
        """Get S3 endpoint URL."""
        return f"{self.region_name}.amazonaws.com"

    @property
    def folders(self) -> list[str]:
        """Get S3 folders."""
        return [f"{self.bucket}/0/", f"{self.bucket}/1/"]


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    redis: RedisConfig = RedisConfig()
    db: DBConfig = DBConfig()
    spark: SparkConfig = SparkConfig()
    s3: S3Config = S3Config()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="NSAPP_",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()

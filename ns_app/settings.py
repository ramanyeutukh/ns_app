import enum

from pydantic import BaseModel
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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="NSAPP_",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()

import uvicorn

from ns_app.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "ns_app.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        loop="uvloop",
        lifespan="on",
        http="httptools",
        factory=True,
    )


if __name__ == "__main__":
    main()

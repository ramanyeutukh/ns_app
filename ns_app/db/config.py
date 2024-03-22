from ns_app.settings import settings

MODELS_MODULES: list[str] = [
    "ns_app.db.models",
]

TORTOISE_CONFIG = {
    "connections": {
        "default": str(settings.db.url),
    },
    "apps": {
        "models": {
            "models": [*MODELS_MODULES, "aerich.models"],
            "default_connection": "default",
        },
    },
}

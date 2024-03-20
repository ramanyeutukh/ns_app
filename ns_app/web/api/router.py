from fastapi.routing import APIRouter

from ns_app.web.api import monitoring, tasks

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(tasks.router)

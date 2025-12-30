from fastapi import APIRouter

from .endpoints.health import router as health_router
from .endpoints.auth import router as auth_router
from .endpoints.task import router as task_router

router = APIRouter()
router.include_router(health_router, prefix="/health", tags=["Salud"])
router.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
router.include_router(task_router, prefix="/tasks", tags=["Tareas"])

__all__ = ["router"]

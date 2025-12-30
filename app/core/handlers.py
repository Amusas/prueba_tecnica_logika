from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.auth import InvalidCredentialsException, UserNotFoundException, InvalidTokenException, ExpiredTokenException
from app.exceptions.task import TaskNotFoundException, NotTaskOwnerException
from app.core.logging import logger

"""
Este módulo contiene los manejadores de excepciones personalizadas de la aplicación.
Cada manejador captura una excepción específica y devuelve una respuesta JSON consistente,
además de registrar el evento en los logs con el contexto de la petición.
"""

async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException) -> JSONResponse:
    """Maneja errores de autenticación por credenciales incorrectas."""
    logger.warning(
        "Contraseña invalida",
        path=request.url.path,
        error=exc.detail,
        ip=request.client.host
    )
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "code": 400,
            "message": exc.detail
        }
    )

async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException) -> JSONResponse:
    """Maneja casos donde el usuario solicitado no existe en la base de datos."""
    logger.warning(
        "Usuario no encontrado",
        path=request.url.path,
        error=exc.detail,
        ip=request.client.host
    )
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "code": 404,
            "message": exc.detail
        }
    )

async def invalid_token_exception_handler(request: Request, exc: InvalidTokenException) -> JSONResponse:
    """Maneja errores de tokens JWT malformados o inválidos."""
    logger.warning(
        "Token inválido",
        path=request.url.path,
        error=exc.detail,
        ip=request.client.host
    )
    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "code": 401,
            "message": exc.detail
        }
    )

async def expired_token_exception_handler(request: Request, exc: ExpiredTokenException) -> JSONResponse:
    """Maneja casos donde el token JWT ha superado su tiempo de vida."""
    logger.warning(
        "Token expirado",
        path=request.url.path,
        error=exc.detail,
        ip=request.client.host
    )
    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "code": 401,
            "message": exc.detail
        }
    )

async def task_not_found_exception_handler(request: Request, exc: TaskNotFoundException) -> JSONResponse:
    """Maneja casos donde la tarea solicitada no existe o ha sido eliminada."""
    logger.warning(
        "Tarea no encontrada",
        path=request.url.path,
        error=exc.detail,
        ip=request.client.host
    )
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "code": 404,
            "message": exc.detail
        }
    )

async def not_task_owner_exception_handler(request: Request, exc: NotTaskOwnerException) -> JSONResponse:
    """Maneja intentos de acceso o modificación de tareas que no pertenecen al usuario autenticado."""
    logger.warning(
        "Acceso denegado: No es el dueño de la tarea",
        path=request.url.path,
        error=exc.detail,
        ip=request.client.host
    )
    return JSONResponse(
        status_code=403,
        content={
            "success": False,
            "code": 403,
            "message": exc.detail
        }
    )

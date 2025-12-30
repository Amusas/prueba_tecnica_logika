from fastapi import FastAPI
from app.core import handlers
from app.exceptions.auth import (
    InvalidCredentialsException,
    UserNotFoundException,
    InvalidTokenException,
    ExpiredTokenException
)
from app.exceptions.task import (
    TaskNotFoundException,
    NotTaskOwnerException
)

def register_exception_handlers(app: FastAPI) -> None:
    """
    Centraliza el registro de manejadores de excepciones personalizadas en la aplicación.
    
    Permite mantener main.py limpio delegando la configuración de respuestas
    de error personalizadas a este módulo.
    """
    app.add_exception_handler(InvalidCredentialsException, handlers.invalid_credentials_exception_handler)
    app.add_exception_handler(UserNotFoundException, handlers.user_not_found_exception_handler)
    app.add_exception_handler(InvalidTokenException, handlers.invalid_token_exception_handler)
    app.add_exception_handler(ExpiredTokenException, handlers.expired_token_exception_handler)
    app.add_exception_handler(TaskNotFoundException, handlers.task_not_found_exception_handler)
    app.add_exception_handler(NotTaskOwnerException, handlers.not_task_owner_exception_handler)

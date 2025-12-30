from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

"""
Esquemas comunes para la estandarización de respuestas y autenticación.
"""

T = TypeVar("T")

class CustomResponse(BaseModel, Generic[T]):
    """
    Estructura genérica para todas las respuestas exitosas de la API.
    """
    success: bool
    code: int
    message: str
    data: Optional[T] = None

class ErrorResponse(BaseModel):
    """
    Estructura estándar para las respuestas de error de la API.
    """
    success: bool = False
    code: int
    message: str

class LoginRequest(BaseModel):
    """Esquema para la solicitud de inicio de sesión."""
    email: str
    password: str

class TokenResponse(BaseModel):
    """Esquema para la entrega del token JWT generado."""
    access_token: str
    token_type: str

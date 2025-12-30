from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.auth import LoginRequest, TokenResponse, CustomResponse, ErrorResponse
from app.services.auth import authenticate_user
from app.core.logging import logger

router = APIRouter()

@router.post(
    "/login", 
    response_model=CustomResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Contraseña inválida"},
        404: {"model": ErrorResponse, "description": "Usuario no encontrado"},
    },
    summary="Iniciar sesión",
    description="Autentica a un usuario con email y contraseña, devolviendo un token JWT de acceso."
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(deps.get_db)
):
    logger.info("Intento de inicio de sesión", email=login_data.email)
    access_token = authenticate_user(db, login_data.email, login_data.password)
    logger.info("Login exitoso", email=login_data.email)
    
    return CustomResponse(
        success=True,
        code=200,
        message="Login Exitoso",
        data=TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )
    )

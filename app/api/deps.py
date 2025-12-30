from typing import Generator
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.config import settings
from app.models.user import User
from app.exceptions.auth import InvalidTokenException, ExpiredTokenException, UserNotFoundException

# Configuración del esquema para autenticación mediante Bearer Token (JWT)
# Se utiliza HTTPBearer para que Swagger permita ingresar el token directamente
security = HTTPBearer()

def get_db() -> Generator:
    """
    Inyección de dependencia para obtener una sesión de base de datos.
    Asegura el cierre de la conexión al finalizar la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    auth: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Valida el token JWT y recupera el usuario autenticado de la base de datos.
    
    Args:
        db: Sesión de base de datos.
        auth: Credenciales de autorización que contienen el token.
        
    Returns:
        Instancia del modelo User si el token es válido.
        
    Raises:
        InvalidTokenException: Si el token está mal formado o falta.
        ExpiredTokenException: Si el token ha expirado.
        UserNotFoundException: Si el usuario del token ya no existe.
    """
    token = auth.credentials
    try:
        # Decodificación y validación del token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise InvalidTokenException()
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()
    except JWTError:
        raise InvalidTokenException()
        
    # Recuperación del usuario a partir del ID (sub) almacenado en el token
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise UserNotFoundException()
        
    return user

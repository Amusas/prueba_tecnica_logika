from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.exceptions.auth import InvalidCredentialsException, UserNotFoundException
from app.core.logging import logger

def authenticate_user(db: Session, email: str, password: str) -> str:
    """
    Valida las credenciales de un usuario y genera un token de acceso.
    
    Args:
        db: Sesión de base de datos.
        email: Correo electrónico del usuario.
        password: Contraseña en texto plano.
        
    Returns:
        Token JWT de acceso si las credenciales son válidas.
        
    Raises:
        UserNotFoundException: Si el email no está registrado.
        InvalidCredentialsException: Si la contraseña no coincide.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning("Fallo de autenticación: Usuario no encontrado", email=email)
        raise UserNotFoundException(detail="Usuario no encontrado")
        
    if not verify_password(password, user.hashed_password):
        logger.warning("Fallo de autenticación: Contraseña incorrecta", email=email)
        raise InvalidCredentialsException(detail="Contraseña invalida")
    
    logger.info("Usuario autenticado correctamente en el servicio", user_id=user.id, email=email)
    
    # El 'sub' del token contiene el ID del usuario como cadena
    return create_access_token(data={"sub": str(user.id)})

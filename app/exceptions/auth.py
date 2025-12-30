class AuthenticationException(Exception):
    """Clase base para todas las excepciones relacionadas con la autenticación."""
    pass

class InvalidCredentialsException(AuthenticationException):
    """Lanzada cuando la contraseña proporcionada no coincide con el hash almacenado."""
    def __init__(self, detail: str = "Contraseña invalida"):
        self.detail = detail

class UserNotFoundException(AuthenticationException):
    """Lanzada cuando se intenta autenticar un email que no existe en el sistema."""
    def __init__(self, detail: str = "Usuario no encontrado"):
        self.detail = detail

class InvalidTokenException(AuthenticationException):
    """Lanzada cuando el token JWT no puede ser decodificado o tiene un formato incorrecto."""
    def __init__(self, detail: str = "Token inválido o malformado"):
        self.detail = detail

class ExpiredTokenException(AuthenticationException):
    """Lanzada cuando un token JWT válido ha superado su fecha de expiración."""
    def __init__(self, detail: str = "El token ha expirado"):
        self.detail = detail

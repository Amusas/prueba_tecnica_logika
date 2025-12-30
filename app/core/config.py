from typing import Optional, Any
from pydantic import ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.core.logging import logger

class Settings(BaseSettings):
    """
    Configuración global de la aplicación.
    Carga valores desde variables de entorno o un archivo .env.
    """
    PROJECT_NAME: str = "Prueba Técnica Logika"
    DEBUG: bool = True
    API_V1_STR: str = "/api"
    
    # Credenciales de Base de Datos
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: str
    DATABASE_URL: Optional[str] = None
    
    # Configuración de Seguridad JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: Any) -> Any:
        """
        Construye automáticamente la URL de conexión a PostgreSQL
        si no se proporciona una explícitamente.
        """
        if isinstance(v, str) and v:
            return v
        
        data = info.data
        return f"postgresql://{data.get('DB_USER')}:{data.get('DB_PASSWORD')}@{data.get('DB_HOST')}:{data.get('DB_PORT')}/{data.get('DB_NAME') or ''}"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

# Intento de carga de configuración al importar el módulo
try:
    settings = Settings()
    logger.info(
        "Configuración cargada correctamente",
        service="api",
        environment="docker"
    )

except ValidationError as e:
    # Notificación de errores de validación en variables de entorno críticas
    for error in e.errors():
        logger.critical(
            "Error en variable de entorno",
            variable=".".join(map(str, error["loc"])),
            descripcion=error["msg"],
            tipo_error=error["type"],
        )

    logger.critical(
        "La aplicación no puede iniciarse por configuración inválida"
    )

    raise RuntimeError(
        "Fallo crítico de configuración: revisa las variables de entorno"
    )

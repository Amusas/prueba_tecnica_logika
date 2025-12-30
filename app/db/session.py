from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from tenacity import retry, stop_after_attempt, wait_fixed, before_log, after_log, retry_if_exception_type
import logging
from sqlalchemy.exc import OperationalError
from app.core.config import settings
from app.core.logging import logger

"""
Configuración de la conexión a la base de datos PostgreSQL utilizando SQLAlchemy.
Incluye una política de reintentos para manejar fallos temporales de conexión durante el inicio.
"""

# Configuración de reintentos: 10 intentos con pausa de 4 segundos entre cada uno
max_tries = 10
wait_seconds = 4

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    retry=retry_if_exception_type(OperationalError),
    before=before_log(logging.getLogger("tenacity.retry"), logging.INFO),
    after=after_log(logging.getLogger("tenacity.retry"), logging.WARN),
)
def get_engine():
    """
    Crea y verifica la conexión con el motor de la base de datos.
    Utiliza una política de reintentos para asegurar que la DB esté lista.
    """
    logger.info("Intentando conectar a la base de datos...")
    engine = create_engine(settings.DATABASE_URL)
    try:
        # Intento de conexión simple para verificar disponibilidad inmediata
        with engine.connect() as connection:
            logger.info("Conexión a la base de datos establecida exitosamente.")
        return engine
    except Exception as e:
        logger.error(f"Fallo al conectar a la base de datos: {e}")
        raise e

# Inicialización única del engine para toda la aplicación
engine = get_engine()

# Fábrica de sesiones para interactuar con la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para la definición de modelosORM
Base = declarative_base()

def get_db():
    """
    Generador de sesiones de base de datos para inyección de dependencias.
    Asegura que la sesión se cierre correctamente después de cada uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

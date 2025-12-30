import structlog
import logging
import sys

def configure_logger():
    """
    Configura el sistema de logging estructurado utilizando structlog.
    
    Establece los procesadores necesarios para incluir niveles de log,
    marcas de tiempo en formato ISO y renderizado final en JSON para
    facilitar la trazabilidad en entornos dockerizados.
    """
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

# Instancia global del logger para ser utilizada en toda la aplicación
logger = structlog.get_logger()

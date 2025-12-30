from fastapi import FastAPI
from app.api import router as api_router
from app.core.logging import configure_logger, logger
from app.core.exception_registry import register_exception_handlers
from app.db.init_db import init_db
from app.db.session import SessionLocal

# Configuración inicial del logger estructurado
configure_logger()

# Configuración detallada de metadatos para OpenAPI
app = FastAPI(
    title="Logika - API de Gestión de Tareas",
    description="""
API moderna para la gestión de tareas desarrollada para la prueba técnica de Logika.

### Características:
* **Autenticación**: Basada en JWT (JSON Web Tokens).
* **Gestión de Tareas**: Operaciones CRUD completas con control de propiedad.
* **Seguridad**: Los usuarios solo pueden ver y modificar sus propias tareas.
* **Paginación**: Soporte nativo para listados extensos.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

logger.info("Iniciando aplicación", title=app.title)

# Registro de rutas modulares
app.include_router(api_router, prefix="/api")
logger.info("Rutas de la API registradas")

# Registro centralizado de manejadores de excepciones
register_exception_handlers(app)
logger.info("Manejadores de excepciones registrados")

@app.on_event("startup")
async def startup_event() -> None:
    """
    Evento disparado al iniciar el servidor.
    Se utiliza para realizar la inicialización de la base de datos y semillas.
    """
    logger.info("Ejecutando evento de inicio (startup)")
    db = SessionLocal()
    try:
        init_db(db)
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error durante la inicialización de la base de datos: {e}")
    finally:
        db.close()

@app.get("/", summary="Bienvenida", tags=["General"])
async def root():
    """Punto de entrada raíz de la API."""
    return {"message": "Bienvenido a la API de Prueba Técnica de Logika. Visita /docs para la documentación."}

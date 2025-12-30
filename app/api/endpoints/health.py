from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from pydantic import BaseModel
import time

router = APIRouter()

class HealthCheckResponse(BaseModel):
    status: str
    checks: dict[str, str]
    response_time_ms: int

@router.get(
    "/",
    summary="Estado de salud del sistema",
    description="Realiza una verificación técnica para asegurar que la API y sus dependencias (base de datos) están operativas.",
    tags=["Salud"],
    response_model=HealthCheckResponse
)
def health_check(db: Session = Depends(get_db)):
    checks = {}
    overall_status = "UP"
    start_time = time.time()

    # Verificación de conexión con la base de datos
    try:
        db.execute(text("SELECT 1"))
        checks["database"] = "UP"
    except Exception as e:
        checks["database"] = f"DOWN: {str(e)}"
        overall_status = "DOWN"

    response_time_ms = int((time.time() - start_time) * 1000)

    return {
        "status": overall_status,
        "checks": checks,
        "response_time_ms": response_time_ms
    }

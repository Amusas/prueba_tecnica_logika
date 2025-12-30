from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.core.enums import TaskStatus

"""
Esquemas Pydantic para la validación y serialización de datos de tareas.
"""

class TaskCreateDTO(BaseModel):
    """Esquema para la creación de una nueva tarea."""
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.PENDING

class TaskUpdateDTO(BaseModel):
    """Esquema para la actualización parcial de una tarea existente."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

class TaskResponseDTO(BaseModel):
    """Esquema para la respuesta detallada de una tarea."""
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    # Permite crear el DTO directamente desde un objeto ORM de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.enums import TaskStatus
from sqlalchemy.sql import func
from app.db.session import Base

class Task(Base):
    """
    Modelo representativo de las tareas asignadas a los usuarios.
    Asociado a la tabla 'tasks'.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    # El estado utiliza el enum TaskStatus para validación a nivel de aplicación
    status = Column(Enum(TaskStatus, values_callable=lambda x: [e.value for e in x]), nullable=False, index=True, default=TaskStatus.PENDING)
    # Referencia al propietario de la tarea
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Sellos de tiempo automáticos
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Navegación hacia el propietario
    owner = relationship("User", back_populates="tasks")
